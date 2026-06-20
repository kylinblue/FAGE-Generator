"""
Fillable-PDF field mapping for the FAGE character sheet.

Reads `data/csv/pdf-saving-parameters.csv` (the form-field schema for the
official FAGE character sheet PDF) and maps a character dict to a
{field_name: value} dict ready for fillable-PDF form filling.

CSV columns:
    Field Name   - PDF AcroForm field name (e.g. "Text227", "Check Box242")
    Index        - PDF field index (informational)
    Value        - Human-readable description of the field
    input-name   - Key used to look up the value from the character data
    Special      - 0 = plain text/checkbox, 1 = multi-line / formatted block
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from utils.data_loader import data_loader
from utils.character import (
    calculate_charge,
    calculate_move,
    calculate_run,
    get_primary_stats_for_class,
)


CSV_PATH = Path(__file__).parent.parent / "data" / "csv" / "pdf-saving-parameters.csv"

_INDEXED = re.compile(r"^(?P<key>.+?)\((?P<idx>\d+)\)$")


def _load_schema() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df["input-name"] = df["input-name"].fillna("").astype(str).str.strip()
    df["Field Name"] = df["Field Name"].astype(str).str.strip()
    df["Special"] = pd.to_numeric(df["Special"], errors="coerce").fillna(0).astype(int)
    return df


_schema_cache: Optional[pd.DataFrame] = None


def get_schema() -> pd.DataFrame:
    global _schema_cache
    if _schema_cache is None:
        _schema_cache = _load_schema()
    return _schema_cache


def _focus_label(foci_primary: List[str], foci_secondary: List[str]) -> str:
    """Format combined foci as `Focus, Other (2)` with `(2)` for double-foci."""
    seen: Dict[str, int] = {}
    for f in [*foci_primary, *foci_secondary]:
        if not f:
            continue
        seen[f] = seen.get(f, 0) + 1
    parts = [f"{name} ({n})" if n > 1 else name for name, n in seen.items()]
    return ", ".join(parts)


_SEP = " | "


def _table(header: List[str], rows: List[List[Any]]) -> str:
    """Render header + rows as a fixed-width table (assumes monospace font).

    Each column is padded to the max width of any cell in that column so the
    pipes line up under a Courier-style font.
    """
    if not rows:
        return ""
    all_rows = [list(header)] + [
        ["" if c is None else str(c) for c in r] for r in rows
    ]
    widths = [max(len(r[i]) for r in all_rows) for i in range(len(header))]
    return "\n".join(
        _SEP.join(r[i].ljust(widths[i]) for i in range(len(header)))
        for r in all_rows
    )


def _clean(value: Any) -> str:
    """Stringify a CSV cell, treating None/NaN as empty (matches the JSON view)."""
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def _degree_rank(degree: Any) -> int:
    """Sort rank for a talent/spec/spell degree.

    Accepts the long form ('Novice'/'Expert'/'Master') or the numeric degree
    (1/2/3); unknown values sort last. Mirrors ``degreeRank`` in
    frontend/src/utils/grouping.js so the PDF matches the on-screen order.
    """
    return {
        "Novice": 1, "1": 1,
        "Expert": 2, "2": 2,
        "Master": 3, "3": 3,
    }.get(_clean(degree), 99)


def _group_by(items: List[Any], key_fn, rank_fn=lambda _item: 0) -> List[Any]:
    """Stable group-by for table display.

    Rows sharing a key stay together; groups appear in the order their key was
    first seen (tracking selection order rather than imposing an alphabetical
    one), and rows within a group are ordered by ``rank_fn``, falling back to
    their original order on ties. Mirrors ``groupBy`` in
    frontend/src/utils/grouping.js.
    """
    first_seen: Dict[Any, int] = {}
    for i, item in enumerate(items):
        key = key_fn(item)
        if key not in first_seen:
            first_seen[key] = i
    # Python's sort is stable, so equal (group, rank) keys keep their original
    # relative order -- matching the frontend's explicit index tie-break.
    return sorted(items, key=lambda item: (first_seen[key_fn(item)], rank_fn(item)))


def _format_inventory(items: List[Dict[str, Any]]) -> str:
    rows = [
        [it.get("item", ""), it.get("quantity", 1)]
        for it in (items or [])
        if it.get("item")
    ]
    return _table(["Item", "Quantity"], rows)


def _format_currency(currency: Dict[str, int]) -> str:
    g, s, c = currency.get("gold", 0), currency.get("silver", 0), currency.get("copper", 0)
    return f"{g}g {s}s {c}c"


_armor_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None


def _armor_lookup() -> Dict[str, Dict[str, Any]]:
    global _armor_lookup_cache
    if _armor_lookup_cache is None:
        _armor_lookup_cache = {a["Name"]: a for a in data_loader.get_armor()}
    return _armor_lookup_cache


def _format_armor(
    armor_name: Optional[str],
    rating_override: Optional[int] = None,
    penalty_override: Optional[int] = None,
) -> str:
    if not armor_name:
        return ""
    a = _armor_lookup().get(armor_name) or {}
    rating = rating_override if rating_override is not None else a.get("Rating", "")
    penalty = penalty_override if penalty_override is not None else a.get("Penalty", "")
    return _SEP.join(str(c) for c in (armor_name, rating, penalty))


_spell_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None
_stunt_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None
_talent_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None
_spec_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None


def _spell_lookup() -> Dict[str, Dict[str, Any]]:
    global _spell_lookup_cache
    if _spell_lookup_cache is None:
        _spell_lookup_cache = {s["Name"]: s for s in data_loader.get_spells()}
    return _spell_lookup_cache


def _stunt_lookup() -> Dict[str, Dict[str, Any]]:
    global _stunt_lookup_cache
    if _stunt_lookup_cache is None:
        _stunt_lookup_cache = {s["Name"]: s for s in data_loader.get_stunts()}
    return _stunt_lookup_cache


def _talent_lookup() -> Dict[str, Dict[str, Any]]:
    global _talent_lookup_cache
    if _talent_lookup_cache is None:
        _talent_lookup_cache = {t["Name"]: t for t in data_loader.get_talents()}
    return _talent_lookup_cache


def _spec_lookup() -> Dict[str, Dict[str, Any]]:
    global _spec_lookup_cache
    if _spec_lookup_cache is None:
        _spec_lookup_cache = {s["Name"]: s for s in data_loader.get_specializations()}
    return _spec_lookup_cache


def _format_spells(spells: List[str]) -> str:
    lookup = _spell_lookup()
    # Group by arcana (the base name before any " - Degree" suffix), Novice -> Master within.
    ordered = _group_by(
        spells or [],
        lambda name: _clean(lookup.get(name, {}).get("Arcana")).split(" - ")[0].strip(),
        lambda name: _degree_rank(lookup.get(name, {}).get("Degree", "")),
    )
    rows = []
    for name in ordered:
        s = lookup.get(name, {})
        rows.append([name, s.get("MP", ""), s.get("CastTime", ""), s.get("TN", "")])
    return _table(["Spell", "MP", "Casting Time", "TN"], rows)


def _format_stunts(stunts: List[str]) -> str:
    lookup = _stunt_lookup()
    # Group by type (Combat / Social / Magic / ...), untyped stunts under "Other".
    ordered = _group_by(
        stunts or [],
        lambda name: _clean(lookup.get(name, {}).get("Type")) or "Other",
    )
    rows = [[name, lookup.get(name, {}).get("Cost", "")] for name in ordered]
    return _table(["Stunt", "Cost"], rows)


_melee_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None
_ranged_lookup_cache: Optional[Dict[str, Dict[str, Any]]] = None


def _melee_lookup() -> Dict[str, Dict[str, Any]]:
    global _melee_lookup_cache
    if _melee_lookup_cache is None:
        _melee_lookup_cache = {w["Weapon"]: w for w in data_loader.get_melee_weapons()}
    return _melee_lookup_cache


def _ranged_lookup() -> Dict[str, Dict[str, Any]]:
    global _ranged_lookup_cache
    if _ranged_lookup_cache is None:
        _ranged_lookup_cache = {w["Weapon"]: w for w in data_loader.get_ranged_weapons()}
    return _ranged_lookup_cache


def _resolve_weapon(entry: Any, lookup: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Normalize a weapon entry (string name or dict) into a full stat dict."""
    if isinstance(entry, dict):
        name = entry.get("Weapon") or entry.get("name")
        merged = dict(lookup.get(name, {})) if name else {}
        merged.update({k: v for k, v in entry.items() if v not in (None, "")})
        return merged or None
    if isinstance(entry, str):
        return lookup.get(entry) or {"Weapon": entry}
    return None


