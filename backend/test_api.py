"""
Quick test script to validate the API is working.
Tests basic endpoints and data loading.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from config import settings
        from api.routes import character, data, actions
        from models.character import Character
        from utils.data_loader import data_loader
        from utils.dice import roll_3d6
        from utils.currency import calculate_currency
        print("[PASS] All imports successful")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        traceback.print_exc()
        return False


def test_data_loading():
    """Test that CSV data can be loaded."""
    print("\nTesting data loading...")
    try:
        from utils.data_loader import data_loader

        # Test loading backgrounds
        backgrounds = data_loader.get_backgrounds()
        print(f"  [PASS] Loaded {len(backgrounds)} backgrounds")

        # Test loading armor
        armor = data_loader.get_armor()
        print(f"  [PASS] Loaded {len(armor)} armor items")

        # Test loading foci
        foci = data_loader.get_foci()
        print(f"  [PASS] Loaded foci for {len(foci)} stats")

        # Test loading talents
        talents = data_loader.get_talents()
        print(f"  [PASS] Loaded {len(talents)} talents")

        # Test loading spells
        spells = data_loader.get_spells()
        print(f"  [PASS] Loaded {len(spells)} spells")

        return True
    except Exception as e:
        print(f"[FAIL] Data loading error: {e}")
        traceback.print_exc()
        return False


def test_models():
    """Test that Pydantic models work."""
    print("\nTesting models...")
    try:
        from models.character import Character, Stats

        # Create a test character
        character = Character(
            name="Test Character",
            char_class="Warrior",
            stats=Stats(Strength=15, Fighting=14)
        )

        print(f"  [PASS] Created character: {character.name}")
        print(f"  [PASS] Character ID: {character.id}")
        print(f"  [PASS] Class: {character.char_class}")

        return True
    except Exception as e:
        print(f"[FAIL] Model error: {e}")
        traceback.print_exc()
        return False


def test_utilities():
    """Test utility functions."""
    print("\nTesting utilities...")
    try:
        from utils.dice import roll_3d6
        from utils.currency import calculate_currency
        from utils.character import format_foci

        # Test dice rolling
        dice, total, has_stunt, stunt_points = roll_3d6()
        print(f"  [PASS] Dice roll: {dice} = {total} (Stunt: {has_stunt}, Stunt die: {stunt_points})")

        # Test currency calculation
        result = calculate_currency(250, 5, 0)
        print(f"  [PASS] Currency: 250c + 5s = {result['silver']}s {result['copper']}c")

        # Test focus formatting
        formatted = format_foci(["Brawling", "Swords"], ["Brawling"])
        print(f"  [PASS] Foci: {formatted}")

        return True
    except Exception as e:
        print(f"[FAIL] Utility error: {e}")
        traceback.print_exc()
        return False


def test_app_creation():
    """Test that FastAPI app can be created."""
    print("\nTesting FastAPI app creation...")
    try:
        from main import app

        print(f"  [PASS] App created: {app.title}")
        print(f"  [PASS] Version: {app.version}")
        print(f"  [PASS] Routes: {len(app.routes)} registered")

        return True
    except Exception as e:
        print(f"[FAIL] App creation error: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("FAGE Character Generator - Backend API Tests")
    print("=" * 60)

    tests = [
        test_imports,
        test_data_loading,
        test_models,
        test_utilities,
        test_app_creation
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"[FAIL] Test failed with exception: {e}")
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")

    if all(results):
        print("\n[SUCCESS] All tests passed! API is ready.")
        print("\nTo start the server:")
        print("  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\nThen visit:")
        print("  http://localhost:8000/docs")
        return 0
    else:
        print("\n[ERROR] Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
