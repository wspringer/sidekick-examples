# Accessible formulas — instructions for Claude

Goal of this example: equations created with InDesign's native Math
Expressions feature (MathML) must end up in the exported PDF as `Formula`
structure elements carrying the equation as **ActualText**. The same recipe
applies to any equation placed as a graphic.

## The recipe

**1. Create each equation as a native math expression:**

```js
const mathObject = doc.createFromMathML(mathmlString, page, layer, ["30mm", "40mm"]);
```

(InDesign 2025+. The object keeps its MathML for editing, but the MathML is
**discarded on PDF export** — which is why ActualText matters.)

**2. Set accessibility data on every equation object:**

```js
const { SourceType } = require('indesign');
const oeo = item.objectExportOptions;
oeo.altTextSourceType = SourceType.SOURCE_CUSTOM;
oeo.customAltText = "x equals minus b plus or minus the square root of b squared minus 4 a c, all over 2 a"; // spoken form
oeo.actualTextSourceType = SourceType.SOURCE_CUSTOM;
oeo.customActualText = "x = (-b ± √(b² − 4ac)) / 2a"; // Unicode linearization
```

- ActualText is a plain-text linearization of the equation. **Never raw
  MathML/XML** — screen readers would read the tags aloud.
- Both `SOURCE_CUSTOM` assignments are required before the custom text takes
  effect.

**3. Export a tagged PDF.** `app.pdfExportPreferences.includeStructure` is
the "Create Tagged PDF" setting — it defaults to true; verify it before
exporting.

**4. Re-tag Figures as Formulas.** InDesign tags every placed object
`Figure`; PDF/UA wants `Formula`. Run the script in this folder on the
exported PDF:

```bash
python3 retag-formulas.py exported.pdf exported-accessible.pdf
```

It renames exactly the `Figure` elements that carry ActualText and prints
what it re-tagged. Requires `pikepdf` (`pip install pikepdf`). **This step
needs a shell** — if you cannot run shell commands (e.g. from Claude
Desktop), tell the user to run the command themselves in a terminal instead
of skipping the step.

**5. Verify.** The tags live in compressed object streams, so grepping the
raw PDF misses them. Read the structure tree back with pikepdf (adapt the
walker in `retag-formulas.py`) and confirm each equation is a `Formula` with
its ActualText.

## InDesign specifics

- Writing the PDF triggers InDesign's folder-permission dialog once per
  session; request access to this folder up front.
- Collections: use `.item(0)`, not `[0]`; compare DOM objects with
  `.equals()`, not `===`.
