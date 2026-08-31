import * as Effect from "effect/Effect";
import * as FileSystem from "effect/FileSystem";
import * as Schema from "effect/Schema";
import { NodeFileSystem } from "@effect/platform-node";
import { deepStrictEqual, strictEqual } from "@effect/vitest/utils";
import { describe, it } from "@effect/vitest";

const root = `${import.meta.dirname}/../../../`;
const pluginSchemaUrl = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json";
const mcpSchemaUrl = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json";
const hostedEndpoint = "https://www.siglata.com/mcp";
const minimumCodexVersion = "0.147";

const authorSchema = Schema.Struct({
  name: Schema.optionalKey(Schema.String),
  email: Schema.optionalKey(Schema.String),
  url: Schema.optionalKey(Schema.String),
});

const pluginManifestSchema = Schema.fromJsonString(
  Schema.Struct({
    $schema: Schema.Literal(pluginSchemaUrl),
    name: Schema.String,
    version: Schema.optionalKey(Schema.String),
    description: Schema.optionalKey(Schema.String),
    author: Schema.optionalKey(authorSchema),
    homepage: Schema.optionalKey(Schema.String),
    repository: Schema.optionalKey(Schema.String),
    license: Schema.optionalKey(Schema.String),
    keywords: Schema.optionalKey(Schema.Array(Schema.String)),
    extensions: Schema.optionalKey(
      Schema.Record(Schema.String, Schema.Record(Schema.String, Schema.Unknown)),
    ),
  }),
);

const mcpManifestSchema = Schema.fromJsonString(
  Schema.Struct({
    $schema: Schema.Literal(mcpSchemaUrl),
    mcpServers: Schema.Record(
      Schema.String,
      Schema.Struct({
        type: Schema.Literal("streamable-http"),
        url: Schema.String,
        headers: Schema.optionalKey(Schema.Record(Schema.String, Schema.String)),
      }),
    ),
  }),
);

const marketplaceSchema = Schema.fromJsonString(
  Schema.Struct({
    name: Schema.String,
    interface: Schema.optionalKey(
      Schema.Struct({
        displayName: Schema.optionalKey(Schema.String),
      }),
    ),
    plugins: Schema.Array(
      Schema.Struct({
        name: Schema.String,
        source: Schema.Struct({
          source: Schema.Literal("local"),
          path: Schema.String,
        }),
        policy: Schema.Struct({
          installation: Schema.Literals(["AVAILABLE", "NOT_AVAILABLE", "INSTALLED_BY_DEFAULT"]),
          authentication: Schema.Literals(["ON_INSTALL", "ON_USE"]),
        }),
        category: Schema.String,
      }),
    ),
  }),
);

const codexOverlaySchema = Schema.fromJsonString(
  Schema.Struct({
    name: Schema.String,
    skills: Schema.String,
    mcpServers: Schema.String,
    interface: Schema.Struct({
      displayName: Schema.String,
      shortDescription: Schema.String,
      longDescription: Schema.String,
      developerName: Schema.String,
      category: Schema.String,
      capabilities: Schema.Array(Schema.String),
      websiteURL: Schema.String,
      defaultPrompt: Schema.Array(Schema.String),
    }),
  }),
);

const readFile = (path: string) =>
  Effect.gen(function* read() {
    const fileSystem = yield* FileSystem.FileSystem;
    return yield* fileSystem.readFileString(`${root}${path}`);
  });

const readJson = (path: string) => Effect.map(readFile(path), JSON.parse);

const keysOf = (value: Record<string, unknown>) => Object.keys(value).sort();

