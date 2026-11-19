#!/usr/bin/env python3
"""Font self-hosted per la UX ATLAS."""
import os, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/fonts"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

RULEHOLDER = [
    ("modesto.woff2", "https://ruleholder.com/fonts/modesto/modesto.woff2"),
    ("modesto-condensed.woff2", "https://ruleholder.com/fonts/modesto-condensed/modesto-condensed.woff2"),
    ("modesto-condensed-bold.woff2", "https://ruleholder.com/fonts/modesto-condensed/modesto-condensed-bold.woff2"),
    ("mulish.woff2", "https://ruleholder.com/fonts/mulish/mulish-400-800-latin.woff2"),
]

def google_font(name, css_url):
    css = urllib.request.urlopen(urllib.request.Request(css_url, headers=UA), timeout=30).read().decode()
    for block in css.split("/*"):
        if block.strip().startswith("latin */"):
            m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
            if m:
                return urllib.request.urlopen(m.group(1), timeout=30).read()
    raise RuntimeError(f"woff2 non trovato per {name}")

def main():
    os.makedirs(OUT, exist_ok=True)
    for name, url in RULEHOLDER:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read()
        open(f"{OUT}/{name}", "wb").write(data)
        print("[OK]", name, len(data))
    for name, url in [("space-grotesk.woff2", "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap"),
                      ("lora.woff2", "https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&display=swap")]:
        data = google_font(name, url)
        open(f"{OUT}/{name}", "wb").write(data)
        print("[OK]", name, len(data))

if __name__ == "__main__":
    main()
