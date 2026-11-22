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
    "I": "Illusione", "N": "Negromanzia", "T": "Trasmutazione", "V": "Invocazione",
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
SAVES = {"str": "Forza", "dex": "Destrezza", "con": "Costituzione", "int": "Intelligenza", "wis": "Saggezza", "cha": "Carisma", "dexterity": "Destrezza", "constitution": "Costituzione", "wisdom": "Saggezza", "intelligence": "Intelligenza", "strength": "Forza", "charisma": "Carisma"}
DMG_ELEMENTS = {
    "acid": "Acido", "bludgeoning": "Contundente", "cold": "Freddo", "fire": "Fuoco",
    "force": "Forza", "lightning": "Fulmine", "necrotic": "Necrotico", "piercing": "Perforante",
    "poison": "Veleno", "psychic": "Psichico", "radiant": "Radiante", "slashing": "Tagliente",
    "thunder": "Tuono", "healing": "Cura",
}
ATTACKS = {"R": "Attacco a distanza", "M": "Attacco in mischia"}
DMG_TYPES = {"S": "Tagliente", "P": "Perforante", "B": "Contundente"}
PROPS = {
    "V": "Versatile", "T": "A due mani", "F": "Finezza", "L": "Leggera", "H": "Pesante",
    "R": "Portata", "T": "A due mani", "TH": "Lancio", "A": "Munizioni", "LD": "Ricarica",
    "S": "Speciale", "2H": "A due mani", "1H": "A una mano",
}
FEAT_CATS = {"O": "Origine", "G": "Generale", "F": "Combattimento", "S": "Stile", "EB": "Epico", "R": "Razziale"}
ABILITIES = {"str": "Forza", "dex": "Destrezza", "con": "Costituzione", "int": "Intelligenza", "wis": "Saggezza", "cha": "Carisma"}
TYPE_TAGS = {"chromatic": "cromatico", "metallic": "metallico", "shapechanger": "mutaforma", "any": "qualsiasi"}
MONSTER_TYPES = {
    "aberration": "Aberrazione", "beast": "Bestia", "celestial": "Celeste", "construct": "Costrutto",
    "dragon": "Drago", "elemental": "Elementale", "fey": "Folletto", "fiend": "Immondo",
    "giant": "Gigante", "humanoid": "Umanoide", "monstrosity": "Mostruosità", "ooze": "Melma",
    "plant": "Pianta", "undead": "Non morto",
}


def load(rel: str):
    return json.loads((DATA / rel).read_text())


ATK = {
    "mw": "Melee Weapon Attack", "rw": "Ranged Weapon Attack",
    "ms": "Melee Spell Attack", "rs": "Ranged Spell Attack",
    "m": "Melee Weapon Attack", "r": "Ranged Weapon Attack",
}


def tag_repl(m) -> str:
    tag = m.group(1).lower()
    body = (m.group(2) or "").strip()
    first = body.split("|")[0].strip()
    if tag in ("atk", "atkr"):
        return " / ".join(ATK.get(x.strip(), x.strip()) for x in first.split(",") if x.strip()) + ":"
    if tag == "h":
        return "Hit: "
    if tag == "hit":
        return f"+{first}" if not first.startswith("+") else first
    if tag == "dc":
        return f"DC {first}"
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
    return ", ".join(out)


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


