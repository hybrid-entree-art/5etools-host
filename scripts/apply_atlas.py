#!/usr/bin/env python3
"""Inietta il livello UX ATLAS nel self-host 5e.tools."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = '<link rel="stylesheet" href="/atlas.css">'
JS = '<script defer src="/atlas.js"></script>'

changed = 0
for page in ROOT.rglob("*.html"):
    if "node_modules" in page.parts:
        continue
    text = page.read_text(encoding="utf-8", errors="ignore")
    if CSS in text:
        continue
    if "</head>" not in text or "</body>" not in text:
        continue
    text = text.replace("</head>", f"\t{CSS}\n</head>", 1)
    text = text.replace("</body>", f"\t{JS}\n</body>", 1)
    text = text.replace('content="#006bc4"', 'content="#0b0f14"')
    if page.name in ("index.html",):
        text = text.replace("<title>5etools</title>", "<title>5E ATLAS — D&D reference</title>")
    page.write_text(text, encoding="utf-8")
    changed += 1
print("pagine aggiornate:", changed)
