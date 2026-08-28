# Accessible formulas

Turn equations placed as **graphics** into equations a PDF can actually
*mean* — tagged `Formula` elements carrying the equation as **ActualText**,
which is what screen readers speak, what Acrobat's copy and text extraction
return, and what PDF/UA expects of math.

The point of this example: it **does not matter how the equation graphic was
made**. One equation here is a placed SVG file; the other is created with
InDesign's native Math Expressions feature (MathML). Both come out of InDesign
as vector outlines with no text in them — and both get their meaning back the
same way.

This is the minimal companion to the blog post
[Accessible Math in InDesign PDFs: Formula Tags and ActualText](https://sidekick.eastpole.nl/blog/accessible-math-pdf/).
For the full LaTeX-to-InDesign production workflow, see
[sidekick-math](https://github.com/wspringer/sidekick-math).

## The problem

A formula placed in InDesign as a graphic — an SVG from a math converter, or a
native math expression — exports to PDF as pure vector paths. Nothing to
select, nothing to search, nothing for a screen reader to say. An
accessibility check flags every one of them.

PDF's designed answer is **ActualText** ("whatever this region looks like,
*this* is what it says") on a **Formula** structure element. InDesign can carry
the ActualText through its tagged-PDF export, but tags every object `Figure`
and offers no way to change it — so the last step happens after export.

## The files

| File | What it is |
|------|------------|
| `quadratic-formula.svg` | the quadratic formula as an SVG (vector outlines, as a math converter produces) |
| `retag-formulas.py` | post-export step: renames `Figure` elements that carry ActualText to `Formula` (needs `pikepdf`) |

## The prompt

Make sure [Sidekick](https://sidekick.eastpole.nl/install) is connected, then
ask Claude (or any other AI assistant):

> Create a new A4 document in InDesign and place two equations on page 1:
>
> 1. the file `quadratic-formula.svg` from this folder, and
> 2. Euler's identity, e^(iπ) + 1 = 0, as a native math expression created
>    from MathML.
>
> Give each placed equation accessibility data through its object export
> options: set the **actual text** to the equation as plain Unicode
> (e.g. `x = (-b ± √(b² − 4ac)) / 2a`), and the **alt text** to a spoken-form
> description. Then export a tagged PDF into this folder and run
> `retag-formulas.py` on it. Finally, read the structure tree back from the
> finished PDF and show me that both equations are `Formula` elements with
> their ActualText.

## What should happen

Claude places both equations (the SVG via a place call, Euler's identity via
`doc.createFromMathML`), sets `customActualText` and `customAltText` on each,
exports with the document structure included, and runs the re-tag script. The
finished PDF's structure tree contains, for each equation:

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

- InDesign **2025 or newer** for the native math expression half (the SVG half
  works in any version Sidekick supports)
- Python 3 with `pikepdf` for the re-tag step: `pip install pikepdf`
- InDesign will ask for **folder access** the first time Claude places the SVG
  or writes the PDF — grant it once per session

## Assets

`quadratic-formula.svg` was generated with
[math-svg-mcp](https://github.com/wspringer/math-svg-mcp) from
`x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}`.
