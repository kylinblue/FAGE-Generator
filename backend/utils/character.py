"""
Character utility functions for FAGE Character Generator.
Handles focus formatting, stat calculations, and character-related operations.
"""

import math
from typing import List, Dict
from collections import Counter


def calculate_move(speed: int) -> int:
    """Move distance equals Speed."""
    return speed


def calculate_charge(speed: int) -> int:
    """Charge distance equals half Speed, rounded up."""
    return math.ceil(speed / 2)


def calculate_run(speed: int) -> int:
    """Run distance equals Speed x 2."""
    return speed * 2


def format_foci(focus1: List[str], focus2: List[str]) -> str:
    """
    Format focus selections for display.

    Combines primary and secondary foci, counts duplicates,
    and formats as "Focus (2)" for duplicates.

    Args:
        focus1: Primary focus selections
        focus2: Secondary focus selections (level 11+ only)

    Returns:
        Comma-separated string of formatted foci

    Example:
        >>> format_foci(["Brawling", "Swords"], ["Brawling"])
        'Brawling (2), Swords'
    """
    all_foci = focus1 + focus2
    if not all_foci:
        return ""

    # Count occurrences
    counted = Counter(all_foci)

    # Format with counts
    formatted = [
        f"{name} ({count})" if count > 1 else name
        for name, count in counted.items()
    ]

    return ", ".join(formatted)


def calculate_hp_max(constitution: int, char_class: str, level: int) -> int:
    """
    Calculate maximum hit points based on class and level.

    Base formula from FAGE rules:
    - Level 1: Starting HP varies by class
    - Subsequent levels: +1d6 (average 3.5, rounded to 4) + Constitution per level

    Args:
        constitution: Constitution stat value
        char_class: Character class (Warrior, Mage, Rogue, Envoy)
        level: Character level (1-20)

    Returns:
        Maximum hit points

    Example:
        >>> calculate_hp_max(12, "Warrior", 3)
        # Warrior starts with higher HP
    """
    # Base HP at level 1 (varies by class)
    base_hp = {
        "Warrior": 10 + constitution,
        "Rogue": 10 + constitution,
        "Mage": 10 + constitution,
        "Envoy": 10 + constitution
    }

    hp = base_hp.get(char_class, 10 + constitution)

    # Add HP for levels beyond 1 (approximately 4 + Constitution per level)
    if level > 1:
        hp += (level - 1) * (4 + constitution)

    return hp


def calculate_mp_max(intelligence: int, willpower: int, char_class: str, level: int) -> int:
    """
    Calculate maximum magic points based on class and level.

    Only Mages and some classes have magic points.

    Args:
        intelligence: Intelligence stat value
        willpower: Willpower stat value
        char_class: Character class
        level: Character level

    Returns:
        Maximum magic points (0 for non-magic classes)

    Example:
        >>> calculate_mp_max(14, 12, "Mage", 3)
        # Mage gets MP based on Intelligence/Willpower
    """
    if char_class == "Mage":
        # Mages get Intelligence + Willpower as base MP
        return 10 + intelligence + (level - 1) * 2
    elif char_class == "Envoy":
        # Envoys might have limited magic
        return (intelligence // 2) if level >= 3 else 0
    else:
        # Warriors and Rogues typically don't have MP
        return 0


def calculate_focus_bonus(foci: List[str], level: int) -> int:
    """
    Calculate bonus from having a relevant focus.

    Focus bonuses in FAGE:
    - Levels 1-5: +2 bonus
    - Levels 6-10: +2 bonus
    - Levels 11+: +3 bonus (or +4 with two foci in same skill)

    Args:
        foci: List of foci for the relevant stat
        level: Character level

    Returns:
        Focus bonus value

    Example:
        >>> calculate_focus_bonus(["Brawling"], 6)
        2
        >>> calculate_focus_bonus(["Brawling", "Brawling"], 11)
        4
    """
    if not foci:
        return 0

    # Count duplicates
    focus_count = len(foci)

    if level >= 11:
        # Level 11+: +3 for one focus, +4 for duplicate
        return 4 if focus_count >= 2 else 3
    else:
        # Level 1-10: +2 for having focus
        return 2


def get_primary_stats_for_class(char_class: str) -> List[str]:
    """
    Get the primary stats for a given character class.

    Primary stats are the key abilities for that class.

    Args:
        char_class: Character class

    Returns:
        List of primary stat names

    Example:
        >>> get_primary_stats_for_class("Warrior")
        ['Fighting', 'Strength', 'Constitution']
    """
    primary_stats = {
        "Warrior": ["Fighting", "Strength", "Constitution"],
        "Mage": ["Intelligence", "Willpower", "Accuracy"],
        "Rogue": ["Dexterity", "Perception", "Communication"],
        "Envoy": ["Communication", "Intelligence", "Willpower"]
    }

    return primary_stats.get(char_class, [])
