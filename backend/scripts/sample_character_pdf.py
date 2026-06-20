"""Generate a sample character PDF for visual review."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.pdf import generate_character_pdf


CHARACTER = {
    "name": "Lyra Embershade",
    "player_name": "Sample Player",
    "char_class": "Mage",
    "ancestry": "Elf",
    "background": "Wanderer",
    "social_class": "Outsider",
    "level": 5,
    "experience": 11,
    "speed": 12,
    "defense": 13,
    "hp_current": 27,
    "hp_max": 32,
    "mp_current": 18,
    "mp_max": 26,
    "stats": {
        "Accuracy": 2,
        "Communication": 1,
        "Constitution": 1,
        "Dexterity": 2,
        "Fighting": 0,
        "Intelligence": 4,
        "Perception": 3,
        "Strength": 0,
        "Willpower": 3,
    },
    "foci_primary": {
        "Accuracy": ["Arcane Blast"],
        "Arcana": ["Fire", "Air"],
        "Communication": [],
        "Constitution": ["Stamina"],
        "Dexterity": ["Stealth"],
        "Fighting": [],
        "Intelligence": ["Arcane Lore", "Historical Lore"],
        "Perception": ["Searching"],
        "Strength": [],
        "Willpower": ["Self-Discipline"],
    },
    "foci_secondary": {
        "Accuracy": [],
        "Arcana": ["Fire"],
        "Communication": [],
        "Constitution": [],
        "Dexterity": [],
        "Fighting": [],
        "Intelligence": ["Arcane Lore"],
        "Perception": [],
        "Strength": [],
        "Willpower": [],
    },
    "talents": [
        "Linguistics|Novice",
        "Lore|Novice",
        "Magic Training|Expert",
    ],
    "specializations": [
        "Arcane Disciple|Novice",
    ],
    "equipment": {
        "armor": "Light Leather",
        "melee_weapons": ["Staff"],
        "ranged_weapons": [],
    },
    "magic": {
        "arcana": ["Fire - Novice", "Air - Novice", "Fire - Expert"],
        "spells": [
            "Arcane Blast",
            "Flame Blast",
            "Flaming Weapon",
            "Shape Fire",
            "Air Bubble",
            "Wind Net",
            "Burning Shield",
        ],
    },
    "extras": {
        "inventory": [
            {"item": "Spellbook (worn leather)", "quantity": 1},
            {"item": "Healing Potion", "quantity": 3},
            {"item": "Lesser Mana Potion", "quantity": 2},
            {"item": "Travel Rations", "quantity": 7},
            {"item": "Bedroll", "quantity": 1},
            {"item": "Tinderbox", "quantity": 1},
            {"item": "Ink & Quill", "quantity": 1},
            {"item": "Silver Locket", "quantity": 1},
        ],
        "currency": {"gold": 42, "silver": 18, "copper": 36},
        "stunts": ["Boost", "Mighty Spell", "Skirmish", "Stay Aware"],
        "weapon_groups": ["Staves", "Brawling"],
        "backstory": (
            "Born in the canopy-city of Vaelthorn, Lyra apprenticed under the "
            "Pyromancer Sael until a fire she could not contain consumed her "
            "master's tower. She has wandered the lowlands since, seeking the "
            "older texts that might explain what she actually summoned that night."
        ),
        "relationships": (
            "Master Sael (deceased, complicated). Caravan-friend Brom (Warrior, "
            "owes her a life-debt). Archivist Wenna in Greyport (informant)."
        ),
        "goals_ties": (
            "Short term: recover Sael's surviving notebooks. "
            "Long term: understand what came through the breach."
        ),
    },
    "auto_apply_damage_extras": True,
    "show_arcana_focus_options": True,
}


def main() -> None:
    out = generate_character_pdf(CHARACTER)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
