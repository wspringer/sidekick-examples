# Update a pricing table from Excel

Update the priced table in an InDesign proposal from an Excel file — handling **changed line items, changed prices, and a different number of rows** — without losing the document's fonts or branding.

## The problem

You build proposals in InDesign with a pricing table whose numbers live in a spreadsheet. When the client revises the scope, the pricing changes: some line items are added, some prices move, the total shifts. Updating the InDesign table by hand is slow and error-prone, and the usual shortcuts let you down:

- **Data merge** repopulates the data but won't honour your brand fonts and table styling.
- **Variable row counts** break hand-written scripts — add or remove a line item and the script needs editing.
- **Copy-paste from Excel** drops your formatting and you re-style every cell.

Re-applying the *same* styling to *new* data, however many rows it is, is exactly what Sidekick can do.

## The files

| File | What it is |
|------|------------|
| `before.idml` | the proposal as it stands: a 4-line-item table, total **$14,500**, in the studio's brand colour and font |
| `pricing.xlsx` | the revised pricing from the client — **6 line items**, new prices, total **$19,400** |
| `after.idml` | the proposal after Sidekick applies the spreadsheet — same branding, new data |

The only difference between `before` and `after` is the **data**. The blue header, the Myriad Pro typeface, the column widths, and the bold total row all survive.

## The prompt

> Here's my InDesign proposal and an updated `pricing.xlsx`. Replace the line items in the pricing table with the rows from the spreadsheet, format the prices as currency, and recompute the total. Keep the table's existing styling exactly — the header colour, the font, the column widths, the bold total row — and add or remove rows as needed to match the spreadsheet.

(Attach both `before.idml`'s document — i.e. open it in InDesign — and `pricing.xlsx` to your AI assistant.)

## What Sidekick should produce

- The table's line items replaced with the **6 rows** from `pricing.xlsx`.
- Prices formatted as currency (`$4,800`), and the **Total** recomputed to **$19,400**.
- **Styling unchanged**: blue header row with white bold labels, Myriad Pro throughout, the same column widths, body rows in regular weight, the total row bold.
- Two rows added (4 → 6 line items) without any manual table surgery.

## Verified

Run end-to-end with Sidekick (plugin 1.0.13) on 2026-06-07 **by giving the prompt above to `before.idml` and changing nothing by hand**: the table grew from 4 to 6 line items, the prices and total updated ($19,400), and — with no manual restyling and no manual repositioning — the new rows kept regular-weight Myriad Pro with the correct row rules, the blue header and bold total held, and the footer note reflowed down below the longer table. Confirmed by snapshot.

## How the document is built (so the update "just works")

Two design choices make the update survive cleanly. They're worth copying in your own documents:

1. **The Total is a *footer* row**, not a body row. When you add rows to a table, InDesign copies the formatting of the adjacent row — so if the Total were the last body row, new rows would inherit *its* bold weight and heavy rule. Making the Total a footer row means new rows copy the last *line-item* row instead, keeping regular weight, right-aligned figures, and the thin rule automatically.
2. **The table and the footer note live in one auto-sizing text frame.** Because the note flows in the same story right after the table, a taller table pushes it down instead of colliding with it.

Without these, "replace the line items" leaves new rows bold and the note overlapping the total — which is exactly what a naive edit produces.

## Notes on the assets

`Northwind Studios` and `Vellum & Vine` are fictional. The brand colour is Sidekick's blue (`#0ea5e9`); the typeface is **Myriad Pro**, which ships with InDesign on every platform, so the example opens correctly for anyone.
