#!/usr/bin/env python3
"""Sottoinsieme curato di immagini per la UX ATLAS (WebP leggere)."""
import io, os, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/art"
UA = {"User-Agent": "Mozilla/5.0 (compatible; atlas-assets/1.0)"}
SOURCES = {
    "cover-xphb.webp": "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/main/covers/XPHB.webp",
    "cover-xdmg.webp": "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/main/covers/XDMG.webp",
    "cover-xmm.webp": "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/main/covers/XMM.webp",
    "hero.webp": "https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/main/book/XPHB/000-01-013.opening-art.webp",
}
CATS = ["sources", "classes", "backgrounds", "species", "feats", "spells",
        "equipment", "magic-items", "monsters", "bastions", "glossary"]
for c in CATS:
    SOURCES[f"cat-{c}.webp"] = f"https://media.ruleholder.com/images/menu/{c}.webp"
    SOURCES[f"cat-{c}-bg.webp"] = f"https://media.ruleholder.com/images/menu/{c}-bg.webp"

def save(name, data, max_w, max_h):
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    if im.width > max_w or im.height > max_h:
        im.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    path = f"{OUT}/{name}"
    im.save(path, "WEBP", quality=76, method=6)
    return os.path.getsize(path)

def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, url in SOURCES.items():
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
            is_bg = name.endswith("-bg.webp")
            is_cover = name.startswith("cover-")
            total += save(name, data, 800 if is_bg else (420 if is_cover else 1200),
                          520 if is_bg else (620 if is_cover else 700))
            print("[OK]", name)
        except Exception as exc:
            print("[FAIL]", name, exc)
    print("totale KB:", total // 1024)

if __name__ == "__main__":
    main()
