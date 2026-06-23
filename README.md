# FAGE Character Generator

A desktop application for creating and managing Fantasy AGE (FAGE) tabletop RPG character sheets. Runs locally on your Windows PC — no internet connection or account required.

> 📖 **New here? Read the [User Manual (PDF)](User_Manual.pdf).** It walks through every feature with screenshots. This README is a quick reference; the manual is the full guide.

## Features

- **Character Management** — create, edit, save, and load characters
- **Complete Character Sheet** — stats, equipment, spells, talents, and inventory
- **PDF Export** — generate printable character sheets
- **Dice Rolling** — built-in 3d6 roller with stunt detection
- **Dark Mode** — toggle between light and dark themes

### Character System

- **Stats** — 9 core attributes with two levels of focus selection
- **Classes** — Envoy, Mage, Rogue, Warrior
- **Equipment** — weapons, armor, and inventory management
- **Magic** — spells, arcana, and MP tracking
- **Talents & Specializations** — class-based filtering
- **Level-Up Tables** — progression tracking by class

## Quick Start

The easiest way to run FAGE is the prebuilt Windows executable — no Python, Node, or setup required.

1. Go to the [**Releases**](../../releases) page and download the latest `FAGE.exe`.
2. Double-click `FAGE.exe`. The app starts and your default browser opens automatically at **http://127.0.0.1:8765**.
3. That's it. Create a character and start playing.

Your characters and game data are stored per-user under `%APPDATA%\FAGE` and persist between runs. To stop the app, close its console window.

> Windows SmartScreen may warn about an unrecognized publisher the first time you run it. Click **More info → Run anyway**.

## Ports

The app needs **one** local port, chosen to avoid conflicts with common services:

| Mode | Port | Notes |
|------|------|-------|
| **Prebuilt `FAGE.exe`** | `8765` | Localhost only; browser opens here automatically. |
| **Development** | `8000` (backend) + `5173` (frontend) | See [Development](#development). |

If `FAGE.exe` reports that port `8765` is already in use, close the other program using it (often a second copy of FAGE) and relaunch.

## Special Features (player-authored)

The **Special Features** card on the Main tab (under *Talents* and *Specializations*) shows
anything that doesn't fit elsewhere on the sheet — ancestry bonuses, character traits,
GM-granted boons, etc. The data is loaded directly from a CSV that you edit by hand.

**File location:** `backend/data/csv/Special_Features.csv` (in the source tree). For the
installed app, edit the copy under `%APPDATA%\FAGE\csv\Special_Features.csv`.

**Format:** three columns — `Source,Name,Effect`. One row per feature. Example:

```csv
Source,Name,Effect
Ancestry (Human),Ability Bonus,Intelligence +1
Background (Soldier),Tough,+2 HP per level
Trait,Lucky,Reroll one failed test per session
```

**To edit:**
1. Open the CSV in any text editor or spreadsheet app.
2. Add or remove rows, save the file (keep the header row).
3. In the app, click **Reload** in the Special Features card header — no restart needed.

## Development

Want to run from source or contribute? You'll need **Python 3.11+** and **Node.js 20+**.

```bat
git clone <repository-url>
cd FAGE-Generator

setup.bat        :: one-time: creates the Python venv and installs all dependencies
start-dev.bat    :: starts backend (port 8000) and frontend (port 5173) together
```

The frontend opens at **http://localhost:5173** with hot reload. (`setup.sh` / `start-dev.sh`
are the macOS/Linux equivalents.)

See **[DEVELOPMENT.md](DEVELOPMENT.md)** for architecture, code structure, testing, and the
PyInstaller build that produces `FAGE.exe`.

## Technology Stack

- **Backend** — FastAPI (Python 3.11+), Pandas, PyPDFForm, Pydantic, Uvicorn
- **Frontend** — Vue 3, Element Plus, Pinia, Vue Router, Vite
- **Packaging** — PyInstaller (single-file Windows executable)

## Project Structure

```
FAGE-Generator/
├── backend/              # FastAPI backend
│   ├── api/routes/       # API endpoints (character, data, actions, system)
│   ├── models/           # Pydantic data models
│   ├── utils/            # Dice, currency, PDF, storage, data loading
│   ├── data/csv/         # Game data (weapons, spells, talents, etc.)
│   ├── launcher.py       # Desktop entry point for the bundled app
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app
├── frontend/             # Vue 3 frontend
│   └── src/              # components, views, stores, composables, utils
├── fage.spec             # PyInstaller build spec
├── User_Manual.pdf       # Full user guide
├── DEVELOPMENT.md        # Developer guide
└── README.md             # This file
```

## AI Use Disclaimer

Majority of backend code was originally manually written in R, then manually translated into Python (etc) for this project. Claude was then used for linting and error detection.
The UI front end code was also originally written in R Shiny, then translated into Vue for strictly formatting purposes with assistance from Claude.
All code was manually reviewed, debugged, and approved before publishing.

## License

This project is for personal use. Fantasy AGE is a trademark of Green Ronin Publishing.

## Credits

- **Co-author**: Darkenedzone — Original R/Shiny App, concept, QA
- **Co-author**: Kylinblue — Python rewrite, development
- **Fantasy AGE System**: Green Ronin Publishing

---

**Version**: 0.10.1
**Last Updated**: 2026-06-23
