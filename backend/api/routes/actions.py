"""
Action API routes for FAGE Character Generator.
Provides endpoints for dice rolling, spell casting, and other game actions.
"""

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from utils.dice import roll_check, roll_damage
from utils.currency import calculate_currency, total_value_in_copper
from utils.data_loader import data_loader
from utils.pdf import generate_character_pdf_bytes


router = APIRouter()


# ============================================================================
# Dice Rolling Models
# ============================================================================

class DiceRollRequest(BaseModel):
    """Request model for basic dice roll."""
    modifier: int = Field(default=0, description="Modifier to add to roll")


class DiceRollResponse(BaseModel):
    """Response model for dice roll."""
    dice: List[int] = Field(..., description="Individual dice results (1-6)")
    roll_total: int = Field(..., description="Sum of dice only")
    final_total: int = Field(..., description="Sum of dice + modifier")
    has_stunt: bool = Field(..., description="Whether stunt point was earned")
    stunt_points: int = Field(default=0, description="Stunt point value (third die)")


class SpellRollRequest(BaseModel):
    """Request model for spell casting roll."""
    spell_name: str = Field(..., description="Name of spell being cast")
    intelligence: int = Field(..., ge=0, le=20, description="Intelligence stat value")
    focus_bonus: int = Field(default=0, description="Bonus from relevant focus")


class SpellRollResponse(BaseModel):
    """Response model for spell casting roll."""
    dice: List[int]
    roll_total: int
    final_total: int
    target_number: int
    success: bool
    has_stunt: bool
    stunt_points: int = 0
    spell_name: str
    spell_effect: Optional[str] = None


class AttackRollRequest(BaseModel):
    """Request model for weapon attack roll."""
    weapon_name: str = Field(..., description="Name of weapon used")
    stat_value: int = Field(..., ge=0, le=20, description="Relevant stat (Fighting/Accuracy)")
    focus_bonus: int = Field(default=0, description="Bonus from weapon focus")
    is_melee: bool = Field(default=True, description="True for melee, False for ranged")


class AttackRollResponse(BaseModel):
    """Response model for weapon attack roll."""
    dice: List[int]
    roll_total: int
    final_total: int
    has_stunt: bool
    stunt_points: int = 0
    weapon_name: str
    damage: Optional[str] = None


class DamageRollRequest(BaseModel):
    """Request model for a damage roll.

    The endpoint is generic: the frontend resolves class/level/conditional
    rules and packages the resulting extras into bonus_dice / stunt_bonus /
    stat_bonus. Provide either weapon_name (looked up in the CSV) or
    num_dice + modifier directly.
    """
    weapon_name: Optional[str] = Field(default=None, description="Weapon name to look up in CSV")
    is_melee: bool = Field(default=True, description="Lookup table when weapon_name is set")
    num_dice: Optional[int] = Field(default=None, ge=0, description="Override base damage dice count")
    modifier: int = Field(default=0, description="Override flat damage modifier")
    stat_bonus: int = Field(default=0, description="Stat added to damage (e.g., Willpower for Arcane Blast)")
    bonus_dice: int = Field(default=0, ge=0, description="Extra d6 added to damage (e.g., Rogue Pinpoint)")
    stunt_bonus: int = Field(default=0, ge=0, description="Stunt die value added to damage per class rules")
    extras_label: Optional[str] = Field(default=None, description="Display label for applied class extras")


class DamageRollResponse(BaseModel):
    """Response model for a damage roll."""
    dice: List[int]
    bonus_dice: List[int]
    modifier: int
    stat_bonus: int
    stunt_bonus: int
    base_total: int
    extra_total: int
    final_total: int
    weapon_name: Optional[str] = None
    extras_label: Optional[str] = None


# ============================================================================
# Currency Models
# ============================================================================

class CurrencyCalculateRequest(BaseModel):
    """Request model for currency calculation."""
    gold: int = Field(default=0, ge=0)
    silver: int = Field(default=0, ge=0)
    copper: int = Field(default=0, ge=0)


class CurrencyCalculateResponse(BaseModel):
    """Response model for currency calculation."""
    gold: int
    silver: int
    copper: int
    total_copper: int