def _resolve_indexed(input_name: str, character: Dict[str, Any]) -> Any:
    """Resolve `Key(N)` patterns for repeating weapon slots (1-indexed)."""
    m = _INDEXED.match(input_name)
    if not m:
        return None
    key = m.group("key")
    idx = int(m.group("idx")) - 1

    melee_keys = ("WeaponName", "WeaponStat", "Damage dice")
    ranged_keys = ("RangedName", "RangedStat", "RangedDamage",
                   "ShortRange", "LongRange", "Reload")

    if key in melee_keys:
        weapons = character.get("equipment", {}).get("melee_weapons", [])
        if idx >= len(weapons):
            return None
        w = _resolve_weapon(weapons[idx], _melee_lookup())
        if not w:
            return None
        if key == "WeaponName":
            return w.get("Weapon", "")
        if key == "WeaponStat":
            return w.get("Skill", "")
        if key == "Damage dice":
            return w.get("Damage", "")

    if key in ranged_keys:
        weapons = character.get("equipment", {}).get("ranged_weapons", [])
        if idx >= len(weapons):
            return None
        w = _resolve_weapon(weapons[idx], _ranged_lookup())
        if not w:
            return None
        return {
            "RangedName": w.get("Weapon", ""),
            "RangedStat": w.get("Skill", ""),
            "RangedDamage": w.get("Damage", ""),
            "ShortRange": w.get("Short Range", ""),
            "LongRange": w.get("Long Range", ""),
            "Reload": w.get("Reload", ""),
        }[key]

    return None


