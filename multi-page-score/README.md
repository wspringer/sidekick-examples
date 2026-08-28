# Multi-page score

Engrave a four-page Schubert song with [GNU LilyPond](https://lilypond.org)
and lay it out in InDesign — title page, running heads, page numbers, a
colophon — with the text *inside* the music (lyrics, tempo, title) set in the
same face as the document's body text. LilyPond engraves; InDesign owns
everything around the music; Claude connects the two.

This is the companion to the blog post
[Sheet music in InDesign: a multi-page score in the document's own font](https://sidekick.eastpole.nl/blog/multi-page-score/).

## The problem

InDesign has no idea what a musical score is. Notation goes through a
notation program, comes out as a PDF, and gets placed page by page. Two
things are tedious about that: the page-by-page placing itself, and the fact
that the music arrives with its own typography. The lyrics and tempo marks
are in whatever the notation program defaulted to, the book is in something
else, and the page looks like two typesetters worked on it without meeting.

Here the notation program is LilyPond, driven through the
[lilypond-mcp](https://github.com/wspringer/lilypond-mcp) server, and Claude
does both jobs: it sizes LilyPond's pages to the InDesign type area so that
page *n* of the score lands on page *n* of the document, and it finds out
which font file InDesign uses for the body text and hands that same file to
LilyPond.

## The files

| File | What it is |
|------|------------|
| `before.idml` | the starting document: A4, facing pages, a title page and a colophon, an `A-Music` parent with running heads and page numbers, and a `Body` style in Minion Pro |
| `score.ly` | *An den Mond*, D 296 (Schubert / Goethe) — the [Mutopia Project](https://www.mutopiaproject.org) transcription, updated with `convert-ly` for current LilyPond |
| `score-layout.ly` | what Claude made of it: the `\paper` block sized to the type area, headers off, fonts pointed at the body face |
| `score.pdf` | the engraved score, four pages |
| `after.idml` | the expected result, six pages |
| `an-den-mond.pdf` | the expected result, exported |
| `.mcp.json` | registers lilypond-mcp for Claude Code |
| `CLAUDE.md` | the recipe, as instructions Claude Code picks up automatically |

## Setup

Besides [Sidekick](https://sidekick.eastpole.nl/install), you need the
`lilypond` MCP server. In **Claude Code**, open this folder and the
`.mcp.json` takes care of it. In **Claude Desktop**, add the same entry to
`claude_desktop_config.json`:

```json
"lilypond": { "command": "npx", "args": ["-y", "lilypond-mcp@latest"] }
```

Nothing else to install: on the first engrave the server fetches a
WebAssembly build of LilyPond (~35 MB). Node 22 or newer.

## The prompt

Open `before.idml` in InDesign, make sure Sidekick is connected, then ask
Claude (or any other AI assistant):

> The song in `score.ly` has to go into the open document between the title
> page and the colophon, one engraved page per document page, with the
> `A-Music` parent applied to the new pages. Engrave it with LilyPond so that
> each PDF page is exactly the size of this document's type area, with no
> margins, headers or page numbers of its own — InDesign supplies those. Set
> the text in the score in the same font as the document's `Body` style: find
> out which font file InDesign loads for it and give that folder to
> LilyPond. Check the preview that the lyrics really come out in that font
> before placing anything.

## What should happen

1. Claude reads the document: A4, margins 20 / 25 / 20 / 18 mm, so a type
   area of 172 × 252 mm; `Body` is Minion Pro Regular, and InDesign reports
   where it loaded the file from — on macOS
   `/Applications/Adobe InDesign 2026/Resources/Required/fonts/MinionPro-Regular.otf`.
2. It rewrites the `\paper` block of the score: page 172 × 252 mm, zero
   margins, no headers or page numbers, `fonts.serif = "Minion Pro"` (see
   `score-layout.ly`).
3. It engraves with `engrave_file`, uncropped, passing that fonts folder as
   `font_dirs`, and looks at the preview: the lyrics are in Minion Pro. The
   PDF has four pages.
4. It inserts four pages after the title page, applies `A-Music`, draws a
   frame on the type area of each (mirrored for verso and recto) and places
   PDF page 1, 2, 3, 4 into them.

The result is a six-page document: title page, four pages of music with
running heads and page numbers 2–5, colophon. Compare with `after.idml`.

## The why

**LilyPond paginates, InDesign owns the furniture.** The alternative —
engraving each system as a cropped snippet and flowing them in a threaded
story — hands page breaking to InDesign, which knows nothing about page turns
or stretching systems to fill a page. LilyPond does that well; so its page
is made the size of the type area and placed one-to-one. Three things bite:

- `paper-width` alone does not change `line-width`; set both.
- A top-level `#(set-global-staff-size 19)` — which most LilyPond files
  have — silently disables `property-defaults.fonts`. The text falls back to
  DejaVu and nothing warns you. Move the staff size into `\paper` as
  `#(layout-set-staff-size 19)`.
- LilyPond rounds the page to whole points (172 mm becomes 488 pt, a tenth
  of a millimetre more), so after placing, fit the frame to the content.

**The font comes from InDesign, not from a guess.** Every `Font` in the
InDesign DOM has a `location` property: the path of the file it was loaded
from. Claude reads it through Sidekick and gives the directory to
lilypond-mcp's `font_dirs`; the family name goes into the score. Two
limits:

- Fonts activated through **Adobe Fonts** report `Added from Adobe Fonts`
  instead of a path, so they can't be handed over. The body font has to be
  on disk — a system font, or one of the fonts InDesign itself ships in
  `Resources/Required/fonts` (that folder is why this example works on a
  fresh InDesign install without installing anything).
- Only the styles that are actually on disk engrave. InDesign bundles Minion
  Pro as **Regular only**; ask LilyPond for bold or italic and it quietly
  uses Regular. That is why the score's title block has plain markups, and
  why `before.idml` uses no bold or italic either. The variable fonts in the
  same folder (Source Serif Variable and friends) are not picked up by
  LilyPond's fontconfig at all.

**`convert-ly` first.** Mutopia's file dates from 2008 (`\version
"2.11.60"`) and current LilyPond rejects it. lilypond-mcp's engine can't run
`convert-ly` (it's a Python tool), so `score.ly` here is already converted;
for your own old files, run `convert-ly -e` from a desktop LilyPond.

## Requirements

- InDesign with Sidekick; verified with InDesign 2026 on macOS. On Windows
  the bundled fonts live under `Program Files` — the path differs, which is
  exactly why Claude reads it instead of guessing.
- Node 22 or newer for lilypond-mcp.
- InDesign will ask for **folder access** the first time Claude places the
  PDF from this folder — grant it once per session.

## Attribution

The music is the public-domain LilyPond transcription of *An den Mond*, D 296
by Ph. Raynaud for the Mutopia Project (reference Mutopia-2008/10/30-1581),
after the Breitkopf & Härtel edition of 1884–1897. The colophon in the
document carries the same credit.
