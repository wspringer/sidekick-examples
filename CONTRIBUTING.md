# Contributing an example

Each example is a folder containing a **reproducible recipe**. The point is that anyone can clone it, run the prompt against Sidekick, and get the documented result.

## Folder layout

```
<slug>/
  README.md        # required — see below
  before.idml      # the starting document (IDML, not INDD)
  <data files>     # any input the prompt references (xlsx, csv, images…)
  after.idml       # optional — the expected result, for eyeballing
  *.pdf            # optional — exported output, if the example produces one
```

The folder `<slug>` should match the slug of its blog post (if it has one), so the two are trivial to cross-reference.

## The README is the source of truth

The most important file is `README.md`. It must contain:

- **The problem** — one short paragraph a designer would recognize.
- **The exact prompt** — copy-pasteable, the literal text you'd give Claude.
- **What Sidekick should produce** — so a reader (and our own regression checks) can tell whether a run succeeded.
- **The why** — any non-obvious logic (e.g. the imposition page-order math), so the example teaches, not just demonstrates.

## Asset hygiene (non-negotiable)

Everything in this repo is **public forever**. Therefore every asset must be:

- **Fictional** — invented company names, made-up pricing, placeholder copy. Never a real client's file or content.
- **Self-made** — no paid stock images, no licensed fonts. Use system fonts and shapes/text you created.
- **Small** — prefer `.idml` (zipped XML) over `.indd`. Keep data files lean.

When in doubt, leave it out. A missing asset is recoverable; a leaked client file or a stock-license violation is not.

## Prefer IDML over INDD

Save starting documents as **IDML** (`File → Save a Copy → InDesign Markup`). It's smaller, somewhat diffable, and opens across InDesign versions. The opaque binary `.indd` should be the exception, not the rule.
