"""
Data API routes for FAGE Character Generator.
Provides access to game data (weapons, spells, talents, etc.) from CSV files.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from utils.data_loader import data_loader


router = APIRouter()


@router.get("/backgrounds", response_model=List[str])
async def get_backgrounds():
    """
    Get list of available character backgrounds.

    Returns:
        List of background names
    """
    try:
        return data_loader.get_backgrounds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading backgrounds: {str(e)}")


@router.get("/armor", response_model=List[Dict[str, Any]])
async def get_armor():
    """
    Get all armor with stats.

    Returns:
        List of armor dictionaries with Name, Rating, Penalty, Strain, etc.
    """
    try:
        return data_loader.get_armor()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading armor: {str(e)}")


@router.get("/weapons/melee", response_model=List[Dict[str, Any]])
async def get_melee_weapons():
    """
    Get all melee weapons with stats.

    Returns:
        List of melee weapon dictionaries with Weapon, Group, Skill, Damage, etc.
    """
    try:
        return data_loader.get_melee_weapons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading melee weapons: {str(e)}")


@router.get("/weapons/ranged", response_model=List[Dict[str, Any]])
async def get_ranged_weapons():
    """
    Get all ranged weapons with stats.

    Returns:
        List of ranged weapon dictionaries with Weapon, Range, Reload, etc.
    """
    try:
        return data_loader.get_ranged_weapons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading ranged weapons: {str(e)}")


@router.get("/foci", response_model=Dict[str, List[str]])
async def get_foci():
    """
    Get all foci organized by stat.

    Returns:
        Dictionary mapping stat names to lists of available foci.
        Example: {"Fighting": ["Brawling", "Heavy Blades"], "Intelligence": [...]}
    """
    try:
        return data_loader.get_foci()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading foci: {str(e)}")


@router.get("/talents", response_model=List[Dict[str, Any]])
async def get_talents(
    char_class: Optional[str] = Query(
        None,
        description="Filter talents by character class (Envoy, Mage, Rogue, Warrior)"
    )
):
    """
    Get talents, optionally filtered by character class.

    Query Parameters:
        char_class: Character class to filter by (optional)

    Returns:
        List of talent dictionaries with Name, Degree, Effect, Class1, Class2, etc.
    """
    try:
        return data_loader.get_talents(char_class=char_class)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading talents: {str(e)}")


@router.get("/specializations", response_model=List[Dict[str, Any]])
async def get_specializations(
    char_class: Optional[str] = Query(
        None,
        description="Filter specializations by character class"
    )
):
    """
    Get specializations, optionally filtered by character class.

    Query Parameters:
        char_class: Character class to filter by (optional)

    Returns:
        List of specialization dictionaries
    """
    try:
        return data_loader.get_specializations(char_class=char_class)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading specializations: {str(e)}")


@router.get("/arcana", response_model=List[str])
async def get_arcana():
    """
    Get list of available arcana for magic users.

    Returns:
        List of arcana names
    """
    try:
        return data_loader.get_arcana()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading arcana: {str(e)}")


@router.get("/spells", response_model=List[Dict[str, Any]])
async def get_spells(
    arcana: Optional[str] = Query(
        None,
        description="Filter spells by arcana"
    )
):
    """
    Get spells, optionally filtered by arcana.

    Query Parameters:
        arcana: Arcana to filter by (optional)

    Returns:
        List of spell dictionaries with Name, Arcana, MP Cost, TN, Effect, etc.
    """
    try:
        return data_loader.get_spells(arcana=arcana)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading spells: {str(e)}")


@router.get("/stunts", response_model=List[Dict[str, Any]])
async def get_stunts():
    """
    Get all available stunts.

    Returns:
        List of stunt dictionaries with Name, SP Cost, Effect, etc.
    """
    try:
        return data_loader.get_stunts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading stunts: {str(e)}")


@router.get("/special-features", response_model=List[Dict[str, Any]])
async def get_special_features():
    """
    Get user-authored special features from Special_Features.csv.

    Players edit this CSV directly to record ancestry bonuses, character
    traits, and anything else that doesn't fit elsewhere on the sheet.

    Returns:
        List of dicts with Source, Name, Effect.
    """
    try:
        return data_loader.get_special_features()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading special features: {str(e)}")


@router.get("/levelup/{class_name}", response_model=List[Dict[str, Any]])
async def get_levelup_table(class_name: str):
    """
    Get level-up progression table for a specific class.

    Path Parameters:
        class_name: Character class (Envoy, Mage, Rogue, Warrior)

    Returns:
        List of level progression dictionaries

    Raises:
        404: If class name is invalid
    """
    # Validate class name
    valid_classes = ['Envoy', 'Mage', 'Rogue', 'Warrior']
    if class_name not in valid_classes:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid class name. Must be one of: {', '.join(valid_classes)}"
        )

    try:
        return data_loader.get_class_progression(class_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading progression table: {str(e)}")


@router.post("/reload")
async def reload_data():
    """
    Reload all CSV data from disk (development utility).

    Returns:
        Success message
    """
    try:
        data_loader.reload_data()
        return {"message": "Data reloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading data: {str(e)}")
