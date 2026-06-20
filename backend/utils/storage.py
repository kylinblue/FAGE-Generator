"""
Character storage utilities for FAGE Character Generator.
Provides file-based JSON storage for character data.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class CharacterStorage:
    """
    File-based storage for character data.

    Each character is saved as a JSON file in the storage/characters directory.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize character storage.

        Args:
            storage_dir: Directory for storing character files
                        (defaults to backend/storage/characters)
        """
        if storage_dir is None:
            # Default to storage/characters relative to this file
            base_path = Path(__file__).parent.parent
            storage_dir = base_path / "storage" / "characters"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, character_id: str) -> Path:
        """
        Get the file path for a character ID.

        Args:
            character_id: Character UUID

        Returns:
            Path to character JSON file
        """
        return self.storage_dir / f"{character_id}.json"

    def save(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a character to storage.

        Args:
            character_data: Character dictionary

        Returns:
            Saved character data with updated timestamp

        Raises:
            ValueError: If character data is missing ID
        """
        character_id = character_data.get('id')
        if not character_id:
            raise ValueError("Character data must include an 'id' field")

        # Update timestamp
        character_data['updated_at'] = datetime.utcnow().isoformat()

        # Write to file
        file_path = self._get_file_path(character_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, indent=2, ensure_ascii=False)

        return character_data

    def load(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a character from storage.

        Args:
            character_id: Character UUID

        Returns:
            Character dictionary, or None if not found
        """
        file_path = self._get_file_path(character_id)

        if not file_path.exists():
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def delete(self, character_id: str) -> bool:
        """
        Delete a character from storage.

        Args:
            character_id: Character UUID

        Returns:
            True if deleted, False if not found
        """
        file_path = self._get_file_path(character_id)

        if not file_path.exists():
            return False

        file_path.unlink()
        return True

    def list_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all characters in storage.

        Args:
            skip: Number of characters to skip (pagination)
            limit: Maximum number of characters to return

        Returns:
            List of character dictionaries
        """
        characters = []

        # Get all JSON files in storage directory
        json_files = sorted(
            self.storage_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True  # Most recently modified first
        )

        # Apply pagination
        json_files = json_files[skip:skip + limit]

        # Load each character
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    character_data = json.load(f)
                    characters.append(character_data)
            except Exception as e:
                # Log error but continue
                print(f"Error loading character from {file_path}: {e}")
                continue

        return characters

    def exists(self, character_id: str) -> bool:
        """
        Check if a character exists in storage.

        Args:
            character_id: Character UUID

        Returns:
            True if character exists, False otherwise
        """
        return self._get_file_path(character_id).exists()


# Global storage instance — honor STORAGE_DIR from settings/env so the
# launcher can redirect to a per-user app data directory.
from config import settings as _settings

_storage_dir = Path(_settings.STORAGE_DIR)
if not _storage_dir.is_absolute():
    _storage_dir = Path(__file__).resolve().parent.parent / _storage_dir

character_storage = CharacterStorage(storage_dir=_storage_dir)