# ============================================================================
# Dice Rolling Endpoints
# ============================================================================

@router.post("/roll/dice", response_model=DiceRollResponse)
async def roll_dice(request: DiceRollRequest):
    """
    Roll 3d6 with optional modifier.

    Request Body:
        modifier: Bonus to add to the roll (default: 0)

    Returns:
        Dice results, totals, and stunt point status

    Example:
        POST /api/roll/dice
        {"modifier": 5}

        Response:
        {
            "dice": [4, 4, 2],
            "roll_total": 10,
            "final_total": 15,
            "has_stunt": true
        }
    """
    result = roll_check(request.modifier)

    return DiceRollResponse(
        dice=result["dice"],
        roll_total=result["roll_total"],
        final_total=result["final_total"],
        has_stunt=result["has_stunt"],
        stunt_points=result["stunt_points"],
    )


@router.post("/roll/spell", response_model=SpellRollResponse)
async def roll_spell(request: SpellRollRequest):
    """
    Roll for spell casting.

    Rolls 3d6 + Intelligence + focus bonus and compares to spell's Target Number.

    Request Body:
        spell_name: Name of spell being cast
        intelligence: Character's Intelligence stat
        focus_bonus: Bonus from relevant focus (default: 0)

    Returns:
        Roll results, success/failure, and spell details

    Raises:
        404: If spell not found

    Example:
        POST /api/roll/spell
        {
            "spell_name": "Arcane Bolt",
            "intelligence": 14,
            "focus_bonus": 2
        }
    """
    # Get spell data
    try:
        spells = data_loader.get_spells()
        spell = next((s for s in spells if s.get('Name') == request.spell_name), None)

        if spell is None:
            raise HTTPException(
                status_code=404,
                detail=f"Spell '{request.spell_name}' not found"
            )

        target_number = int(spell.get('TN', 0))
        result = roll_check(request.intelligence + request.focus_bonus, target_number)

        return SpellRollResponse(
            dice=result["dice"],
            roll_total=result["roll_total"],
            final_total=result["final_total"],
            target_number=target_number,
            success=result["success"],
            has_stunt=result["has_stunt"],
            stunt_points=result["stunt_points"],
            spell_name=request.spell_name,
            spell_effect=spell.get('Effect'),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing spell roll: {str(e)}"
        )


@router.post("/roll/attack", response_model=AttackRollResponse)
async def roll_attack(request: AttackRollRequest):
    """
    Roll for weapon attack.

    Rolls 3d6 + stat + focus bonus for the attack.

    Request Body:
        weapon_name: Name of weapon used
        stat_value: Fighting (melee) or Accuracy (ranged)
        focus_bonus: Bonus from weapon focus
        is_melee: True for melee, False for ranged

    Returns:
        Roll results and weapon details

    Example:
        POST /api/roll/attack
        {
            "weapon_name": "Longsword",
            "stat_value": 14,
            "focus_bonus": 2,
            "is_melee": true
        }
    """
    try:
        # Get weapon data
        if request.is_melee:
            weapons = data_loader.get_melee_weapons()
        else:
            weapons = data_loader.get_ranged_weapons()

        weapon = next((w for w in weapons if w.get('Weapon') == request.weapon_name), None)

        result = roll_check(request.stat_value + request.focus_bonus)

        return AttackRollResponse(
            dice=result["dice"],
            roll_total=result["roll_total"],
            final_total=result["final_total"],
            has_stunt=result["has_stunt"],
            stunt_points=result["stunt_points"],
            weapon_name=request.weapon_name,
            damage=weapon.get('Damage') if weapon else None,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing attack roll: {str(e)}"
        )