describe("Agent Plugins marketplace", () => {
  it.effect("validates the Agent Plugins 1.0 manifests and marketplace index", () =>
    Effect.gen(function* validate() {
      const plugin = yield* readJson("plugins/siglata/plugin.json");
      const mcp = yield* readJson("plugins/siglata/mcp.json");
      const marketplace = yield* readJson(".agents/plugins/marketplace.json");
      yield* Schema.decodeEffect(pluginManifestSchema)(JSON.stringify(plugin));
      yield* Schema.decodeEffect(mcpManifestSchema)(JSON.stringify(mcp));
      yield* Schema.decodeEffect(marketplaceSchema)(JSON.stringify(marketplace));
      deepStrictEqual(keysOf(plugin), [
        "$schema",
        "author",
        "description",
        "homepage",
        "keywords",
        "license",
        "name",
        "repository",
        "version",
      ]);
      deepStrictEqual(keysOf(mcp), ["$schema", "mcpServers"]);
      deepStrictEqual(keysOf(marketplace), ["interface", "name", "plugins"]);
      deepStrictEqual(keysOf(plugin.author), ["name", "url"]);
      deepStrictEqual(keysOf(mcp.mcpServers.siglata), ["type", "url"]);
      deepStrictEqual(keysOf(marketplace.plugins[0]), ["category", "name", "policy", "source"]);
      deepStrictEqual(keysOf(marketplace.plugins[0].source), ["path", "source"]);
      deepStrictEqual(keysOf(marketplace.plugins[0].policy), ["authentication", "installation"]);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("publishes Apache-2.0 plugin metadata", () =>
    Effect.gen(function* checkLicense() {
      const plugin = yield* readJson("plugins/siglata/plugin.json");
      const license = yield* readFile("plugins/siglata/LICENSE");
      strictEqual(plugin.license, "Apache-2.0");
      strictEqual(license.includes("Apache License"), true);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("keeps catalogue parameters in the generated artifact", () =>
    Effect.gen(function* checkCatalogue() {
      const skill = yield* readFile("plugins/siglata/skills/files/SKILL.md");
      const catalogue = yield* readFile("plugins/siglata/skills/files/catalogue.md");
      strictEqual(skill.includes("catalogue.md"), true);
      strictEqual(catalogue.length > 0, true);
      strictEqual(skill.includes("inputSchema"), false);
      strictEqual(skill.includes("outputSchema"), false);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("keeps the hosted Streamable HTTP endpoint in sync", () =>
    Effect.gen(function* checkEndpoint() {
      const mcp = yield* readJson("plugins/siglata/mcp.json");
      const server = mcp.mcpServers.siglata;
      strictEqual(server.type, "streamable-http");
      strictEqual(server.url, hostedEndpoint);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("declares the Codex 0.147 minimum in the Codex overlay", () =>
    Effect.gen(function* checkMinimum() {
      const overlay = yield* readJson("plugins/siglata/.codex-plugin/plugin.json");
      yield* Schema.decodeEffect(codexOverlaySchema)(JSON.stringify(overlay));
      strictEqual(overlay.interface.longDescription.includes(`Codex ${minimumCodexVersion}`), true);
      strictEqual(
        (yield* readFile("plugins/siglata/skills/files/SKILL.md")).includes(
          `Codex ${minimumCodexVersion}`,
        ),
        true,
      );
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("keeps Codex-only fields inside the overlay", () =>
    Effect.gen(function* checkNamespaces() {
      const plugin = yield* readJson("plugins/siglata/plugin.json");
      const overlay = yield* readJson("plugins/siglata/.codex-plugin/plugin.json");
      deepStrictEqual(
        Object.keys(plugin).filter((key) =>
          ["apps", "hooks", "interface", "mcpServers", "skills"].includes(key),
        ),
        [],
      );
      deepStrictEqual(
        Object.keys(overlay).filter((key) =>
          [
            "author",
            "description",
            "homepage",
            "keywords",
            "license",
            "repository",
            "version",
          ].includes(key),
        ),
        [],
      );
      deepStrictEqual(keysOf(overlay), ["interface", "mcpServers", "name", "skills"]);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("keeps the marketplace entry available and named Siglata", () =>
    Effect.gen(function* checkMarketplace() {
      const marketplace = yield* readJson(".agents/plugins/marketplace.json");
      strictEqual(marketplace.name, "siglata");
      strictEqual(marketplace.interface.displayName, "Siglata");
      strictEqual(marketplace.plugins[0].name, "siglata");
      strictEqual(marketplace.plugins[0].source.path, "./plugins/siglata");
      strictEqual(marketplace.plugins[0].policy.installation, "AVAILABLE");
      strictEqual(marketplace.plugins[0].policy.authentication, "ON_INSTALL");
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );

  it.effect("publishes only regenerated output and refuses dirty input", () =>
    Effect.gen(function* checkWorkflow() {
      const workflow = yield* readFile(".github/workflows/publish-marketplace.yml");
      strictEqual(workflow.includes("vp install --frozen-lockfile"), true);
      strictEqual(workflow.includes("vp test tests/marketplace.test.ts"), true);
      strictEqual(workflow.includes("if: env.SOURCE_TOKEN != ''"), true);
      strictEqual(workflow.includes("if: env.SOURCE_TOKEN == ''"), true);
      strictEqual(workflow.includes("token: ${{ env.SOURCE_TOKEN }}"), true);
      strictEqual(workflow.includes("vp run generate-catalogue"), true);
      strictEqual(
        workflow.includes(
          "bun scripts/regenerate-marketplace.mjs --source .source --destination .",
        ),
        true,
      );
      strictEqual(workflow.includes("git diff --exit-code"), true);
      strictEqual(
        workflow.includes("git diff --exit-code -- .agents/plugins plugins/siglata"),
        true,
      );
      strictEqual(workflow.includes("git commit"), false);
      strictEqual(workflow.includes("git push"), false);
    }).pipe(Effect.provide(NodeFileSystem.layer)),
  );
});