def _split_entry(entry: str) -> tuple:
    """Split a stored 'Name|Degree' entry. Degree may be missing."""
    parts = (entry or "").split("|", 1)
    name = parts[0].strip()
    degree = parts[1].strip() if len(parts) > 1 else ""
    return name, degree


def _talent_row(entry: str) -> List[Any]:
    name, degree = _split_entry(entry)
    info = _talent_lookup().get(name, {})
    label = f"{name} ({degree})" if degree else name
    return [label, info.get("Source", ""), info.get("Page", "")]


def _spec_row(entry: str) -> List[Any]:
    name, degree = _split_entry(entry)
    info = _spec_lookup().get(name, {})
    label = f"{name} ({degree})" if degree else name
    return [label, info.get("Source", ""), info.get("Page", "")]


def _format_talents(talents: List[str], specializations: List[str]) -> str:
    sections: List[str] = []

    # Group by title (Sharpshooter, Mage Hunter, ...) with Novice -> Expert -> Master within each.
    _by_title = lambda e: _split_entry(e)[0]
    _by_degree = lambda e: _degree_rank(_split_entry(e)[1])

    sections.append("[ Talents ]")
    talent_rows = [_talent_row(t) for t in _group_by(talents or [], _by_title, _by_degree)]
    sections.append(
        _table(["Name", "Source", "Page"], talent_rows) or "Name | Source | Page"
    )

    sections.append("")
    sections.append("[ Specializations ]")
    spec_rows = [_spec_row(s) for s in _group_by(specializations or [], _by_title, _by_degree)]
    sections.append(
        _table(["Name", "Source", "Page"], spec_rows) or "Name | Source | Page"
    )

    sf_rows = [
        [sf.get("Source", ""), sf.get("Name", ""), sf.get("Effect", "")]
        for sf in data_loader.get_special_features()
        if sf.get("Source") or sf.get("Name") or sf.get("Effect")
    ]
    if sf_rows:
        sections.append("")
        sections.append("[ Special Features ]")
        sections.append(_table(["Source", "Name", "Effect"], sf_rows))

    return "\n".join(sections)


