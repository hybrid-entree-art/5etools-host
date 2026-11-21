#!/usr/bin/env python3
"""Build a normalized, reader-friendly version of the three 2024 core books."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "data" / "core-2024.json"
DATA = ROOT.parents[2] / "5etools-host" / "data"
OUT = ROOT / "data" / "books-2024.json"

RE_TAG = re.compile(r"\{@([a-zA-Z]+)(?:\s+([^}]+))?\}")
ATK = {
    "mw": "Attacco con arma da mischia", "rw": "Attacco con arma a distanza",
    "ms": "Attacco con incantesimo da mischia", "rs": "Attacco con incantesimo a distanza",
    "m": "Attacco con arma da mischia", "r": "Attacco con arma a distanza",
}
BOOKS = {
    "XPHB": ("Player's Handbook", "Manuale del Giocatore"),
    "XDMG": ("Dungeon Master's Guide", "Manuale del Master"),
    "XMM": ("Monster Manual", "Manuale dei Mostri"),
}


def tag_repl(m):
    tag = m.group(1).lower()
    body = (m.group(2) or "").strip()
    first = body.split("|")[0].strip()
    if tag in ("atk", "atkr"):
        return " / ".join(ATK.get(x.strip(), x.strip()) for x in first.split(",") if x.strip()) + ":"
    if tag == "h":
        return "Colpo:"
    if tag == "hit":
        return f"+{first}" if not first.startswith("+") else first
    if tag == "dc":
        return f"CD {first}"
    if tag == "chance":
        return f"{first}%"
    return first


def clean(value):
    if value is None:
        return ""
    text = RE_TAG.sub(tag_repl, str(value)).replace("[Area of Effect]", "")
    return re.sub(r"\s+", " ", text).strip()


def block(entry):
    if isinstance(entry, str):
        return {"t": "p", "v": clean(entry)}
    if isinstance(entry, list):
        return {"t": "group", "items": [b for b in (block(x) for x in entry) if b]}
    if not isinstance(entry, dict):
        return {"t": "p", "v": clean(entry)}
    typ = entry.get("type")
    name = clean(entry.get("name"))
    if typ == "statblock":
        yield_ref = {"name": entry.get("name"), "tag": entry.get("tag"), "source": entry.get("source")}
        return {"t": "ref", **yield_ref}
    if typ in ("image", "gallery", "abilityAttackMod", "abilityDc", "abilityGeneric"):
        return None
    if typ == "table":
        labels = [clean(x) for x in (entry.get("colLabels") or [])]
        rows = []
        for row in entry.get("rows") or []:
            rows.append([clean(c) for c in row])
        if not rows:
            return None
        return {"t": "table", "name": name, "head": labels, "rows": rows}
    if typ in ("list", "list-hang-notitle"):
        items = []
        for item in entry.get("items") or []:
            if isinstance(item, dict):
                label = clean(item.get("name"))
                body = block(item.get("entry") or item.get("entries"))
                text = label + (": " + body.get("v", "") if body and body.get("v") else "")
                items.append(text.strip())
            else:
                b = block(item)
                if b and b.get("v"):
                    items.append(b["v"])
        return {"t": "list", "items": [x for x in items if x]}
    if typ in ("inset", "quote", "callout", "variant"):
        items = [b for b in (block(x) for x in (entry.get("entries") or [])) if b]
        return {"t": "note", "name": name, "items": items}
    if typ in ("section", "entries", "homebrew", "spellcasting", "classFeature", "subclassFeature"):
        items = [b for b in (block(x) for x in (entry.get("entries") or [])) if b]
        return {"t": "section", "name": name, "id": entry.get("id"), "items": items}
    if "entries" in entry:
        items = [b for b in (block(x) for x in (entry.get("entries") or [])) if b]
        return {"t": "section", "name": name, "id": entry.get("id"), "items": items}
    if "entry" in entry:
        return block(entry.get("entry"))
    return {"t": "p", "v": clean(entry.get("name") or entry.get("caption") or "")}


def chapter(x):
    items = [b for b in (block(e) for e in (x.get("entries") or [])) if b]
    return {"id": x.get("id"), "name": clean(x.get("name")), "page": x.get("page"), "items": items}



TARGETS = {
    "XPHB": {
        "Chapter 3: Character Classes": ["classes", "subclasses"],
        "Chapter 4: Character Origins": ["backgrounds", "species"],
        "Chapter 5: Feats": ["feats"],
        "Chapter 6: Equipment": ["equipment"],
        "Chapter 7: Spells": ["spells"],
        "Rules Glossary": ["glossary"],
    },
    "XDMG": {
        "Chapter 7: Treasure": ["magic-items"],
        "Chapter 8: Bastions": ["bastions"],
    },
    "XMM": {
        "Monsters A to Z": ["monsters"],
    },
}


def dedupe_refs(node, seen):
    if isinstance(node, dict):
        if node.get("t") == "ref" and node.get("cat") is not None:
            key = (node["cat"], node["idx"])
            if key in seen:
                return None
            seen.add(key)
        if isinstance(node.get("items"), list):
            node["items"] = [x for x in (dedupe_refs(v, seen) for v in node["items"]) if x is not None]
    elif isinstance(node, list):
        for x in node:
            dedupe_refs(x, seen)
    return node


def ensure_category(chapter, cats, core):
    seen = set()
    dedupe_refs(chapter["items"], seen)
    for cat in cats:
        have = {idx for c, idx in seen if c == cat}
        missing = [i for i in range(core["categories"][cat]["count"]) if i not in have]
        if not missing:
            continue
        chapter["items"].append({
            "t": "section",
            "name": "Indice completo · " + core["categories"][cat]["label"],
            "items": [{"t": "ref", "name": core["categories"][cat]["items"][i]["name"],
                       "tag": cat, "source": core["categories"][cat]["items"][i].get("source"),
                       "cat": cat, "idx": i} for i in missing],
        })
        seen.update((cat, i) for i in missing)

def main():
    core = json.loads(CORE.read_text())
    refs = {}
    for cat, c in core["categories"].items():
        for idx, item in enumerate(c["items"]):
            refs[(item["name"], item.get("source"))] = {"category": cat, "index": idx}
            refs.setdefault((item["name"], None), {"category": cat, "index": idx})

    books = {}
    for code, (title, it) in BOOKS.items():
        raw = json.loads((DATA / "book" / f"book-{code.lower()}.json").read_text())["bookData"][0]["data"]
        chapters = [chapter(x) for x in raw if x.get("type") == "section"]
        # Resolve statblock references against the compendium indexes first.
        def resolve(node):
            if isinstance(node, list):
                for x in node:
                    resolve(x)
            elif isinstance(node, dict):
                if node.get("t") == "ref":
                    hit = refs.get((node.get("name"), node.get("source"))) or refs.get((node.get("name"), None))
                    if hit:
                        node["cat"] = hit["category"]
                        node["idx"] = hit["index"]
                for key in ("items",):
                    if isinstance(node.get(key), list):
                        resolve(node[key])
        resolve(chapters)
        for ch in chapters:
            targets = TARGETS.get(code, {}).get(ch["name"])
            if targets:
                ensure_category(ch, targets, core)
        books[code] = {"code": code, "title": title, "it": it, "chapters": chapters}
        print(code, len(chapters), "chapters", len(json.dumps(chapters)) // 1024, "KB")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"books": books}, ensure_ascii=False, separators=(",", ":")))
    print("total", OUT.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
