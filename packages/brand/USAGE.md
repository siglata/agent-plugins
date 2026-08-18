# SIGLATA marks

`brand` is the single import path for the SIGLATA marks. The package currently
contains the existing favicon and the `⊢ SIGLATA` lockup. The manifest records
the formats that still need a design decision or production asset.

## Clear space

Keep at least the height of the `⊢` glyph empty on every side of the lockup. Use
the same rule around the favicon when it appears beside another mark. The space
belongs to the mark; text, controls, borders, and other logos do not enter it.

## Minimum size

Render the live-text wordmark at the 16px size used by `/install`. At smaller
sizes, use the favicon only when its rules remain distinct. The favicon floor is
16px square. The pending app-icon files will define their own raster sizes when
the design work is commissioned.

## Colour and type

The wordmark uses Inter at weight 600. A colour lockup uses `--brand`, which is
`--teal-9` and has the value `#0b625f`. Use the token in an inline or component
implementation so the colour follows the register. The SVG keeps the letters as
text rather than outlines.

## Misuse

Do not redraw the glyph, outline the wordmark, change its tracking, stretch it,
rotate it, add an effect, or place another mark inside its clear space. Do not
replace `⊢` with a similar character. Use the package export and the declared
format for the surface; pending formats are gaps, not alternate files to invent
locally.
