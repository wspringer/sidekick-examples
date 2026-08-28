# Accessible formulas

Turn equations placed with InDesign's native **Math Expressions** feature
(MathML) into equations the exported PDF can actually *mean* — tagged
`Formula` elements carrying the equation as **ActualText**, which is what
screen readers speak, what Acrobat's copy and text extraction return, and
what PDF/UA expects of math.

This is the companion to the blog post
[Accessible Math in InDesign PDFs: Formula Tags and ActualText](https://sidekick.eastpole.nl/blog/accessible-math-pdf/).

## The problem

InDesign 2025 introduced native math: give it MathML and it renders a crisp
equation on the page. But that equation is a *graphic* — on PDF export it
becomes pure vector paths, and the MathML is discarded. Nothing to select,
nothing to search, nothing for a screen reader to say. An accessibility check
flags every equation in the document.

PDF's designed answer is **ActualText** ("whatever this region looks like,
*this* is what it says") on a **Formula** structure element. InDesign can
carry ActualText through its tagged-PDF export, but tags every object
`Figure` and offers no way to change it — so the last step happens after
export.

The same recipe works for *any* equation placed as a graphic, whatever made
it — this example uses native MathML so it needs nothing beyond InDesign and
Sidekick.

## The files

| File | What it is |
|------|------------|
| `retag-formulas.py` | post-export step: renames `Figure` elements that carry ActualText to `Formula` (needs `pikepdf`) |
| `CLAUDE.md` | the recipe, as instructions Claude Code picks up automatically |

## The prompt

Make sure [Sidekick](https://sidekick.eastpole.nl/install) is connected, then
ask Claude (or any other AI assistant):

> Create a new A4 document in InDesign and place two equations on page 1 as
> native math expressions from MathML: the quadratic formula, and Euler's
> identity e^(iπ) + 1 = 0.
>
> Give each equation accessibility data through its object export options:
> set the **actual text** to the equation as plain Unicode
> (e.g. `x = (-b ± √(b² − 4ac)) / 2a`), and the **alt text** to a spoken-form
> description. Then export a tagged PDF into this folder and run
> `retag-formulas.py` on it. Finally, read the structure tree back from the
> finished PDF and show me that both equations are `Formula` elements with
> their ActualText.

## What should happen

Claude creates both equations via `doc.createFromMathML`, sets
`customActualText` and `customAltText` on each, exports with the document
structure included, and runs the re-tag script. The finished PDF's structure
tree contains, for each equation:

```
Formula  (ActualText: "x = (-b ± √(b² − 4ac)) / 2a")
Formula  (ActualText: "e^(iπ) + 1 = 0")
```

## Seeing it for yourself

Open the finished PDF in **Acrobat** (Preview ignores tags):

- **Accessibility tags panel** — expand the tree, right-click a `<Formula>`
  tag → **Properties**: the Actual Text and Alternate Text fields hold the
  equation and its spoken form.
- **The copy test** — Select All, copy, paste into a text editor: the paste
  contains the equations as text, substituted from ActualText.
- **Read Out Loud** — Acrobat speaks the equations instead of skipping them.

What you *don't* get — in any PDF workflow — is glyph-level selection of the
outlines themselves; see the blog post for why that's a limitation of PDF
itself, not of this pipeline.

## Requirements

- InDesign **2025 or newer** (the Math Expressions feature)
- Python 3 with `pikepdf` for the re-tag step: `pip install pikepdf`
- InDesign will ask for **folder access** the first time Claude writes the
  PDF — grant it once per session

**Claude Code vs. Claude Desktop:** the re-tag step runs a Python script, so
the example works end to end from **Claude Code** (which also picks up the
`CLAUDE.md` in this folder automatically). From **Claude Desktop** there's no
shell — Claude will do the InDesign half and hand you the
`python3 retag-formulas.py …` command to run yourself in a terminal.
