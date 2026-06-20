# FAGE Character Generator

A modern web application for creating and managing Fantasy AGE (FAGE) tabletop RPG character sheets. Built with FastAPI (Python) backend and Vue.js 3 frontend.

## Features

### Core Features
- **Character Management**: Create, edit, save, and load characters
- **Complete Character Sheet**: All stats, equipment, spells, talents, and inventory
- **PDF Export**: Generate printable character sheets
- **Local Storage**: Save characters to browser LocalStorage
- **Dice Rolling**: Built-in 3d6 dice roller with stunt detection
- **Dark Mode**: Toggle between light and dark themes

### Character System
- **Stats**: 9 core attributes with focus selection (two levels)
- **Classes**: Envoy, Mage, Rogue, Warrior
- **Equipment**: Weapons, armor, and inventory management
- **Magic System**: Spells, arcana, and MP tracking
- **Talents & Specializations**: Class-based filtering
- **Level-Up Tables**: Progression tracking by class

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Runtime environment
- **Pandas** - Data processing for CSV files
- **PyPDFForm** - Fillable AcroForm PDF generation
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Element Plus** - UI component library
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Build tool and dev server

## Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- OR: Python 3.11+, Node.js 20+, and npm

### Option 1: Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd FAGE-pyGenerator
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend + API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**:
   ```bash
   python main.py
   ```
   Or with Uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will be available at http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at http://localhost:5173

4. **Build for production**:
   ```bash
   npm run build
   ```

## Project Structure

```
FAGE-pyGenerator/
├── backend/                    # FastAPI backend
│   ├── api/                   # API routes
│   │   └── routes/
│   │       ├── character.py   # Character CRUD
│   │       ├── data.py        # CSV data endpoints
│   │       ├── actions.py     # Dice rolls, PDF export
│   │       └── utils.py       # Utilities
│   ├── models/                # Pydantic models
│   │   ├── character.py
│   │   └── inventory.py
│   ├── utils/                 # Utility functions
│   │   ├── dice.py           # Dice rolling
│   │   ├── currency.py       # Currency calculations
│   │   ├── pdf.py            # PDF generation
│   │   └── logger.py         # Logging configuration
│   ├── data/                  # Static data
│   │   └── csv/              # Game data CSV files
│   ├── storage/               # Saved characters
│   ├── generated_pdfs/        # Temporary PDF storage
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Configuration
│   └── requirements.txt      # Python dependencies
│
├── frontend/                  # Vue.js frontend
│   ├── src/
│   │   ├── components/       # Reusable Vue components
│   │   ├── views/            # Page components (tabs)
│   │   ├── stores/           # Pinia state management
│   │   ├── composables/      # Vue composables
│   │   ├── utils/            # Utility functions
│   │   ├── assets/           # Static assets
│   │   ├── router/           # Vue Router config
│   │   ├── App.vue           # Root component
│   │   └── main.js           # App entry point
│   ├── public/               # Public static files
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose configuration
├── .dockerignore
├── README.md                  # This file
├── DEVELOPMENT.md             # Developer guide
└── MIGRATION-PLAN.md          # Migration documentation
```

## API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key Endpoints

#### Character Management
- `POST /api/characters` - Create character
- `GET /api/characters/{id}` - Get character
- `PUT /api/characters/{id}` - Update character
- `DELETE /api/characters/{id}` - Delete character
- `GET /api/characters` - List all characters

#### Data Retrieval
- `GET /api/data/backgrounds` - Get backgrounds
- `GET /api/data/armor` - Get armor list
- `GET /api/data/weapons/melee` - Get melee weapons
- `GET /api/data/weapons/ranged` - Get ranged weapons
- `GET /api/data/foci` - Get foci by stat
- `GET /api/data/talents?char_class={class}` - Get talents
- `GET /api/data/spells?arcana={arcana}` - Get spells
- `GET /api/data/stunts` - Get stunts list
- `GET /api/data/levelup/{class_name}` - Get level-up table

#### Actions
- `POST /api/roll/dice` - Roll 3d6
- `POST /api/roll/spell` - Roll spell casting
- `POST /api/characters/{id}/export` - Export character to PDF

