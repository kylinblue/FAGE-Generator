"""
Currency calculation utilities for FAGE Character Generator.
Handles conversion between gold, silver, and copper.

Conversion rates:
- 10 copper = 1 silver
- 10 silver = 1 gold
- Therefore: 100 copper = 1 gold
"""

from typing import Dict


def calculate_currency(copper: int, silver: int, gold: int) -> Dict[str, int]:
    """
    Normalize currency to proper denominations.

    Converts all currency to copper, then breaks it down into
    the highest denominations possible.

    Args:
        copper: Number of copper pieces
        silver: Number of silver pieces
        gold: Number of gold pieces

    Returns:
        Dictionary with normalized gold, silver, copper values

    Example:
        >>> calculate_currency(250, 5, 0)
        {'gold': 3, 'silver': 0, 'copper': 0}
        >>> # 250 copper + 50 copper (5 silver) = 300 copper total
        >>> # = 3 gold + 0 silver + 0 copper
    """
    # Convert everything to copper
    total_copper = copper + (silver * 10) + (gold * 100)

    # Break down to highest denominations
    gold_out = total_copper // 100
    remaining = total_copper % 100

    silver_out = remaining // 10
    copper_out = remaining % 10

    return {
        "gold": gold_out,
        "silver": silver_out,
        "copper": copper_out
    }


def total_value_in_copper(copper: int, silver: int, gold: int) -> int:
    """
    Calculate total currency value in copper pieces.

    Args:
        copper: Number of copper pieces
        silver: Number of silver pieces
        gold: Number of gold pieces

    Returns:
        Total value in copper pieces

    Example:
        >>> total_value_in_copper(50, 3, 1)
        180
        >>> # 50 copper + 30 copper (3 silver) + 100 copper (1 gold)
    """
    return copper + (silver * 10) + (gold * 100)
