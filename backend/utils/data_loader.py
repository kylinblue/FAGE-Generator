"""
CSV data loading utilities for FAGE Character Generator.
Provides cached access to all game data (weapons, spells, talents, etc.).
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from functools import lru_cache

from config import settings


class DataLoader:
    """
    Singleton class for loading and caching CSV data.

    All CSV files are loaded once and cached in memory for fast access.
    """

    _instance: Optional['DataLoader'] = None
    _data_cache: Dict[str, pd.DataFrame] = {}

    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the data loader (only once)."""
        if self._initialized:
            return

        # Determine the base path for CSV files. Honor CSV_DIR from settings
        # so the launcher can point at a writable per-user copy.
        csv_dir = Path(settings.CSV_DIR)
        if not csv_dir.is_absolute():
            csv_dir = Path(__file__).resolve().parent.parent / csv_dir
        self.base_path = csv_dir

        # CSV files to load
        self.csv_files = {
            "backgrounds": "Backgrounds.csv",
            "armor": "Armour.csv",
            "melee_weapons": "MeleeWeapons.csv",
            "ranged_weapons": "RangeWeapons.csv",
            "focus_list": "Focus-List.csv",
            "talents": "Talents.csv",
            "specializations": "Specs.csv",
            "arcana": "Arcana-List.csv",
            "spells": "Spell-List.csv",
            "stunts": "Stunts-list.csv",
            "special_features": "Special_Features.csv",
            # Class-specific progression files
            "envoy": "Envoy.csv",
            "mage": "Mage.csv",
            "rogue": "Rogue.csv",
            "warrior": "Warrior.csv"
        }

        self._initialized = True

    def _load_csv(self, key: str) -> pd.DataFrame:
        """
        Load a CSV file by key.

        Args:
            key: Key from csv_files dictionary

        Returns:
            DataFrame containing the CSV data

        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        if key in self._data_cache:
            return self._data_cache[key]

        filename = self.csv_files.get(key)
        if not filename:
            raise ValueError(f"Unknown data key: {key}")

        filepath = self.base_path / filename

        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        # Load CSV with pandas (handle BOM for UTF-8, preserve embedded newlines)
        df = pd.read_csv(filepath, encoding='utf-8-sig', quotechar='"', engine='python')

        # Fix embedded linebreaks in text fields for affected tables
        if key in ('talents', 'specializations', 'spells', 'envoy', 'mage', 'rogue', 'warrior'):
            df = df.apply(lambda col: col.map(
                lambda x: x.replace('\r\n', '<br><br>').replace('\n', '<br><br>') if isinstance(x, str) else x
            ))

        # Cache the dataframe
        self._data_cache[key] = df

        return df

    def get_backgrounds(self) -> List[str]:
        """Get list of available backgrounds."""
        df = self._load_csv("backgrounds")
        # Assuming the CSV has a 'Background' column
        if 'Background' in df.columns:
            return df['Background'].dropna().tolist()
        # If the structure is different, return first column
        return df.iloc[:, 0].dropna().tolist()

    def get_armor(self) -> List[Dict[str, Any]]:
        """Get all armor with stats."""
        df = self._load_csv("armor")
        return df.to_dict('records')

    def get_melee_weapons(self) -> List[Dict[str, Any]]:
        """Get all melee weapons with stats."""
        df = self._load_csv("melee_weapons")
        for col in ('BonusHit', 'BonusDamage'):
            if col in df.columns:
                df[col] = df[col].fillna(0)
        return df.to_dict('records')

    def get_ranged_weapons(self) -> List[Dict[str, Any]]:
        """Get all ranged weapons with stats."""
        df = self._load_csv("ranged_weapons")
        for col in ('BonusHit', 'BonusDamage'):
            if col in df.columns:
                df[col] = df[col].fillna(0)
        return df.to_dict('records')

    def get_foci(self) -> Dict[str, List[str]]:
        """
        Get all foci organized by stat.

        Returns:
            Dictionary mapping stat names to lists of available foci
            Example: {"Fighting": ["Brawling", "Heavy Blades", ...]}
        """
        df = self._load_csv("focus_list")

        # Each column is a stat, values are foci for that stat
        foci_dict = {}
        for col in df.columns:
            # Remove NaN values and convert to list
            foci_dict[col] = df[col].dropna().tolist()

        return foci_dict

    def get_talents(self, char_class: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get talents, optionally filtered by class.

        Args:
            char_class: Character class to filter by (None = all talents)

        Returns:
            List of talent dictionaries
        """
        df = self._load_csv("talents")

        if char_class:
            # Filter by Class1 or Class2 columns
            mask = (
                (df['Class1'] == char_class) |
                (df['Class2'] == char_class) |
                (df['Class1'] == 'Any') |
                (df['Class2'] == 'Any')
            )
            df = df[mask]

        return df.to_dict('records')

    def get_specializations(self, char_class: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get specializations, optionally filtered by class.

        Args:
            char_class: Character class to filter by (None = all specs)

        Returns:
            List of specialization dictionaries
        """
        df = self._load_csv("specializations")

        if char_class:
            # Filter by Class1 or Class2 columns (if they exist)
            if 'Class1' in df.columns:
                mask = (
                    (df['Class1'] == char_class) |
                    (df.get('Class2', '') == char_class) |
                    (df['Class1'] == 'Any')
                )
                df = df[mask]

        return df.to_dict('records')

    def get_arcana(self) -> List[str]:
        """Get list of available arcana."""
        df = self._load_csv("arcana")
        # Assuming the CSV has an 'Arcana' column
        if 'Arcana' in df.columns:
            return df['Arcana'].dropna().tolist()
        # If different structure, return first column
        return df.iloc[:, 0].dropna().tolist()

    def get_spells(self, arcana: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get spells, optionally filtered by arcana.

        Args:
            arcana: Arcana to filter by (None = all spells)

        Returns:
            List of spell dictionaries
        """
        df = self._load_csv("spells")

        if arcana:
            df = df[df['Arcana'] == arcana]

        return df.to_dict('records')

    def get_stunts(self) -> List[Dict[str, Any]]:
        """Get all stunts."""
        df = self._load_csv("stunts")
        return df.to_dict('records')

    def get_special_features(self) -> List[Dict[str, Any]]:
        """Get all user-authored special features (ancestry bonuses, traits, etc.)."""
        # Reload from disk every call so manual edits to the CSV show up without restart.
        self._data_cache.pop("special_features", None)
        df = self._load_csv("special_features")
        df = df.dropna(how='all')
        return df.fillna('').to_dict('records')

    def get_class_progression(self, char_class: str) -> List[Dict[str, Any]]:
        """
        Get level-up progression table for a class.

        Args:
            char_class: Character class (Envoy, Mage, Rogue, Warrior)

        Returns:
            List of level progression dictionaries
        """
        key = char_class.lower()
        if key not in self.csv_files:
            raise ValueError(f"Unknown class: {char_class}")

        df = self._load_csv(key)
        return df.to_dict('records')

    def reload_data(self):
        """Clear cache and reload all data (useful for development)."""
        self._data_cache.clear()


# Global instance
data_loader = DataLoader()