def _format_groups(weapon_groups: List[str]) -> str:
    return ", ".join(weapon_groups or [])


def _resolve(input_name: str, character: Dict[str, Any]) -> Any:
    """Resolve one input-name token to a value pulled from the character dict."""
    stats = character.get("stats", {})
    foci_p = character.get("foci_primary", {})
    foci_s = character.get("foci_secondary", {})
    extras = character.get("extras", {})
    equipment = character.get("equipment", {})
    magic = character.get("magic", {})

    nine_stats = ("Accuracy", "Communication", "Constitution", "Dexterity",
                  "Fighting", "Intelligence", "Perception", "Strength", "Willpower")

    if input_name in nine_stats:
        return stats.get(input_name, 0)

    if input_name.endswith("(Foc)"):
        stat = input_name[: -len("(Foc)")]
        return _focus_label(foci_p.get(stat, []), foci_s.get(stat, []))

    if input_name.endswith("CheckBox"):
        # The 9 stat checkboxes on the sheet mark the character's PRIMARY
        # abilities (the class's key stats), not whether a focus is held.
        stat = input_name[: -len("CheckBox")]
        primary = get_primary_stats_for_class(character.get("char_class", ""))
        return stat in primary

    indexed = _resolve_indexed(input_name, character)
    if indexed is not None:
        return indexed

    direct = {
        "Name": character.get("name", ""),
        "Ancestry": character.get("ancestry", ""),
        "Background": character.get("background", ""),
        "Class": character.get("char_class", ""),
        "Level": character.get("level", 1),
        "Social": character.get("social_class", ""),
        "Speed": character.get("speed", 0),
        "Defence": character.get("defense", 0),
        "Experience": character.get("experience", 0),
        "CurrentHP": character.get("hp_current", 0),
        "MaxHP": character.get("hp_max", 0),
        "CurrentMP": character.get("mp_current", 0),
        "MaxMP": character.get("mp_max", 0),
        "Spellpower": stats.get("Willpower", 0) + 10,
        "Relationships": extras.get("relationships", ""),
        "Goals": extras.get("goals_ties", ""),
        "Backstory": extras.get("backstory", ""),
    }
    if input_name in direct:
        return direct[input_name]

    speed = character.get("speed", 0) or 0
    if input_name == "MoveSpeed":
        return calculate_move(speed)
    if input_name == "ChargeSpeed":
        return calculate_charge(speed)
    if input_name == "RunSpeed":
        return calculate_run(speed)

    block = {
        "StuntsPDF": _format_stunts(extras.get("stunts", [])),
        "ArmourPDF": _format_armor(
            equipment.get("armor"),
            equipment.get("armor_rating"),
            equipment.get("armor_penalty"),
        ),
        "InventoryPDF": _format_inventory(extras.get("inventory", [])),
        "CurrencyPDF": _format_currency(extras.get("currency", {})),
        "SpellsPDF": _format_spells(magic.get("spells", [])),
        "TalentsPDF": _format_talents(
            character.get("talents", []),
            character.get("specializations", []),
        ),
        "GroupsPDF": _format_groups(extras.get("weapon_groups", [])),
    }
    if input_name in block:
        return block[input_name]

    return None


def map_character_to_fields(character: Dict[str, Any]) -> Dict[str, Any]:
    """Build `{pdf_field_name: value}` dict from a character dict using the schema CSV."""
    schema = get_schema()
    fields: Dict[str, Any] = {}
    for _, row in schema.iterrows():
        input_name = row["input-name"]
        if not input_name:
            continue
        value = _resolve(input_name, character)
        if value is None:
            continue
        fields[row["Field Name"]] = value
    return fields
