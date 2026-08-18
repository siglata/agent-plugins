export type BrandAssetStatus = "pending" | "ready";

export type BrandAssetFormat = "icns" | "ico" | "png" | "svg";

export interface BrandAsset {
  readonly id: string;
  readonly format: BrandAssetFormat;
  readonly path: string;
  readonly purpose: string;
  readonly status: BrandAssetStatus;
}

/**
 * One declaration per asset and format. A pending entry is a named design gap;
 * the brand gate reports it and waits for the asset to be commissioned.
 */
export const brandManifest = [
  {
    format: "svg",
    id: "symbol",
    path: "symbol/symbol.svg",
    purpose: "The SIGLATA glyph without a wordmark or background.",
    status: "pending",
  },
  {
    format: "svg",
    id: "wordmark",
    path: "wordmark/wordmark.svg",
    purpose: "The live-text ⊢ SIGLATA lockup from the /install template.",
    status: "ready",
  },
  {
    format: "svg",
    id: "wordmark-monochrome",
    path: "wordmark/monochrome.svg",
    purpose: "A single-ink wordmark for surfaces that cannot carry the brand colour.",
    status: "pending",
  },
  {
    format: "svg",
    id: "favicon",
    path: "favicon/favicon.svg",
    purpose: "The browser favicon and the existing SIGLATA mark migrated from the app.",
    status: "ready",
  },
  {
    format: "ico",
    id: "favicon",
    path: "favicon/favicon.ico",
    purpose: "The Windows and legacy browser favicon container.",
    status: "pending",
  },
  {
    format: "png",
    id: "apple-touch",
    path: "favicon/apple-touch-180.png",
    purpose: "The 180px Apple touch icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "social-og",
    path: "social/og-1200x630.png",
    purpose: "The 1200×630 Open Graph card.",
    status: "pending",
  },
  {
    format: "png",
    id: "social-twitter",
    path: "social/twitter.png",
    purpose: "The Twitter/X social card.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-16",
    path: "app-icon/16.png",
    purpose: "The 16px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-32",
    path: "app-icon/32.png",
    purpose: "The 32px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-48",
    path: "app-icon/48.png",
    purpose: "The 48px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-64",
    path: "app-icon/64.png",
    purpose: "The 64px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-128",
    path: "app-icon/128.png",
    purpose: "The 128px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-256",
    path: "app-icon/256.png",
    purpose: "The 256px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-512",
    path: "app-icon/512.png",
    purpose: "The 512px application icon.",
    status: "pending",
  },
  {
    format: "png",
    id: "app-icon-1024",
    path: "app-icon/1024.png",
    purpose: "The 1024px application icon source.",
    status: "pending",
  },
  {
    format: "icns",
    id: "app-icon-macos",
    path: "app-icon/macos.icns",
    purpose: "The macOS application icon container.",
    status: "pending",
  },
  {
    format: "ico",
    id: "app-icon-windows",
    path: "app-icon/windows.ico",
    purpose: "The Windows application icon container.",
    status: "pending",
  },
] as const satisfies readonly BrandAsset[];
