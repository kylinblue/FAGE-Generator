"""
Simple test script for PDF generation functionality.
Tests the PyPDFForm-based fillable-PDF generation system.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.pdf import generate_character_pdf

# Sample character data for testing
test_character = {
    "name": "Test Character",
    "player_name": "Test Player",
    "char_class": "Warrior",
    "level": 5,
    "background": "Noble",
    "stats": {
        "Accuracy": 12,
        "Communication": 10,
        "Constitution": 14,
        "Dexterity": 11,
        "Fighting": 15,
        "Intelligence": 9,
        "Perception": 13,
        "Strength": 16,
        "Willpower": 10
    },
    "foci_primary": {
        "Fighting": ["Heavy Blades"],
        "Strength": ["Climbing"],
        "Accuracy": [],
        "Communication": [],
        "Constitution": [],
        "Dexterity": [],
        "Intelligence": [],
        "Perception": [],
        "Willpower": []
    },
    "foci_secondary": {
        "Accuracy": [],
        "Communication": [],
        "Constitution": [],
        "Dexterity": [],
        "Fighting": [],
        "Intelligence": [],
        "Perception": [],
        "Strength": [],
        "Willpower": []
    },
    "hp_current": 34,
    "hp_max": 34,
    "mp_current": 9,
    "mp_max": 9,
    "equipment": {
        "armor": "Light Leather",
        "melee_weapons": [
            {
                "Weapon": "Longsword",
                "Group": "Heavy Blades",
                "Damage": "2d6",
                "Special": "Versatile"
            }
        ],
        "ranged_weapons": [
            {
                "Weapon": "Longbow",
                "Group": "Bows",
                "Damage": "1d6+3",
                "Short Range": "32",
                "Long Range": "65",
                "Reload": "Free"
            }
        ]
    },
    "talents": ["Armor Training (Journeyman)", "Weapon Groups (Heavy Blades)"],
    "specializations": ["Knight"],
    "magic": {
        "arcana": [],
        "spells": []
    },
    "extras": {
        "inventory": [
            {"item": "Rope (50 ft)", "quantity": 1},
            {"item": "Torch", "quantity": 5},
            {"item": "Rations", "quantity": 7}
        ],
        "currency": {
            "gold": 25,
            "silver": 50,
            "copper": 100
        },
        "stunts": ["Mighty Blow"],
        "backstory": "A noble warrior seeking glory and honor in battle.",
        "photo": None
    }
}


def main():
    print("=" * 60)
    print("FAGE PDF Generation Test")
    print("=" * 60)
    print()

    print("Testing PDF generation with sample character data...")
    print(f"Character: {test_character['name']}")
    print(f"Class: {test_character['char_class']} (Level {test_character['level']})")
    print()

    try:
        # Generate PDF
        print("Generating PDF...")
        pdf_path = generate_character_pdf(test_character)

        print("[SUCCESS] PDF generated successfully!")
        print(f"[FILE] Saved to: {pdf_path}")
        print()

        # Check file exists and get size
        from pathlib import Path
        pdf_file = Path(pdf_path)
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size
            print(f"File size: {file_size:,} bytes ({file_size / 1024:.2f} KB)")
            print()
            print("[PASS] Test PASSED - PDF file created successfully")
        else:
            print("[FAIL] Test FAILED - PDF file not found")
            return 1

    except Exception as e:
        print("[FAIL] Test FAILED with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        print()
        print("Full traceback:")
        traceback.print_exc()
        return 1

    print()
    print("=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
