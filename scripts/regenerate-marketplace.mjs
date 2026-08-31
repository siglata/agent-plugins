import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const valueFor = (name, fallback) => {
  const index = process.argv.indexOf(name);
  return index < 0 ? fallback : process.argv[index + 1];
};

const destination = resolve(valueFor("--destination", process.cwd()));
const source = resolve(
  valueFor("--source", process.env.SIGLATA_SOURCE_DIR) ??
    (() => {
      throw new Error("--source or SIGLATA_SOURCE_DIR is required");
    })(),
);
const sourcePlugin = resolve(source, "plugins/siglata");
const destinationPlugin = resolve(destination, "plugins/siglata");
sourcePlugin === destinationPlugin &&
  (() => {
    throw new Error("source and destination must be different");
  })();
await rm(destinationPlugin, { force: true, recursive: true });
await cp(sourcePlugin, destinationPlugin, { recursive: true });

const plugin = JSON.parse(await readFile(resolve(destinationPlugin, "plugin.json"), "utf8"));
const marketplace = {
  name: plugin.name,
  interface: {
    displayName: "Siglata",
  },
  plugins: [
    {
      name: plugin.name,
      source: {
        source: "local",
        path: "./plugins/siglata",
      },
      policy: {
        installation: "AVAILABLE",
        authentication: "ON_INSTALL",
      },
      category: "Productivity",
    },
  ],
};

const marketplaceDirectory = resolve(destination, ".agents/plugins");
await mkdir(marketplaceDirectory, { recursive: true });
await writeFile(
  resolve(marketplaceDirectory, "marketplace.json"),
  `${JSON.stringify(marketplace, null, 2)}\n`,
);
