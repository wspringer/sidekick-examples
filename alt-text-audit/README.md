# Alt-text audit

Audit and fix the **alt text on every image** in an InDesign document in one
pass — find the images with no alt text and the ones carrying Adobe's
auto-generated *"AI generated…"* placeholder, and replace them with proper,
human-readable descriptions of **what's actually visible**.

## The problem

Accessible PDFs (WCAG / PDF-UA, and increasingly a legal requirement under the
European Accessibility Act) need alt text on every meaningful image. InDesign
makes you set it one frame at a time through **Object → Object Export Options**,
so on a real document it quietly gets skipped — and skipped alt text fails an
accessibility check on every figure.

Recent InDesign versions made it worse: they **auto-fill alt text with
AI-generated descriptions** stamped *"AI generated"*, which land on client photos
where they have no business being. Turning it off is its own chore, and removing
the placeholders is per-image drudgery.

Either way you need the same thing: a pass over **every** image that flags the
missing and the AI-generated ones and writes proper descriptions — and, crucially,
descriptions of *what the reader actually sees*, not of parts of an image that are
cropped away or hidden under another element. That last part is where a naive
approach (or Adobe's own AI) gets it wrong.

## The file

A two-page, monochrome editorial document (Minion Pro, 12 greyscale photos,
images embedded):

| File | What it is |
|------|------------|
| `before.idml` | the document as it stands — 12 images in a realistic mix of alt-text states |
| `images/` | the 12 source photos (greyscale; freely-licensed — see "Assets") |

**Starting state** — what the audit has to catch:

| Alt-text state | Count | Should become |
|----------------|-------|---------------|
| Adobe **"AI generated"** placeholder | 5 | a proper, human description |
| **Missing** (no alt text) | 4 | a proper, human description |
| **Good** (already human-written) | 3 | left untouched |

Page 1 deliberately places five images in **awkward ways**, so the audit's
descriptions are tested against the cases that trip up automatic alt text:

| Placement | What it tests |
|-----------|---------------|
| **Clipped by its frame** (the hero) | describe only the visible crop, not the whole asset |
| **Text overlay** (the title runs across the hero) | the headline is visible, but isn't part of the photo |
| **Partly hidden by a shape** | the covered part isn't visible, so it stays out of the alt text |
| **Rotated frame** | the bounding box has empty corners, not image content |
| **Oval frame** | the clip shape, not a rectangle, decides what's visible |

Page 2 is a plate of seven more ordinary photographs, so the audit has real
volume to work through.

## The prompt

Open `before.idml` in InDesign and ask your AI assistant:

> Audit the alt text on every image in this InDesign document. Show me which
> images are missing alt text and which have an auto-generated "AI generated"
> placeholder, then write proper alt text for those — describing only what is
> actually visible in each image as it sits on the page — and leave the images
> that already have good alt text alone.

Behind the scenes the assistant finds every image and reads its current alt text,
then looks at the pages as they're laid out before writing each description.
Because it sees the page the way the reader does, the description matches what's
actually visible.

## What Sidekick should produce

- An **audit**: the 5 AI-generated and 4 missing images flagged (9 to fix), the 3
  good ones recognised and left alone.
- **Proper descriptions** written for the 9 — none beginning with "AI generated",
  each describing the actual subject.
- **Visible-only correctness** on the awkward placements: the clipped hero
  described by its crop (not the full photo); the partly-hidden photo described by
  its visible part (not the area under the black block); the photo under the title
  described without the headline; the rotated and oval frames without their empty
  corners.

## Verified

Built with Sidekick: the 12 images were given their alt-text states
programmatically — 5 with the "AI generated" placeholder, 4 left empty, 3 written
properly — so the audit has a realistic mix to find. The awkward placements
(clipped, overlaid, partly hidden, rotated, oval) are what make "describe only
what's visible" the right rule, since each one shows the reader something
different from the raw image file.

## Assets

The 12 photos come from [Picsum](https://picsum.photos) (which serves
[Unsplash](https://unsplash.com/license)-licensed images — free to use, no
attribution required), converted to greyscale for the monochrome design. They are
embedded in the IDML so the file is self-contained; the originals are in
`images/`. The type is **Minion Pro**, which ships with InDesign on every
platform.
