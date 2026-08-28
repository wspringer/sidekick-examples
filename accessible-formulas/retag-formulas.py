#!/usr/bin/env python3
"""Re-tag equation Figures as Formula elements in a tagged PDF.

InDesign tags every placed object as a Figure; PDF/UA wants equations tagged
Formula. This script renames exactly the Figure structure elements that carry
ActualText — which, in this workflow, is the equations.

Usage:
    python3 retag-formulas.py input.pdf output.pdf

Requires: pikepdf  (pip install pikepdf)
"""

import sys

import pikepdf
from pikepdf import Name


def walk(elem, stats):
    if not isinstance(elem, pikepdf.Dictionary):
        return
    if elem.get("/S") == Name("/Figure") and elem.get("/ActualText"):
        elem.S = Name("/Formula")
        stats.append(str(elem.get("/ActualText")))
    kids = elem.get("/K")
    if isinstance(kids, pikepdf.Array):
        for kid in kids:
            walk(kid, stats)
    elif kids is not None:
        walk(kids, stats)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    with pikepdf.open(src) as pdf:
        root = pdf.Root.get("/StructTreeRoot")
        if root is None:
            sys.exit(
                "No structure tree found — export the PDF with "
                "'Create Tagged PDF' enabled and try again."
            )
        stats = []
        walk(root.get("/K"), stats)
        pdf.save(dst)
    print(f"Re-tagged {len(stats)} equation(s) as Formula:")
    for text in stats:
        print(f"  {text}")


if __name__ == "__main__":
    main()
