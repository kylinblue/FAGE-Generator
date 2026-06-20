# FAGE Character Generator - Backend API

FastAPI-based REST API for the Fantasy AGE Character Generator.

## Features

- **Character Management**: Full CRUD operations for character sheets
- **Game Data**: Access to weapons, spells, talents, backgrounds, and more
- **Dice Rolling**: 3d6 rolls with stunt detection
- **Magic System**: Spell casting with target number checks
- **Currency Calculations**: Automatic conversion between gold/silver/copper

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

### Running the Server

Development mode (with auto-reload):
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or using the main.py directly:
```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## API Documentation

### Character Endpoints

- `POST /api/characters` - Create new character
- `GET /api/characters/{id}` - Get character by ID
- `PUT /api/characters/{id}` - Update character
- `DELETE /api/characters/{id}` - Delete character
- `GET /api/characters` - List all characters

### Data Endpoints

- `GET /api/data/backgrounds` - Get backgrounds
- `GET /api/data/armor` - Get armor list
- `GET /api/data/weapons/melee` - Get melee weapons
- `GET /api/data/weapons/ranged` - Get ranged weapons
- `GET /api/data/foci` - Get foci by stat
- `GET /api/data/talents?char_class=Warrior` - Get talents (filtered)
- `GET /api/data/specializations?char_class=Mage` - Get specializations
- `GET /api/data/arcana` - Get arcana list
- `GET /api/data/spells?arcana=Fire` - Get spells (filtered)
- `GET /api/data/stunts` - Get stunts list
- `GET /api/data/levelup/{class_name}` - Get level progression table

### Action Endpoints

- `POST /api/roll/dice` - Roll 3d6 with modifier
- `POST /api/roll/spell` - Roll spell casting
- `POST /api/roll/attack` - Roll weapon attack
- `POST /api/currency/calculate` - Calculate currency conversion

### Utility Endpoints

- `GET /` - API information
- `GET /health` - Health check

## Project Structure

```
backend/
├── api/
│   └── routes/
│       ├── character.py    # Character CRUD
│       ├── data.py         # CSV data access
│       └── actions.py      # Dice, spells, currency
├── models/
│   └── character.py        # Pydantic models
├── utils/
│   ├── character.py        # Character utilities
│   ├── currency.py         # Currency calculations
│   ├── data_loader.py      # CSV loading
│   ├── dice.py             # Dice rolling
│   ├── filters.py          # Data filtering
│   └── storage.py          # File-based storage
├── data/
│   └── csv/                # Game data files
├── storage/
│   └── characters/         # Saved characters (JSON)
├── config.py               # Settings
├── main.py                 # FastAPI app
└── requirements.txt        # Dependencies
```

## Development

### Testing the API

Visit http://localhost:8000/docs for interactive API testing with Swagger UI.

Example requests:

**Create a character:**
```bash
curl -X POST "http://localhost:8000/api/characters" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Thorin Ironforge",
    "char_class": "Warrior",
    "stats": {"Strength": 15, "Fighting": 14}
  }'
```

**Roll dice:**
```bash
curl -X POST "http://localhost:8000/api/roll/dice" \
  -H "Content-Type: application/json" \
  -d '{"modifier": 5}'
```

**Get talents for Warriors:**
```bash
curl "http://localhost:8000/api/data/talents?char_class=Warrior"
```

### Adding New Endpoints

1. Create route in `api/routes/`
2. Add models in `models/` if needed
3. Add utilities in `utils/` if needed
4. Register router in `main.py`

## Configuration

Edit `.env` or set environment variables:

- `API_TITLE` - API name
- `API_VERSION` - Version string
- `CORS_ORIGINS` - Allowed frontend origins (comma-separated)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `RELOAD` - Auto-reload on changes (default: true)

## Storage

Characters are saved as JSON files in `storage/characters/`. Each character has a UUID-based filename.

## Week 1 Status

✅ FastAPI project structure
✅ Pydantic data models
✅ CSV loading utilities
✅ Data routes (backgrounds, armor, weapons, foci, talents, spells, etc.)
✅ Character CRUD endpoints
✅ Dice rolling and action routes
✅ CORS configuration
✅ Swagger documentation

## Next Steps (Week 2+)

- Frontend Vue.js integration
- Real-time validation
- Advanced search/filtering
- Testing suite