SPEED_IT = {"walk": "Cammina", "fly": "Vola", "swim": "Nuota", "burrow": "Scava", "climb": "Arrampica"}
SKILL_IT = {
    "acrobatics": "Acrobazia", "animal handling": "Addestrare animali", "arcana": "Arcano",
    "athletics": "Atletica", "deception": "Inganno", "history": "Storia", "insight": "Intuizione",
    "intimidation": "Intimidire", "investigation": "Indagare", "medicine": "Medicina",
    "nature": "Natura", "perception": "Percezione", "performance": "Intrattenere",
    "persuasion": "Persuasione", "religion": "Religione", "sleight of hand": "Rapidità di mano",
    "stealth": "Furtività", "survival": "Sopravvivenza",
}
SENSE_IT = {"darkvision": "Scurovisione", "blindsight": "Vista cieca", "tremorsense": "Percezione tellurica", "truesight": "Vista vera"}
COND_IT = {
    "blinded": "Accecato", "charmed": "Affascinato", "deafened": "Assordato", "exhaustion": "Affaticamento",
    "frightened": "Spaventato", "grappled": "Afferrato", "incapacitated": "Incapacitato", "invisible": "Invisibile",
    "paralyzed": "Paralizzato", "petrified": "Pietrificato", "poisoned": "Avvelenato", "prone": "Prono",
    "restrained": "Trattenuto", "stunned": "Stordito", "unconscious": "Incosciente",
}
LANG_IT = {"common": "Comune", "draconic": "Draconico", "deep speech": "Parlata profonda", "elvish": "Elfico", "dwarvish": "Nanico", "infernal": "Infernale", "celestial": "Celestiale", "abyssal": "Abissale", "undercommon": "Comune sotterraneo"}


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
            out.append(f"{SPEED_IT.get(k, k)} {v.get('number', '')} {v.get('condition', '')}".strip())
        else:
            out.append(f"{SPEED_IT.get(k, k)} {v}")
    return ", ".join(out)


def make_spell(x, source_lookup=None):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "level": x.get("level", 0),
        "school": SCHOOLS.get(x.get("school", ""), x.get("school", "")),
        "schoolCode": x.get("school", ""), "time": fmt_time(x.get("time")),
        "range": fmt_range(x.get("range")), "components": comps(x.get("components")),
        "duration": fmt_duration(x.get("duration")),
        "save": ", ".join(SAVES.get(v, v) for v in (x.get("savingThrow") or [])),
        "damage": ", ".join(DMG_ELEMENTS.get(v, v) for v in (x.get("damageInflict") or [])),
        "attack": ", ".join(ATTACKS.get(v, v) for v in (x.get("spellAttack") or [])),
        "ritual": bool((x.get("meta") or {}).get("ritual")),
        "concentration": any(d.get("concentration") for d in (x.get("duration") or [])),
        "area": ", ".join(x.get("areaTags") or []),
        "entries": flat(x.get("entries")), "higher": flat(x.get("entriesHigherLevel")),
        "classes": sorted((((source_lookup or {}).get("xphb", {}).get(x["name"].lower(), {}) or {}).get("class", {}) or {}).get("XPHB", {}) or []),
    }


def fmt_lang(value):
    text = clean(value).replace("ft.", "piedi").replace("telepathy", "telepatia")
    for en, it in LANG_IT.items():
        text = re.sub(r"\b" + re.escape(en) + r"\b", it, text, flags=re.I)
    return text


def fmt_damage_list(values):
    out = []
    for v in values or []:
        if isinstance(v, dict):
            out.append(clean(v.get("special") or v.get("type") or v.get("note") or "Speciale"))
        else:
            out.append(DMG_ELEMENTS.get(v, v))
    return ", ".join(out)