## Special Features (player-authored)

The **Special Features** card on the Main tab (under *Talents* and *Specializations*) shows
anything that doesn't fit elsewhere on the sheet — ancestry bonuses, character traits,
GM-granted boons, etc. The data is loaded directly from a CSV that you edit by hand.

**File location:** `backend/data/csv/Special_Features.csv`

**Format:** three columns — `Source,Name,Effect`. One row per feature. Example:

```csv
Source,Name,Effect
Ancestry (Human),Ability Bonus,Intelligence +1
Background (Soldier),Tough,+2 HP per level
Trait,Lucky,Reroll one failed test per session
```

**To edit:**
1. Open `backend/data/csv/Special_Features.csv` in any text editor or spreadsheet app.
2. Add or remove rows, save the file (keep the header row).
3. In the app, click **Reload** in the Special Features card header — no server restart needed.

## Configuration

### Environment Variables

Backend configuration via environment variables or `.env` file:

```bash
# API Settings
API_TITLE="FAGE Character Generator API"
API_VERSION="2.0.0"

# Server Settings
HOST=0.0.0.0
PORT=8000
RELOAD=true

# CORS Settings (add production frontend URL)
CORS_ORIGINS=["http://localhost:5173","http://localhost:8000"]

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=       # Optional log file path

# Storage
STORAGE_DIR=storage/characters
CSV_DIR=data/csv
```

Frontend configuration via `.env.development` or `.env.production`:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

## Docker Deployment

### Build the Docker Image

```bash
docker build -t fage-generator .
```

### Run the Container

```bash
docker run -p 8000:8000 \
  -v fage-data:/app/backend/storage/characters \
  -e LOG_LEVEL=INFO \
  fage-generator
```

### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

## Data Persistence

### Docker Volumes
- `character-data` - Saves character JSON files
- `pdf-data` - Stores generated PDFs (temporary)

### LocalStorage (Frontend)
- Characters are also saved to browser LocalStorage
- Survives page refreshes
- Limited to ~10MB per domain

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development instructions including:
- Setting up the development environment
- Code structure and patterns
- Testing guidelines
- Contributing guidelines

## Migration from R/Shiny

This is a complete rewrite from the original R/Shiny application. See [MIGRATION-PLAN.md](MIGRATION-PLAN.md) for:
- Technology mapping (R/Shiny → FastAPI/Vue)
- Feature parity checklist
- Architecture decisions
- Implementation phases

## Troubleshooting

### Backend Issues

**Port already in use**:
```bash
# Find and kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

**CSV files not found**:
Ensure CSV files are in `backend/data/csv/` directory.

### Frontend Issues

**Module not found**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**API connection refused**:
- Verify backend is running on http://localhost:8000
- Check CORS settings in `backend/config.py`
- Verify `VITE_API_BASE_URL` in frontend `.env` file

### Docker Issues

**Build fails**:
```bash
# Clear Docker cache and rebuild
docker-compose down -v
docker system prune -a
docker-compose up --build
```

**Permission issues**:
```bash
# Fix file permissions (Linux/Mac)
sudo chown -R $USER:$USER .
```

## AI Use Disclaimer

Majority of backend code was originally manually written in R, then manually translated into Python (etc) for this project. Claude was then used for linting and error detection
The UI front end code was also originally written in R Shiny, then translated into Vue for strictly formatting purposes with assistance from Claude. 
All code was manually reviewed, debugged, and approved before publishing


## License

This project is for personal use. Fantasy AGE is a trademark of Green Ronin Publishing.

## Credits

- **Original R/Shiny App**: [Your Name]
- **FastAPI Rewrite**: Developed with Claude Code
- **Fantasy AGE System**: Green Ronin Publishing

## Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Check the API documentation at `/docs`
4. Create an issue on GitHub (if applicable)

## Roadmap

Future enhancements:
- [ ] User authentication and cloud storage
- [ ] Character sharing via unique URLs
- [ ] Mobile-responsive improvements
- [ ] Print-optimized PDF layouts
- [ ] Campaign management features
- [ ] Additional game systems support
- [ ] Offline PWA support

---

**Version**: 2.0.0
**Last Updated**: 2026-01-28
