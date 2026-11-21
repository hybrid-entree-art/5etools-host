#!/usr/bin/env python3
"""Build the compact 2024 core dataset used by the UX prototype.

Source: the JSON shipped with the self-hosted 5e.tools repository.
Only XPHB / XDMG / XMM records are exported.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT.parents[2] / "5etools-host" / "data"
OUT = ROOT / "data" / "core-2024.json"

RE_TAG = re.compile(r"\{@([a-zA-Z]+)(?:\s+([^}]+))?\}")
SCHOOLS = {
    "A": "Abiurazione", "C": "Evocazione", "D": "Divinazione", "E": "Ammaliamento",
    "I": "Illusione", "N": "Negromanzia", "T": "Trasmutazione", "V": "Evocazione",
}
SIZES = {"T": "Minuscola", "S": "Piccola", "M": "Media", "L": "Grande", "H": "Enorme", "G": "Mastodontica"}
RARITY = {
    "none": "Comune", "common": "Comune", "uncommon": "Non comune", "rare": "Raro",
    "very rare": "Molto raro", "legendary": "Leggendario", "artifact": "Artefatto",
    "varied": "Variabile", "unknown": "Sconosciuta",
}
ITEM_TYPES = {
    "M": "Arma da mischia", "R": "Arma a distanza", "A": "Munizioni", "LA": "Armatura leggera",
    "MA": "Armatura media", "HA": "Armatura pesante", "S": "Scudo", "RD": "Bacchetta",
    "WD": "Bacchetta", "RG": "Anello", "P": "Pozione", "SC": "Pergamena", "W": "Oggetto prodigioso",
    "ST": "Bastone", "T": "Strumento", "GS": "Set da gioco", "INS": "Strumento musicale",
    "AT": "Oggetto d'arte", "G": "Equipaggiamento", "PACK": "Pacchetto", "OTH": "Altro",
}
FEAT_CATS = {"O": "Origine", "G": "Generale", "F": "Combattimento", "S": "Stile", "EB": "Epico", "R": "Razziale"}
ABILITIES = {"str": "Forza", "dex": "Destrezza", "con": "Costituzione", "int": "Intelligenza", "wis": "Saggezza", "cha": "Carisma"}
MONSTER_TYPES = {
    "aberration": "Aberrazione", "beast": "Bestia", "celestial": "Celeste", "construct": "Costrutto",
    "dragon": "Drago", "elemental": "Elementale", "fey": "Folletto", "fiend": "Immondo",
    "giant": "Gigante", "humanoid": "Umanoide", "monstrosity": "Mostruosità", "ooze": "Melma",
    "plant": "Pianta", "undead": "Non morto",
}


def load(rel: str):
    return json.loads((DATA / rel).read_text())


ATK = {
    "mw": "Attacco con arma da mischia", "rw": "Attacco con arma a distanza",
    "ms": "Attacco con incantesimo da mischia", "rs": "Attacco con incantesimo a distanza",
    "m": "Attacco con arma da mischia", "r": "Attacco con arma a distanza",
}


def tag_repl(m) -> str:
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
    if tag in ("damage", "dice", "scaledamage", "scaledice", "recharge"):
        return first
    return first


def clean(value) -> str:
    if value is None:
        return ""
    text = str(value)
    text = RE_TAG.sub(tag_repl, text)
    text = text.replace("—", "—").replace("’", "’").replace("[Area of Effect]", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def flat(entries) -> str:
    """Flatten 5e.tools entries into readable paragraphs."""
    if entries is None:
        return ""
    if isinstance(entries, str):
        return clean(entries)
    if isinstance(entries, list):
        return "\n\n".join(x for x in (flat(e) for e in entries) if x)
    if not isinstance(entries, dict):
        return clean(entries)
    e = entries
    if "entries" in e:
        body = flat(e["entries"])
        name = clean(e.get("name"))
        return f"{name}. {body}".strip() if name and body and not body.startswith(name) else body
    if "items" in e:
        return "\n".join(flat(x) for x in e["items"] if flat(x))
    if "entry" in e:
        return flat(e["entry"])
    if "rows" in e:
        rows = []
        for row in e["rows"]:
            rows.append(" | ".join(clean(c) for c in row))
        return "\n".join(rows)
    return clean(e.get("name") or e.get("caption") or "")


def fmt_time(t) -> str:
    if not isinstance(t, list) or not t:
        return ""
    parts = []
    for x in t:
        n = x.get("number", 1)
        unit = {"action": "azione", "bonus": "azione bonus", "reaction": "reazione",
                "minute": "minuto", "hour": "ora", "round": "round"}.get(x.get("unit"), x.get("unit", ""))
        parts.append(f"{n} {unit}")
    return ", ".join(parts)


def fmt_range(r) -> str:
    if not isinstance(r, dict):
        return ""
    if r.get("type") == "special":
        return "Speciale"
    dist = r.get("distance") or {}
    unit = {"feet": "piedi", "miles": "miglia", "self": "te stesso", "touch": "contatto"}.get(dist.get("type"), dist.get("type", ""))
    amount = dist.get("amount")
    return f"{amount} {unit}" if amount else unit


def fmt_duration(d) -> str:
    if not isinstance(d, list) or not d:
        return ""
    out = []
    for x in d:
        if x.get("type") == "instant":
            out.append("Istantanea")
        elif x.get("type") == "permanent":
            out.append("Permanente")
        elif x.get("type") == "special":
            out.append("Speciale")
        elif x.get("type") == "timed":
            dur = x.get("duration") or {}
            amount = dur.get("amount", "")
            unit = {"minute": "minuti", "hour": "ore", "round": "round", "day": "giorni"}.get(dur.get("type"), dur.get("type", ""))
            out.append(f"{amount} {unit}".strip())
    text = ", ".join(out)
    if any(x.get("concentration") for x in d):
        text += ", concentrazione"
    return text


def comps(c) -> str:
    if not isinstance(c, dict):
        return ""
    out = [k.upper() for k in ("v", "s", "m") if c.get(k)]
    return ", ".join(out)


def cr_value(cr) -> str:
    if isinstance(cr, dict):
        return str(cr.get("cr", ""))
    return str(cr or "")


def ac_value(ac) -> str:
    if isinstance(ac, list):
        return ", ".join(str(x) for x in ac)
    if isinstance(ac, dict):
        return str(ac.get("ac", ""))
    return str(ac or "")


def hp_value(hp) -> str:
    if isinstance(hp, dict):
        if hp.get("average"):
            return f"{hp['average']} ({hp.get('formula', '')})".strip()
        return clean(hp.get("special", ""))
    return str(hp or "")


def speed_value(speed) -> str:
    if isinstance(speed, str):
        return speed
    if not isinstance(speed, dict):
        return ""
    out = []
    for k, v in speed.items():
        if k in ("canHover",):
            continue
        if isinstance(v, dict):
            out.append(f"{k} {v.get('number', '')} {v.get('condition', '')}".strip())
        else:
            out.append(f"{k} {v}")
    return ", ".join(out)


def make_spell(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "level": x.get("level", 0),
        "school": SCHOOLS.get(x.get("school", ""), x.get("school", "")),
        "schoolCode": x.get("school", ""), "time": fmt_time(x.get("time")),
        "range": fmt_range(x.get("range")), "components": comps(x.get("components")),
        "duration": fmt_duration(x.get("duration")),
        "entries": flat(x.get("entries")), "higher": flat(x.get("entriesHigherLevel")),
        "classes": x.get("classes") or [],
    }


def make_monster(x):
    traits = x.get("trait") or []
    actions = x.get("action") or []
    bonus = x.get("bonus") or []
    reactions = x.get("reaction") or []
    text = flat(traits + actions + bonus + reactions)
    sizes = "/".join(SIZES.get(s, s) for s in (x.get("size") or []))
    return {
        "name": x["name"], "source": x.get("source", "XMM"), "size": sizes,
        "type": MONSTER_TYPES.get(str(x.get("type", "")).lower(), clean(x.get("type", ""))), "cr": cr_value(x.get("cr")),
        "ac": ac_value(x.get("ac")), "hp": hp_value(x.get("hp")), "speed": speed_value(x.get("speed")),
        "entries": text,
        "abilities": {k.upper(): x.get(k) for k in ("str", "dex", "con", "int", "wis", "cha") if x.get(k) is not None},
    }


def make_item(x):
    raw_type = x.get("type", "").split("|")[0]
    return {
        "name": x["name"], "source": x.get("source", "XDMG"), "type": ITEM_TYPES.get(raw_type, raw_type),
        "typeCode": raw_type, "rarity": RARITY.get(x.get("rarity", ""), x.get("rarity", "")),
        "attune": clean(x.get("reqAttune", "")), "weight": x.get("weight"),
        "entries": flat(x.get("entries")),
    }


def make_class(x):
    hd = x.get("hd") or {}
    prim = []
    for group in x.get("primaryAbility") or []:
        for k, v in group.items():
            if v:
                prim.append(ABILITIES.get(k, k))
    text = flat(x.get("classFeatures") or [])
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "hitDie": f"d{hd.get('faces', '?')}" if hd else "",
        "primary": ", ".join(prim), "caster": ABILITIES.get(x.get("spellcastingAbility", ""), ""),
        "entries": text,
    }


def make_subclass(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "className": x.get("className", ""),
        "entries": flat(x.get("subclassFeatures") or []),
    }


def make_feat(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "category": FEAT_CATS.get(x.get("category", ""), x.get("category", "")),
        "prerequisite": flat(x.get("prerequisite")),
        "entries": flat(x.get("entries")),
    }


def make_background(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "entries": flat(x.get("entries")),
    }


def make_species(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "types": ", ".join(clean(t) for t in (x.get("creatureTypes") or [])),
        "size": "/".join(SIZES.get(s, s) for s in (x.get("size") or [])),
        "speed": str(x.get("speed", "")), "darkvision": x.get("darkvision"),
        "resist": ", ".join(clean(r) for r in (x.get("resist") or [])),
        "entries": flat(x.get("entries")),
    }


def make_bastion(x):
    return {
        "name": x["name"], "source": x.get("source", "XDMG"),
        "facilityType": x.get("facilityType", ""), "level": x.get("level"),
        "space": ", ".join(clean(s) for s in (x.get("space") or [])),
        "entries": flat(x.get("entries")),
    }


def make_glossary(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "ruleType": x.get("ruleType", ""), "entries": flat(x.get("entries")),
    }


def main():
    spells = [make_spell(x) for x in load("spells/spells-xphb.json").get("spell", []) if x.get("source") == "XPHB"]
    monsters = []
    for f in sorted((DATA / "bestiary").glob("bestiary-*.json")):
        monsters += [make_monster(x) for x in json.loads(f.read_text()).get("monster", []) if x.get("source") in ("XMM", "XDMG")]
    items = load("items.json").get("item", [])
    magic = [make_item(x) for x in items if x.get("source") == "XDMG"]
    equipment = [make_item(x) for x in items if x.get("source") == "XPHB"]
    classes = []
    subclasses = []
    for f in sorted((DATA / "class").glob("class-*.json")):
        d = json.loads(f.read_text())
        classes += [make_class(x) for x in d.get("class", []) if x.get("source") == "XPHB"]
        subclasses += [make_subclass(x) for x in d.get("subclass", []) if x.get("source") == "XPHB"]
    feats = [make_feat(x) for x in load("feats.json").get("feat", []) if x.get("source") == "XPHB"]
    backgrounds = [make_background(x) for x in load("backgrounds.json").get("background", []) if x.get("source") == "XPHB"]
    species = [make_species(x) for x in load("races.json").get("race", []) if x.get("source") == "XPHB"]
    bastions = [make_bastion(x) for x in load("bastions.json").get("facility", []) if x.get("source") == "XDMG"]
    glossary = [make_glossary(x) for x in load("variantrules.json").get("variantrule", []) if x.get("source") == "XPHB"]

    categories = [
        ("spells", "Incantesimi", spells),
        ("monsters", "Mostri", monsters),
        ("magic-items", "Oggetti magici", magic),
        ("equipment", "Equipaggiamento", equipment),
        ("classes", "Classi", classes),
        ("subclasses", "Sottoclassi", subclasses),
        ("feats", "Talenti", feats),
        ("backgrounds", "Background", backgrounds),
        ("species", "Specie", species),
        ("bastions", "Bastioni", bastions),
        ("glossary", "Glossario", glossary),
    ]
    payload = {
        "edition": "2024",
        "books": [
            {"code": "XPHB", "title": "Player's Handbook", "it": "Manuale del Giocatore"},
            {"code": "XDMG", "title": "Dungeon Master's Guide", "it": "Manuale del Dungeon Master"},
            {"code": "XMM", "title": "Monster Manual", "it": "Manuale dei Mostri"},
        ],
        "categories": {key: {"label": label, "count": len(rows), "items": rows} for key, label, rows in categories},
        "total": sum(len(rows) for _, _, rows in categories),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    for key, label, rows in categories:
        print(f"{label:18} {len(rows):4}")
    print(f"{'TOTALE':18} {payload['total']:4}  {OUT.stat().st_size/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