def make_monster(x):
    traits = x.get("trait") or []
    actions = x.get("action") or []
    bonus = x.get("bonus") or []
    reactions = x.get("reaction") or []
    legendary_actions = x.get("legendary") or []
    sections = []
    for label, rows in (("Tratti", traits), ("Azioni", actions), ("Azioni bonus", bonus),
                        ("Reazioni", reactions), ("Azioni leggendarie", legendary_actions)):
        items = [{"name": clean(r.get("name", "")), "entries": flat(r.get("entries") or r.get("entry"))} for r in rows]
        items = [i for i in items if i["name"] or i["entries"]]
        if items:
            sections.append({"label": label, "items": items})
    text = "\n\n".join(f"{i['name']}. {i['entries']}" for sec in sections for i in sec["items"])
    sizes = "/".join(SIZES.get(s, s) for s in (x.get("size") or []))
    raw_type = x.get("type", "")
    if isinstance(raw_type, dict):
        base_type = raw_type.get("type", "")
        tags = raw_type.get("tags") or []
        type_label = MONSTER_TYPES.get(str(base_type).lower(), clean(base_type))
        if tags:
            type_label += " (" + ", ".join(TYPE_TAGS.get(str(t).lower(), clean(t)) for t in tags) + ")"
    else:
        type_label = MONSTER_TYPES.get(str(raw_type).lower(), clean(raw_type))
    return {
        "name": x["name"], "source": x.get("source", "XMM"), "size": sizes,
        "type": type_label, "cr": cr_value(x.get("cr")),
        "ac": ac_value(x.get("ac")), "hp": hp_value(x.get("hp")), "speed": speed_value(x.get("speed")),
        "entries": text, "sections": sections,
        "abilities": {k.upper(): x.get(k) for k in ("str", "dex", "con", "int", "wis", "cha") if x.get(k) is not None},
        "saves": ", ".join(f"{ABILITIES.get(k, k)} {v}" for k, v in (x.get("save") or {}).items()),
        "skills": ", ".join(f"{SKILL_IT.get(k.lower(), k.title())} {v}" for k, v in (x.get("skill") or {}).items()),
        "senses": ", ".join(clean(v).replace("ft.", "piedi") for v in (x.get("senses") or [])).replace("Darkvision", "Scurovisione").replace("Blindsight", "Vista cieca").replace("Tremorsense", "Percezione tellurica").replace("Truesight", "Vista vera") + (f" · passivo {x.get('passive')}" if x.get("passive") else ""),
        "languages": ", ".join(fmt_lang(v) for v in (x.get("languages") or [])),
        "resist": fmt_damage_list(x.get("resist")),
        "immune": fmt_damage_list(x.get("immune")),
        "conditionImmune": ", ".join(COND_IT.get(str(v).lower(), clean(v)) for v in (x.get("conditionImmune") or [])),
    }


def make_variant(x):
    inh = x.get("inherits") or {}
    return {
        "name": x["name"], "source": "XDMG", "type": "Variante", "typeCode": "GV",
        "rarity": RARITY.get(inh.get("rarity", ""), inh.get("rarity", "")),
        "attune": clean(inh.get("reqAttune", "")), "weight": inh.get("weight"),
        "entries": flat(inh.get("entries")),
    }


def make_item(x):
    raw_type = x.get("type", "").split("|")[0]
    return {
        "name": x["name"], "source": x.get("source", "XDMG"), "type": ITEM_TYPES.get(raw_type, raw_type),
        "typeCode": raw_type, "rarity": RARITY.get(x.get("rarity", ""), x.get("rarity", "")),
        "attune": clean(x.get("reqAttune", "")), "weight": x.get("weight"),
        "damage": (f"{x.get('dmg1', '')} {DMG_TYPES.get(x.get('dmgType', ''), x.get('dmgType', ''))}".strip() if x.get("dmg1") else ""),
        "properties": ", ".join(PROPS.get(str(v).split("|")[0], str(v).split("|")[0]) for v in (x.get("property") or [])),
        "mastery": ", ".join(str(v).split("|")[0] for v in (x.get("mastery") or [])),
        "ac": x.get("ac"), "strength": x.get("strength"), "stealth": x.get("stealth"),
        "weaponCategory": x.get("weaponCategory", ""),
        "entries": flat(x.get("entries")),
    }


def make_class(x, image="", feature_map=None):
    hd = x.get("hd") or {}
    prim = []
    for group in x.get("primaryAbility") or []:
        for k, v in group.items():
            if v:
                prim.append(ABILITIES.get(k, k))
    features = []
    for raw in x.get("classFeatures") or []:
        name = raw.get("classFeature", "") if isinstance(raw, dict) else raw
        parts = name.split("|")
        fname = parts[0].strip()
        f = (feature_map or {}).get((fname, x["name"])) or (feature_map or {}).get((fname, None))
        if f:
            features.append({"name": f["name"], "level": f.get("level"), "entries": flat(f.get("entries"))})
    text = "\n\n".join(f"{f['name']} (Livello {f['level']}): {f['entries']}" for f in features)
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "image": image,
        "hitDie": f"d{hd.get('faces', '?')}" if hd else "",
        "primary": ", ".join(prim), "caster": ABILITIES.get(x.get("spellcastingAbility", ""), ""),
        "entries": text, "features": features,
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


