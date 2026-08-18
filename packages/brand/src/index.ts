import type { BrandAsset } from "../manifest.ts";

export { brandManifest } from "../manifest.ts";
export type { BrandAsset, BrandAssetFormat, BrandAssetStatus } from "../manifest.ts";

export type BrandAssetReference = Pick<BrandAsset, "format" | "id" | "path"> & {
  readonly url: URL;
};

/** Public references. Consumers do not address files inside the package directly. */
export const favicon = {
  format: "svg",
  id: "favicon",
  path: "favicon/favicon.svg",
  url: new URL("../favicon/favicon.svg", import.meta.url),
} as const satisfies BrandAssetReference;

export const wordmark = {
  format: "svg",
  id: "wordmark",
  path: "wordmark/wordmark.svg",
  url: new URL("../wordmark/wordmark.svg", import.meta.url),
} as const satisfies BrandAssetReference;

export const assets = { favicon, wordmark } as const;
