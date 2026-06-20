"""
Character API routes for FAGE Character Generator.
Provides CRUD operations for character management.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.character import (
    Character,
    CharacterCreate,
    CharacterUpdate,
    CharacterSummary
)
from utils.storage import character_storage
from datetime import datetime


router = APIRouter()


@router.post("/", response_model=Character, status_code=201)
async def create_character(character_data: CharacterCreate):
    """
    Create a new character.

    Request Body:
        CharacterCreate model with name, class, stats, etc.

    Returns:
        Complete Character model with assigned ID and timestamps

    Example:
        POST /api/characters
        {
            "name": "Thorin Ironforge",
            "char_class": "Warrior",
            "stats": {"Strength": 15, "Fighting": 14, ...}
        }
    """
    # Convert CharacterCreate to full Character model
    character = Character(
        **character_data.model_dump(),
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )

    # Save to storage
    try:
        saved_data = character_storage.save(character.model_dump())
        return Character(**saved_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving character: {str(e)}")


@router.get("/{character_id}", response_model=Character)
async def get_character(character_id: str):
    """
    Get a character by ID.

    Path Parameters:
        character_id: UUID of the character

    Returns:
        Complete Character model

    Raises:
        404: If character not found
    """
    character_data = character_storage.load(character_id)

    if character_data is None:
        raise HTTPException(status_code=404, detail="Character not found")

    return Character(**character_data)


@router.put("/{character_id}", response_model=Character)
async def update_character(character_id: str, updates: CharacterUpdate):
    """
    Update an existing character.

    Path Parameters:
        character_id: UUID of the character

    Request Body:
        CharacterUpdate model with fields to update (all optional)

    Returns:
        Updated Character model

    Raises:
        404: If character not found

    Example:
        PUT /api/characters/abc-123
        {
            "level": 3,
            "hp_current": 35,
            "stats": {"Strength": 16}
        }
    """
    # Load existing character
    character_data = character_storage.load(character_id)

    if character_data is None:
        raise HTTPException(status_code=404, detail="Character not found")

    # Convert to Character model
    character = Character(**character_data)

    # Apply updates (only non-None fields)
    update_data = updates.model_dump(exclude_unset=True)

    # Handle nested updates (stats, equipment, etc.)
    for key, value in update_data.items():
        if value is not None:
            if key in ['stats', 'foci_primary', 'foci_secondary', 'equipment', 'magic', 'extras']:
                # For nested models, merge with existing data
                existing_value = getattr(character, key)
                if hasattr(existing_value, 'model_dump'):
                    # It's a Pydantic model
                    existing_dict = existing_value.model_dump()
                    existing_dict.update(value.model_dump(exclude_unset=True) if hasattr(value, 'model_dump') else value)
                    setattr(character, key, type(existing_value)(**existing_dict))
                else:
                    setattr(character, key, value)
            else:
                # For simple fields, direct update
                setattr(character, key, value)

    # Update timestamp
    character.updated_at = datetime.utcnow().isoformat()

    # Save to storage
    try:
        saved_data = character_storage.save(character.model_dump())
        return Character(**saved_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating character: {str(e)}")


@router.delete("/{character_id}", status_code=204)
async def delete_character(character_id: str):
    """
    Delete a character.

    Path Parameters:
        character_id: UUID of the character

    Returns:
        204 No Content on success

    Raises:
        404: If character not found
    """
    success = character_storage.delete(character_id)

    if not success:
        raise HTTPException(status_code=404, detail="Character not found")

    return None


@router.get("/", response_model=List[CharacterSummary])
async def list_characters(
    skip: int = Query(0, ge=0, description="Number of characters to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of characters to return")
):
    """
    List all saved characters.

    Query Parameters:
        skip: Number of characters to skip (default: 0)
        limit: Maximum number to return (default: 100, max: 1000)

    Returns:
        List of CharacterSummary models (lightweight version)

    Example:
        GET /api/characters?skip=0&limit=10
    """
    try:
        characters = character_storage.list_all(skip=skip, limit=limit)

        # Convert to CharacterSummary (only essential fields)
        summaries = [
            CharacterSummary(
                id=char['id'],
                name=char['name'],
                player_name=char.get('player_name'),
                char_class=char['char_class'],
                level=char['level'],
                created_at=char['created_at'],
                updated_at=char['updated_at']
            )
            for char in characters
        ]

        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing characters: {str(e)}")