def make_species(x, image=""):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "image": image,
        "types": ", ".join(MONSTER_TYPES.get(str(t).lower(), clean(t)) for t in (x.get("creatureTypes") or [])),
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


def make_rule(x, kind):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"),
        "ruleType": kind, "entries": flat(x.get("entries")),
    }


FEATURE_TYPES = {"EI": "Invocazione occulta", "MV:B": "Manovra", "MM": "Metamagica"}


def make_optional(x):
    types = [FEATURE_TYPES.get(t, t) for t in (x.get("featureType") or [])]
    label = ", ".join(types) or "Opzione di classe"
    prereq = flat(x.get("prerequisite"))
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "typeLabel": label,
        "prerequisite": prereq, "entries": flat(x.get("entries")),
        "subtitle": label, "meta": label,
        "tags": [{"text": label, "tide": True}],
        "stats": [["Tipo", label], ["Prerequisito", prereq]],
    }


def make_language(x):
    kind = {"standard": "Standard", "rare": "Rara"}.get(x.get("type"), "Lingua")
    speakers = ", ".join(clean(v) for v in (x.get("typicalSpeakers") or []))
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "typeLabel": kind,
        "entries": flat(x.get("entries")), "subtitle": kind, "meta": kind,
        "tags": [{"text": kind, "tide": True}],
        "stats": [["Tipo", kind], ["Parlanti", speakers]],
    }


def make_deity(x):
    return {
        "name": x["name"], "source": x.get("source", "XDMG"), "pantheon": x.get("pantheon", ""),
        "title": x.get("title", ""), "worshipers": x.get("worshipers", ""),
        "plane": x.get("plane", ""), "symbol": x.get("symbol", ""),
        "entries": flat(x.get("entries")), "subtitle": x.get("pantheon", "Divinità"),
        "meta": x.get("pantheon", ""),
        "tags": [{"text": x.get("pantheon", "Divinità"), "tide": True}],
        "stats": [["Pantheon", x.get("pantheon", "")], ["Titolo", x.get("title", "")],
                  ["Adoratori", x.get("worshipers", "")], ["Piano", x.get("plane", "")],
                  ["Simbolo", x.get("symbol", "")]],
    }


def make_skill(x):
    ab = ABILITIES.get(x.get("ability", ""), x.get("ability", ""))
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "ability": ab,
        "entries": flat(x.get("entries")), "subtitle": ab, "meta": ab,
        "tags": [{"text": ab, "tide": True}],
        "stats": [["Abilità", ab]],
    }


def make_mastery(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "typeLabel": "Maestria",
        "entries": flat(x.get("entries")), "subtitle": "Maestria", "meta": "Maestria",
        "tags": [{"text": "Maestria", "tide": True}],
        "stats": [["Tipo", "Maestria"]],
    }


def make_property(x):
    entry = (x.get("entries") or [{}])[0]
    name = clean(entry.get("name") or x.get("abbreviation") or "")
    return {
        "name": name, "source": x.get("source", "XPHB"), "typeLabel": "Proprietà",
        "abbreviation": x.get("abbreviation", ""), "entries": flat(x.get("entries")),
        "subtitle": "Proprietà", "meta": "Proprietà",
        "tags": [{"text": "Proprietà", "tide": True}],
        "stats": [["Tipo", "Proprietà"], ["Abbreviazione", x.get("abbreviation", "")]],
    }


def make_treasure(x, kind):
    return {
        "name": x["name"], "source": x.get("source", "XDMG"), "typeLabel": kind,
        "entries": flat(x.get("table") or x.get("entries")), "subtitle": kind, "meta": kind,
        "tags": [{"text": kind, "tide": True}],
        "stats": [["Tipo", kind]],
    }


def make_item_type(x):
    return {
        "name": x["name"], "source": x.get("source", "XPHB"), "typeLabel": "Tipo di oggetto",
        "abbreviation": x.get("abbreviation", ""), "entries": flat(x.get("entries")),
        "subtitle": "Tipo di oggetto", "meta": x.get("abbreviation", "Tipo"),
        "tags": [{"text": "Tipo di oggetto", "tide": True}],
        "stats": [["Tipo", "Tipo di oggetto"], ["Abbreviazione", x.get("abbreviation", "")]],
    }