@router.post("/roll/damage", response_model=DamageRollResponse)
async def roll_damage_endpoint(request: DamageRollRequest):
    """
    Roll damage dice with optional class extras.

    The endpoint is a generic dice pipeline. The frontend determines which
    class/level rules apply (Envoy stunt damage, Mage Arcane Blast stunt,
    Rogue Pinpoint d6, Warrior stunt damage, etc.) and packages the
    resulting extras into bonus_dice / stunt_bonus / stat_bonus.

    Provide either weapon_name (looked up in CSV for Dice/Mod) or
    num_dice + modifier directly. Direct fields take precedence when both
    are supplied.
    """
    try:
        weapon = None
        num_dice = request.num_dice
        modifier = request.modifier

        if request.weapon_name and (request.num_dice is None):
            weapons = (
                data_loader.get_melee_weapons()
                if request.is_melee
                else data_loader.get_ranged_weapons()
            )
            weapon = next(
                (w for w in weapons if w.get('Weapon') == request.weapon_name),
                None,
            )
            if weapon is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Weapon '{request.weapon_name}' not found",
                )
            num_dice = int(weapon.get('Dice', 0))
            if request.modifier == 0:
                modifier = int(weapon.get('Mod', 0))

        if num_dice is None:
            raise HTTPException(
                status_code=400,
                detail="Provide either weapon_name or num_dice",
            )

        result = roll_damage(
            num_dice=num_dice,
            modifier=modifier,
            stat_bonus=request.stat_bonus,
            bonus_dice=request.bonus_dice,
            stunt_bonus=request.stunt_bonus,
        )

        return DamageRollResponse(
            dice=result["dice"],
            bonus_dice=result["bonus_dice"],
            modifier=result["modifier"],
            stat_bonus=result["stat_bonus"],
            stunt_bonus=result["stunt_bonus"],
            base_total=result["base_total"],
            extra_total=result["extra_total"],
            final_total=result["final_total"],
            weapon_name=request.weapon_name,
            extras_label=request.extras_label,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing damage roll: {str(e)}",
        )


# ============================================================================
# Currency Endpoints
# ============================================================================

@router.post("/currency/calculate", response_model=CurrencyCalculateResponse)
async def calculate_currency_endpoint(request: CurrencyCalculateRequest):
    """
    Calculate normalized currency values.

    Converts currency to highest denominations:
    - 100 copper = 1 silver
    - 100 silver = 1 gold

    Request Body:
        gold, silver, copper amounts

    Returns:
        Normalized currency and total value in copper

    Example:
        POST /api/currency/calculate
        {"gold": 0, "silver": 5, "copper": 250}

        Response:
        {
            "gold": 0,
            "silver": 7,
            "copper": 50,
            "total_copper": 750
        }
    """
    try:
        # Calculate normalized currency
        result = calculate_currency(
            request.copper,
            request.silver,
            request.gold
        )

        # Calculate total value
        total = total_value_in_copper(
            request.copper,
            request.silver,
            request.gold
        )

        return CurrencyCalculateResponse(
            gold=result['gold'],
            silver=result['silver'],
            copper=result['copper'],
            total_copper=total
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating currency: {str(e)}"
        )


# ============================================================================
# PDF Export Endpoints
# ============================================================================

class PDFExportRequest(BaseModel):
    """Request model for PDF export."""
    character: dict = Field(..., description="Complete character data")


REQUIRED_PDF_FIELDS = ("name", "char_class", "level", "stats")
REQUIRED_STATS = (
    "Accuracy", "Communication", "Constitution", "Dexterity",
    "Fighting", "Intelligence", "Perception", "Strength", "Willpower",
)


def _missing_pdf_fields(character: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for field in REQUIRED_PDF_FIELDS:
        value = character.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)

    stats = character.get("stats") or {}
    if isinstance(stats, dict):
        for stat in REQUIRED_STATS:
            if stat not in stats or stats[stat] in (None, ""):
                missing.append(f"stats.{stat}")
    return missing


@router.post("/export/pdf")
async def export_pdf(character: Dict[str, Any] = Body(...)):
    """
    Export a character sheet as a filled PDF.

    Accepts the raw character dictionary in the body and returns the
    AcroForm-filled FAGE sheet as a PDF download.
    """
    missing = _missing_pdf_fields(character)
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot export PDF — required character fields are missing or empty.",
                "missing_fields": missing,
                "hint": "Fill in these fields on the character sheet before exporting.",
            },
        )
    try:
        pdf_bytes = generate_character_pdf_bytes(character)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {e}")

    char_name = character["name"].replace(" ", "_").replace("/", "_").replace("\\", "_")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{char_name}.pdf"'},
    )


