# Booklet imposition (saddle-stitch)

Reorder a multi-page document into **printer spreads** so it can be printed double-sided and folded into a booklet — the imposition InDesign won't do for you when you just want a PDF.

## The problem

You've laid out an 8-page zine in reading order (page 1, 2, 3 … 8) and you want a **print-ready PDF**: print it double-sided, fold the stack in half, staple the spine, and the pages read in order.

InDesign won't give you this from **Export to PDF** — that exports single pages or reader spreads, not imposed printer spreads. And **Print Booklet** imposes but goes to a printer (or a PostScript file), not a clean PDF. If you don't have imposition software, you're stuck reordering pages by hand.

The reordering is pure, deterministic logic, though — exactly the kind of rule-based busywork Sidekick can take over.

## The imposition math

For a saddle-stitch booklet the page count must be a **multiple of 4**. Pages are paired by working inward from both ends. For 8 pages (2 folded sheets), the printer spreads are:

| Sheet | Side | Left page | Right page |
|------:|------|----------:|:-----------|
| 1 | outside | 8 | 1 |
| 1 | inside  | 2 | 7 |
| 2 | outside | 6 | 3 |
| 2 | inside  | 4 | 5 |

So the reader order `1 2 3 4 5 6 7 8` becomes the imposed sequence **`8 1 2 7 6 3 4 5`**.

General rule for `N` pages (N a multiple of 4): the sequence is `N, 1, 2, N-1, N-2, 3, 4, N-3, …` — outermost pair first, working inward.

## The prompt

> I have an 8-page InDesign document laid out in reading order (pages 1 through 8). I want to print it as a saddle-stitch booklet: printed double-sided, folded in half, and stapled. Reorder the pages into the correct printer-spread sequence for an 8-page booklet so that when it's folded the pages read in order, then export a print-ready PDF. Don't change the content of any page — only their order.

## What Sidekick should produce

- The document's pages reordered to **`8, 1, 2, 7, 6, 3, 4, 5`**.
- A `booklet.pdf` (8 single pages) in that imposed order.
- Page **content unchanged** — only the page sequence differs.

## Printing it

`booklet.pdf` is single pages in imposition order. To turn it into the booklet, print it **2 pages per sheet, double-sided (flip on short edge)**, then fold the stack in half and staple the spine. Each consecutive pair in the PDF becomes one sheet side:

`[8 1]` `[2 7]` `[6 3]` `[4 5]` — matching the sheet table above.

Most print shops (and the print tools at many public libraries) accept this directly: hand them the PDF and ask for "2-up, double-sided, saddle-stitch."

## Files

| File | What it is |
|------|------------|
| `before.idml` | 8-page document, one big page number (1–8) per page, in reading order |
| `after.idml` | the same document after imposition (pages in order 8,1,2,7,6,3,4,5) |
| `booklet.pdf` | the exported PDF, 8 single pages in imposed order |

To run it yourself: open `before.idml`, give Claude the prompt above, and compare against `after.idml` / `booklet.pdf`.

## Verified

Built and run end-to-end with Sidekick (plugin 1.0.13) on 2026-06-07: document created, pages reordered to `8,1,2,7,6,3,4,5` (confirmed page 8 lands in the first slot), and both `after.idml` and an 8-page `booklet.pdf` exported successfully.