def make_legendary(x):
    return {
        "name": x["name"], "source": x.get("source", "XMM"), "typeLabel": "Gruppo leggendario",
        "entries": flat(x.get("regionalEffects") or []), "subtitle": "Gruppo leggendario",
        "meta": "Gruppo leggendario",
        "tags": [{"text": "Gruppo leggendario", "tide": True}],
        "stats": [["Tipo", "Gruppo leggendario"]],
    }


def make_card(x):
    return {
        "name": x["name"], "source": x.get("source", "XDMG"), "set": x.get("set", ""),
        "entries": flat(x.get("entries")), "subtitle": x.get("set", "Carta"),
        "meta": x.get("set", "Carta"),
        "tags": [{"text": x.get("set", "Carta"), "tide": True}],
        "stats": [["Mazzo", x.get("set", "")]],
    }


def main():
    spell_lookup = load("generated/gendata-spell-source-lookup.json")
    spells = [make_spell(x, spell_lookup) for x in load("spells/spells-xphb.json").get("spell", []) if x.get("source") == "XPHB"]
    monsters = []
    for f in sorted((DATA / "bestiary").glob("bestiary-*.json")):
        monsters += [make_monster(x) for x in json.loads(f.read_text()).get("monster", []) if x.get("source") in ("XMM", "XDMG")]
    legendary_groups = [x for x in load("bestiary/legendarygroups.json").get("legendaryGroup", []) if x.get("source") == "XMM"]
    for g in legendary_groups:
        info = flat(g.get("regionalEffects") or [])
        if not info:
            continue
        for m in monsters:
            match = m["name"] == g["name"]
            if g["name"].endswith(" Dragon") and m["name"].endswith(g["name"]) and m["name"].split(" ", 1)[0] in ("Adult", "Ancient"):
                match = True
            if match:
                m["legendary"] = {"name": g["name"], "entries": info}
    items = load("items.json").get("item", [])
    magic = [make_item(x) for x in items if x.get("source") == "XDMG"]
    seen_magic = {x["name"] for x in magic}
    for x in load("items-base.json").get("itemEntry", []):
        if x.get("source") == "XDMG" and x["name"] not in seen_magic:
            magic.append(make_item(x))
            seen_magic.add(x["name"])
    for x in load("magicvariants.json").get("magicvariant", []):
        inh = x.get("inherits") or {}
        if any("|XDMG" in s for s in (inh.get("reprintedAs") or [])) and x["name"] not in seen_magic:
            magic.append(make_variant(x))
            seen_magic.add(x["name"])
    equipment = [make_item(x) for x in items if x.get("source") == "XPHB"]
    base = load("items-base.json").get("baseitem", [])
    seen_equipment = {x["name"] for x in equipment}
    for x in load("vehicles.json").get("vehicle", []):
        if x.get("source") == "XDMG" and x["name"] not in seen_equipment:
            equipment.append(make_item(x))
            seen_equipment.add(x["name"])
    for x in base:
        if x.get("source") == "XPHB" and x["name"] not in seen_equipment:
            equipment.append(make_item(x))
            seen_equipment.add(x["name"])
    class_images = {}
    for f in (DATA / "class").glob("fluff-class-*.json"):
        d = json.loads(f.read_text())
        for x in d.get("classFluff", []):
            if x.get("source") == "XPHB" and (x.get("images") or []):
                class_images[x["name"]] = x["images"][0].get("href", {}).get("path", "")
    species_images = {}
    for x in load("fluff-races.json").get("raceFluff", []):
        if x.get("source") == "XPHB" and (x.get("images") or []):
            species_images[x["name"]] = x["images"][0].get("href", {}).get("path", "")
    class_features = {}
    class_files = []
    for f in sorted((DATA / "class").glob("class-*.json")):
        d = json.loads(f.read_text())
        class_files.append(d)
        for x in d.get("classFeature", []):
            key = (x.get("name"), x.get("className"))
            if key not in class_features or x.get("source") == "XPHB":
                class_features[key] = x
    classes = []
    subclasses = []
    for d in class_files:
        classes += [make_class(x, class_images.get(x["name"], ""), class_features) for x in d.get("class", []) if x.get("source") == "XPHB"]
        subclasses += [make_subclass(x) for x in d.get("subclass", []) if x.get("source") == "XPHB"]
    feats = [make_feat(x) for x in load("feats.json").get("feat", []) if x.get("source") == "XPHB"]
    backgrounds = [make_background(x) for x in load("backgrounds.json").get("background", []) if x.get("source") == "XPHB"]
    species = [make_species(x, species_images.get(x["name"], "")) for x in load("races.json").get("race", []) if x.get("source") == "XPHB"]
    bastions = [make_bastion(x) for x in load("bastions.json").get("facility", []) if x.get("source") == "XDMG"]
    class_options = [make_optional(x) for x in load("optionalfeatures.json").get("optionalfeature", []) if x.get("source") == "XPHB"]
    languages = [make_language(x) for x in load("languages.json").get("language", []) if x.get("source") in ("XPHB", "XMM")]
    deities = [make_deity(x) for x in load("deities.json").get("deity", []) if x.get("source") == "XDMG"]
    skills = [make_skill(x) for x in load("skills.json").get("skill", []) if x.get("source") == "XPHB"]
    mastery = [make_mastery(x) for x in load("items-base.json").get("itemMastery", []) if x.get("source") == "XPHB"]
    properties = [make_property(x) for x in load("items-base.json").get("itemProperty", []) if x.get("source") in ("XPHB", "XDMG")]
    loot = load("loot.json")
    treasure = [make_treasure(x, "Gemme") for x in loot.get("gems", []) if x.get("source") == "XDMG"]
    treasure += [make_treasure(x, "Oggetti d'arte") for x in loot.get("artObjects", []) if x.get("source") == "XDMG"]
    cards = [make_card(x) for x in load("decks.json").get("card", []) if x.get("source") == "XDMG"]
    legendary = [make_legendary(x) for x in load("bestiary/legendarygroups.json").get("legendaryGroup", []) if x.get("source") == "XMM"]
    item_types = [make_item_type(x) for x in load("items-base.json").get("itemType", []) if x.get("source") in ("XPHB", "XDMG", "XMM")]
    glossary = [make_glossary(x) for x in load("variantrules.json").get("variantrule", []) if x.get("source") == "XPHB"]
    seen_rules = {(x["name"], x["source"]) for x in glossary}
    for filename, key, label in [
        ("conditionsdiseases.json", "condition", "Condizione"),
        ("conditionsdiseases.json", "status", "Stato"),
        ("conditionsdiseases.json", "disease", "Malattia"),
        ("trapshazards.json", "hazard", "Pericolo"),
        ("trapshazards.json", "trap", "Trappola"),
        ("actions.json", "action", "Azione"),
        ("senses.json", "sense", "Senso"),
        ("objects.json", "object", "Oggetto"),
        ("rewards.json", "reward", "Ricompensa"),
    ]:
        for x in load(filename).get(key, []):
            if x.get("source") in ("XPHB", "XDMG") and (x["name"], x["source"]) not in seen_rules:
                glossary.append(make_rule(x, label))
                seen_rules.add((x["name"], x["source"]))

    categories = [
        ("spells", "Incantesimi", spells),
        ("monsters", "Mostri", monsters),
        ("magic-items", "Oggetti magici", magic),
        ("equipment", "Equipaggiamento", equipment),
        ("classes", "Classi", classes),
        ("subclasses", "Sottoclassi", subclasses),
        ("class-options", "Opzioni di classe", class_options),
        ("feats", "Talenti", feats),
        ("backgrounds", "Background", backgrounds),
        ("species", "Specie", species),
        ("bastions", "Bastioni", bastions),
        ("languages", "Lingue", languages),
        ("deities", "Divinità", deities),
        ("skills", "Abilità", skills),
        ("mastery", "Maestria delle armi", mastery),
        ("properties", "Proprietà delle armi", properties),
        ("treasure", "Tesori", treasure),
        ("item-types", "Tipi di oggetto", item_types),
        ("cards", "Carte", cards),
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
