#!/usr/bin/env python3
"""Inietta il tema ATLAS nelle pagine del self-host 5e.tools."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = '<link rel="stylesheet" href="/atlas-theme.css">'

changed = 0
for page in ROOT.rglob("*.html"):
    if "node_modules" in page.parts or "atlas-theme" in page.name:
        continue
    text = page.read_text(encoding="utf-8", errors="ignore")
    if LINK in text:
        continue
    # Inserisce dopo l'ultimo stylesheet esistente nel <head>, o prima di </head>.
    if "</head>" in text:
        text = text.replace("</head>", f"\t{LINK}\n</head>", 1)
    else:
        continue
    text = text.replace('content="#006bc4"', 'content="#0b0f14"')
    page.write_text(text, encoding="utf-8")
    changed += 1
print(f"pagine aggiornate: {changed}")
