"""
Pydantic models for FAGE Character Generator.
Data models for character sheets, stats, equipment, magic, and related features.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import uuid4


class Stats(BaseModel):
    """Character ability scores (0-20 range)."""
    Accuracy: int = Field(default=0, ge=0, le=20)
    Communication: int = Field(default=0, ge=0, le=20)
    Constitution: int = Field(default=0, ge=0, le=20)
    Dexterity: int = Field(default=0, ge=0, le=20)
    Fighting: int = Field(default=0, ge=0, le=20)
    Intelligence: int = Field(default=0, ge=0, le=20)
    Perception: int = Field(default=0, ge=0, le=20)
    Strength: int = Field(default=0, ge=0, le=20)
    Willpower: int = Field(default=0, ge=0, le=20)


class Foci(BaseModel):
    """Focus selections per stat (two-level dependent selections)."""
    Accuracy: List[str] = Field(default_factory=list)
    Arcana: List[str] = Field(default_factory=list)
    Communication: List[str] = Field(default_factory=list)
    Constitution: List[str] = Field(default_factory=list)
    Dexterity: List[str] = Field(default_factory=list)
    Fighting: List[str] = Field(default_factory=list)
    Intelligence: List[str] = Field(default_factory=list)
    Perception: List[str] = Field(default_factory=list)
    Strength: List[str] = Field(default_factory=list)
    Willpower: List[str] = Field(default_factory=list)


class Equipment(BaseModel):
    """Character equipment (armor and weapons)."""
    armor: Optional[str] = None
    armor_rating: Optional[int] = None
    armor_penalty: Optional[int] = None
    melee_weapons: List[str] = Field(default_factory=list)
    ranged_weapons: List[str] = Field(default_factory=list)


class Magic(BaseModel):
    """Magic system data (arcana and spells)."""
    arcana: List[str] = Field(default_factory=list, description="Known arcana")
    spells: List[str] = Field(default_factory=list, description="Known spells")


class InventoryItem(BaseModel):
    """Single inventory item with quantity."""
    item: str = Field(..., min_length=1, description="Item name")
    quantity: int = Field(default=1, ge=1, description="Item quantity")


class Currency(BaseModel):
    """Character currency (gold, silver, copper)."""
    gold: int = Field(default=0, ge=0)
    silver: int = Field(default=0, ge=0)
    copper: int = Field(default=0, ge=0)


class Extras(BaseModel):
    """Additional character features (inventory, currency, stunts, backstory)."""
    inventory: List[InventoryItem] = Field(default_factory=list)
    currency: Currency = Field(default_factory=Currency)
    stunts: List[str] = Field(default_factory=list)
    weapon_groups: List[str] = Field(default_factory=list, description="Trained weapon-group proficiencies")
    backstory: str = Field(default="", description="Character backstory")
    relationships: str = Field(default="", description="Character relationships")
    goals_ties: str = Field(default="", description="Character goals and ties")
    extra_notes: str = Field(default="", description="Extra notes about the character")


class Character(BaseModel):
    """Complete character sheet model."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique character ID")
    name: str = Field(..., min_length=1, max_length=100, description="Character name")
    player_name: Optional[str] = Field(default=None, max_length=100, description="Player name")
    char_class: str = Field(..., description="Character class")
    background: Optional[str] = Field(default=None, description="Character background")
    level: int = Field(default=1, ge=1, le=20, description="Character level")

    # New profile fields
    ancestry: Optional[str] = Field(default=None, max_length=100, description="Character ancestry")
    social_class: Optional[str] = Field(default=None, max_length=100, description="Character social class")
    speed: int = Field(default=0, ge=0, description="Character speed")
    defense: int = Field(default=0, ge=0, description="Character defense")
    experience: int = Field(default=0, ge=0, description="Character experience points")
    photo: Optional[str] = Field(default=None, description="Base64-encoded photo")

    # Core stats and derived values
    stats: Stats = Field(default_factory=Stats)
    hp_current: int = Field(default=0, ge=0, description="Current hit points")
    hp_max: int = Field(default=0, ge=0, description="Maximum hit points")
    mp_current: int = Field(default=0, ge=0, description="Current magic points")
    mp_max: int = Field(default=0, ge=0, description="Maximum magic points")

    # Foci (two-level selections)
    foci_primary: Foci = Field(default_factory=Foci, description="Primary focus selections")
    foci_secondary: Foci = Field(default_factory=Foci, description="Secondary focus selections (level 11+)")

    # Talents and specializations
    talents: List[str] = Field(default_factory=list, description="Selected talents")
    specializations: List[str] = Field(default_factory=list, description="Selected specializations")

    # Equipment
    equipment: Equipment = Field(default_factory=Equipment)

    # Magic system
    magic: Magic = Field(default_factory=Magic)

    # Extras
    extras: Extras = Field(default_factory=Extras)

    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Creation timestamp")
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Last update timestamp")

    @field_validator('char_class')
    @classmethod
    def validate_class(cls, v: str) -> str:
        """Validate character class is one of the four allowed classes."""
        allowed_classes = ['Envoy', 'Mage', 'Rogue', 'Warrior']
        if v not in allowed_classes:
            raise ValueError(f'Character class must be one of: {", ".join(allowed_classes)}')
        return v


class CharacterCreate(BaseModel):
    """Model for creating a new character (without ID and timestamps)."""
    name: str = Field(..., min_length=1, max_length=100)
    player_name: Optional[str] = Field(default=None, max_length=100)
    char_class: str
    background: Optional[str] = None
    level: int = Field(default=1, ge=1, le=20)
    stats: Stats = Field(default_factory=Stats)

    @field_validator('char_class')
    @classmethod
    def validate_class(cls, v: str) -> str:
        """Validate character class."""
        allowed_classes = ['Envoy', 'Mage', 'Rogue', 'Warrior']
        if v not in allowed_classes:
            raise ValueError(f'Character class must be one of: {", ".join(allowed_classes)}')
        return v


class CharacterUpdate(BaseModel):
    """Model for updating an existing character (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    player_name: Optional[str] = Field(None, max_length=100)
    char_class: Optional[str] = None
    background: Optional[str] = None
    level: Optional[int] = Field(None, ge=1, le=20)
    stats: Optional[Stats] = None
    hp_current: Optional[int] = Field(None, ge=0)
    hp_max: Optional[int] = Field(None, ge=0)
    mp_current: Optional[int] = Field(None, ge=0)
    mp_max: Optional[int] = Field(None, ge=0)
    foci_primary: Optional[Foci] = None
    foci_secondary: Optional[Foci] = None
    talents: Optional[List[str]] = None
    specializations: Optional[List[str]] = None
    equipment: Optional[Equipment] = None
    magic: Optional[Magic] = None
    extras: Optional[Extras] = None

    @field_validator('char_class')
    @classmethod
    def validate_class(cls, v: Optional[str]) -> Optional[str]:
        """Validate character class if provided."""
        if v is None:
            return v
        allowed_classes = ['Envoy', 'Mage', 'Rogue', 'Warrior']
        if v not in allowed_classes:
            raise ValueError(f'Character class must be one of: {", ".join(allowed_classes)}')
        return v


class CharacterSummary(BaseModel):
    """Lightweight character model for list views."""
    id: str
    name: str
    player_name: Optional[str]
    char_class: str
    level: int
    created_at: str
    updated_at: str
