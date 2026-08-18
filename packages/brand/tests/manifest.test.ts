import * as Arr from "effect/Array";
import * as Effect from "effect/Effect";
import * as FileSystem from "effect/FileSystem";
import * as HashSet from "effect/HashSet";
import * as P from "effect/Predicate";
import * as R from "effect/Record";
import * as Schema from "effect/Schema";
import { NodeFileSystem } from "@effect/platform-node";
import { expect, it } from "@effect/vitest";

import { brandManifest } from "../manifest.ts";
import * as brand from "../src/index.ts";

interface BrandReference {
  readonly path: string;
  readonly url: URL;
}

const isUrl = Schema.is(Schema.instanceOf(globalThis.URL));

const isBrandReference = (value: unknown): value is BrandReference =>
  P.isObject(value) &&
  P.hasProperty(value, "path") &&
  P.isString(value.path) &&
  P.hasProperty(value, "url") &&
  isUrl(value.url);

const exportedBrandReferences = (): readonly BrandReference[] =>
  Arr.filter(R.values(brand), isBrandReference);

const packageRoot = new URL("../", import.meta.url);
const pathOnDisk = (path: string): string => new URL(path, packageRoot).pathname;

it("the manifest declares each asset once", () => {
  const keys = Arr.map(brandManifest, (asset) => `${asset.id}.${asset.format}`);
  expect(HashSet.size(HashSet.fromIterable(keys))).toBe(keys.length);
});

it.layer(NodeFileSystem.layer)("the brand assets on disk", (suite) => {
  suite.effect("keeps ready and pending statuses true on disk", () =>
    Effect.gen(function* manifestStatuses() {
      const fileSystem = yield* FileSystem.FileSystem;
      const presence = yield* Effect.forEach(
        brandManifest,
        (asset) =>
          Effect.map(fileSystem.exists(pathOnDisk(asset.path)), (exists) => ({ asset, exists })),
        { concurrency: 1 },
      );

      const missingReady = presence.filter(
        ({ asset, exists }) => asset.status === "ready" && !exists,
      );
      const presentPending = presence.filter(
        ({ asset, exists }) => asset.status === "pending" && exists,
      );

      expect(missingReady.map(({ asset }) => asset.path)).toEqual([]);
      expect(presentPending.map(({ asset }) => asset.path)).toEqual([]);
    }),
  );

  suite.effect("registers every exported reference and resolves it", () =>
    Effect.gen(function* exportedReferences() {
      const fileSystem = yield* FileSystem.FileSystem;
      const declaredPaths = HashSet.fromIterable(Arr.map(brandManifest, (asset) => asset.path));
      const references = exportedBrandReferences();

      expect(references.length).toBeGreaterThan(0);
      expect(
        Arr.filter(
          Arr.map(references, (reference) => reference.path),
          (path) => !HashSet.has(declaredPaths, path),
        ),
      ).toEqual([]);

      const presence = yield* Effect.forEach(
        references,
        (reference) =>
          Effect.map(fileSystem.exists(reference.url.pathname), (exists) => ({
            exists,
            reference,
          })),
        { concurrency: 1 },
      );
      expect(
        Arr.map(
          Arr.filter(presence, ({ exists }) => !exists),
          ({ reference }) => reference.path,
        ),
      ).toEqual([]);
    }),
  );
});
