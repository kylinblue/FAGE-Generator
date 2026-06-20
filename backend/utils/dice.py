"""
Dice rolling utilities for FAGE Character Generator.
Implements 3d6 checks (with stunt detection) and damage rolls.
"""

import random
from typing import List, Optional, Tuple, TypedDict


def roll_d6(n: int) -> List[int]:
    """Roll n six-sided dice and return the individual results."""
    if n <= 0:
        return []
    return [random.randint(1, 6) for _ in range(n)]


def roll_3d6() -> Tuple[List[int], int, bool, int]:
    """
    Roll three six-sided dice with stunt detection.

    Returns:
        - dice: list of three results
        - total: sum of the three dice
        - has_stunt: True when any two dice match (a stunt point is earned)
        - stunt_points: value of the third die (the stunt/drama die) when has_stunt, else 0
    """
    dice = roll_d6(3)
    total = sum(dice)
    has_stunt = dice[0] == dice[1] or dice[0] == dice[2] or dice[1] == dice[2]
    stunt_points = dice[2] if has_stunt else 0
    return dice, total, has_stunt, stunt_points


def roll_with_modifier(modifier: int = 0) -> Tuple[List[int], int, int, bool, int]:
    """Roll 3d6 plus a flat modifier; returns dice, roll_total, final_total, stunt info."""
    dice, roll_total, has_stunt, stunt_points = roll_3d6()
    final_total = roll_total + modifier
    return dice, roll_total, final_total, has_stunt, stunt_points


class CheckResult(TypedDict):
    dice: List[int]
    roll_total: int
    final_total: int
    has_stunt: bool
    stunt_points: int
    target_number: Optional[int]
    success: Optional[bool]


def roll_check(modifier: int = 0, target_number: Optional[int] = None) -> CheckResult:
    """
    Resolve a 3d6 check: roll, add modifier, optionally compare to a target number.

    Shared core for attack rolls, spell casting rolls, and ability checks.
    """
    dice, roll_total, final_total, has_stunt, stunt_points = roll_with_modifier(modifier)
    success = final_total >= target_number if target_number is not None else None
    return {
        "dice": dice,
        "roll_total": roll_total,
        "final_total": final_total,
        "has_stunt": has_stunt,
        "stunt_points": stunt_points,
        "target_number": target_number,
        "success": success,
    }


class DamageResult(TypedDict):
    dice: List[int]
    bonus_dice: List[int]
    modifier: int
    stat_bonus: int
    stunt_bonus: int
    base_total: int
    extra_total: int
    final_total: int


def roll_damage(
    num_dice: int,
    modifier: int = 0,
    stat_bonus: int = 0,
    bonus_dice: int = 0,
    stunt_bonus: int = 0,
) -> DamageResult:
    """
    Roll damage dice and combine with modifiers.

    Args:
        num_dice: Number of base damage d6 (from weapon/spell).
        modifier: Flat damage modifier (weapon Mod column).
        stat_bonus: Stat added to damage (e.g., Willpower for Arcane Blast).
        bonus_dice: Additional d6 to roll (e.g., Rogue Pinpoint).
        stunt_bonus: Stunt die value added to damage per class rules.

    The util is intentionally generic; class/level/conditional logic is
    resolved by the caller, which packages the relevant flags into the
    bonus_dice / stunt_bonus / stat_bonus inputs.
    """
    dice = roll_d6(num_dice)
    bonus = roll_d6(bonus_dice)
    base_total = sum(dice) + modifier + stat_bonus
    extra_total = sum(bonus) + stunt_bonus
    return {
        "dice": dice,
        "bonus_dice": bonus,
        "modifier": modifier,
        "stat_bonus": stat_bonus,
        "stunt_bonus": stunt_bonus,
        "base_total": base_total,
        "extra_total": extra_total,
        "final_total": base_total + extra_total,
    }
