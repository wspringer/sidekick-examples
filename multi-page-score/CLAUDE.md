# Multi-page score — recipe

Engrave `score.ly` with the `lilypond` MCP server and place it in the open
InDesign document through Sidekick, one engraved page per document page, in
the document's own body font. Read `README.md` for the background; this file
is the procedure.

## 1. Read the document, don't assume

Through Sidekick's `execute`:

- page size and `facingPages` from `doc.documentPreferences`
- margins from `doc.pages.item(0).marginPreferences` (top, bottom, `left` =
  inside, `right` = outside) — the type area is what's left of the page
- the `Body` paragraph style's `appliedFont`: its `fontFamily`, and its
  **`location`** — the path of the font file InDesign loaded. Take the
  directory of that path; it is what LilyPond gets as `font_dirs`.

If `location` is the string `Added from Adobe Fonts` there is no file on disk
you can hand to LilyPond. Say so and stop; the user has to pick a body font
that is installed as a file.

## 2. Rewrite the `\paper` block of `score.ly`

Write the result to `score-layout.ly` (keep `score.ly` untouched):

```lilypond
\paper {
  #(layout-set-staff-size 19)          % NOT a top-level set-global-staff-size
  paper-width  = <type-area width>\mm
  paper-height = <type-area height>\mm
  line-width   = <type-area width>\mm  % paper-width alone does not set it
  top-margin = 0\mm  bottom-margin = 0\mm  left-margin = 0\mm  right-margin = 0\mm
  indent = 28\mm
  print-page-number = ##f
  oddHeaderMarkup = ##f  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f  evenFooterMarkup = ##f
  property-defaults.fonts.serif = "<Body font family>"
}
```

Also set `tagline = ##f` in `\header`, and remove any top-level
`#(set-global-staff-size …)` line — with one present, LilyPond ignores
`property-defaults.fonts` and falls back to DejaVu without an error.

## 3. Engrave and check

`engrave_file` with `source: "score-layout.ly"`, `formats: ["pdf"]`,
`crop: false` (full pages, not a cropped snippet), `font_dirs: [<directory
from step 1>]`, `output_dir: "."`. Look at the preview PNG the tool returns:
the lyrics and the title must be in the body font. If they are in a sans
serif, the font did not load — re-check steps 1 and 2 before placing
anything.

## 4. Place, one PDF page per document page

- Insert as many pages after page 1 as the PDF has, with
  `doc.pages.add(LocationOptions.AFTER, previousPage)`, and set
  `appliedMaster` to the `A-Music` parent on each.
- On each new page add a rectangle spanning the type area. Facing pages
  mirror: on a verso (`page.side.equals(PageSideOptions.LEFT_HAND)`) the
  frame runs from `marginPreferences.right` to `pageWidth -
  marginPreferences.left`; on a recto from `.left` to `pageWidth - .right`.
- Before each `place()`, set `app.pdfPlacePreferences.pageNumber` to the PDF
  page you want and `pdfCrop` to `PDFCrop.CROP_MEDIA`.
- After placing, `frame.fit(FitOptions.FRAME_TO_CONTENT)`: LilyPond rounds
  the page to whole points, so the PDF is a fraction of a millimetre larger
  than the frame.

Finish with a spread snapshot to confirm running heads, page numbers and the
music line up, then save.
