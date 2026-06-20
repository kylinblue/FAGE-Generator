# FAGE Character Generator - Development Guide

This guide provides detailed instructions for developers working on the FAGE Character Generator project.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Architecture](#project-architecture)
3. [Development Workflow](#development-workflow)
4. [Code Style and Standards](#code-style-and-standards)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Common Tasks](#common-tasks)
8. [Contributing](#contributing)

---

## Development Environment Setup

### Prerequisites

- **Python 3.11+**: Backend runtime
- **Node.js 20+**: Frontend development
- **npm 10+**: Package manager
- **Git**: Version control
- **Docker** (optional): For containerized development
- **VS Code** (recommended): IDE with Python and Vue extensions

### Initial Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd FAGE-pyGenerator
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
cp .env.example .env
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env.development
```

#### 4. Verify Setup

**Backend**:
```bash
cd backend
python main.py
# Should start on http://localhost:8000
# Check http://localhost:8000/docs
```

**Frontend**:
```bash
cd frontend
npm run dev
# Should start on http://localhost:5173
```

---

## Project Architecture

### Backend Architecture (FastAPI)

```
backend/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── api/                   # API layer
│   └── routes/
│       ├── character.py   # Character CRUD operations
│       ├── data.py        # Static data endpoints (CSV)
│       ├── actions.py     # Dice rolls, PDF export
│       └── utils.py       # Utility endpoints
├── models/                # Data models (Pydantic)
│   ├── character.py       # Character, Stats, Equipment
│   └── inventory.py       # Inventory, Currency
├── utils/                 # Business logic
│   ├── dice.py           # Dice rolling algorithms
│   ├── currency.py       # Currency calculations
│   ├── pdf.py            # PDF generation (PyPDFForm fillable AcroForm)
│   └── logger.py         # Logging configuration
└── data/
    └── csv/              # Game data (weapons, spells, etc.)
```

#### Key Patterns

**Dependency Injection**: FastAPI's dependency system for shared resources
**Pydantic Models**: Type-safe data validation
**Async/Await**: Asynchronous request handling
**Router-based**: Modular route organization

### Frontend Architecture (Vue 3)

```
frontend/src/
├── main.js                # App initialization
├── App.vue               # Root component
├── router/
│   └── index.js          # Vue Router configuration
├── stores/               # Pinia state management
│   ├── character.js      # Character state
│   ├── data.js           # CSV data caching
│   └── ui.js             # UI state (modals, theme)
├── views/                # Page components (routed)
│   ├── MainTab.vue       # Stats & equipment
│   ├── MagicTab.vue      # Spells & MP
│   ├── InventoryTab.vue  # Inventory & currency
│   └── LevelUpTab.vue    # Progression tables
├── components/           # Reusable components
│   ├── StatCard.vue      # Stat input with foci
│   ├── WeaponTable.vue   # Weapon selection
│   ├── DiceRoller.vue    # Dice rolling UI
│   └── ...
├── composables/          # Vue Composition API helpers
│   ├── useCharacter.js   # Character operations
│   ├── useData.js        # Data fetching
│   └── useDice.js        # Dice rolling logic
└── utils/
    ├── api.js            # Axios instance
    └── calculations.js   # HP/MP calculations
```

#### Key Patterns

**Composition API**: Modern Vue 3 style
**Pinia Stores**: Centralized state management
**Composables**: Reusable logic extraction
**Component-based**: Modular UI components

---

## Development Workflow

### Running Development Servers

**Option 1: Separate Terminals**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**Option 2: Docker Compose (with hot reload)**

```bash
# Edit docker-compose.yml to mount source directories
docker-compose up
```

### Making Changes

#### Backend Changes

1. **Create/modify API endpoint**:
   - Add route handler in appropriate file (`api/routes/`)
   - Define Pydantic models if needed
   - Update OpenAPI docs (automatic with FastAPI)
   - Test endpoint via Swagger UI at `/docs`

2. **Add business logic**:
   - Create utility functions in `utils/`
   - Write pure functions (no side effects)
   - Add type hints for all parameters

3. **Update data models**:
   - Modify Pydantic models in `models/`
   - Add validation rules
   - Update related endpoints

Example:
```python
# backend/api/routes/character.py
from fastapi import APIRouter, HTTPException
from models.character import Character

router = APIRouter()

@router.get("/{character_id}", response_model=Character)
async def get_character(character_id: str):
    # Implementation
    pass
```

#### Frontend Changes

1. **Create/modify Vue component**:
   - Use Composition API with `<script setup>`
   - Props for inputs, emits for outputs
   - Use Element Plus components

2. **Update state management**:
   - Modify Pinia stores in `stores/`
   - Use reactive refs and computed properties

3. **Add new routes**:
   - Update `router/index.js`
   - Create corresponding view component

Example:
```vue
<!-- frontend/src/components/StatCard.vue -->
<script setup>
import { computed } from 'vue'

const props = defineProps({
  statName: String,
  value: Number
})

const emit = defineEmits(['update:value'])

const modifier = computed(() => Math.floor((props.value - 10) / 2))
</script>

<template>
  <el-card>
    <h3>{{ statName }}</h3>
    <el-input-number
      :model-value="value"
      @update:model-value="emit('update:value', $event)"
    />
    <p>Modifier: {{ modifier }}</p>
  </el-card>
</template>
```

### Hot Reload

- **Backend**: Uvicorn auto-reloads on file changes (if `RELOAD=true`)
- **Frontend**: Vite HMR (Hot Module Replacement) updates instantly

---

## Code Style and Standards

### Python (Backend)

**Style Guide**: PEP 8

**Key Rules**:
- Use type hints for all function parameters and returns
- Docstrings for all public functions (Google style)
- Snake_case for variables and functions
- PascalCase for classes
- Use async/await for I/O operations
- Maximum line length: 100 characters

Example:
```python
async def calculate_hp(constitution: int, level: int) -> int:
    """
    Calculate maximum hit points.

    Args:
        constitution: Constitution stat value
        level: Character level

    Returns:
        Maximum HP value
    """
    base_hp = 10 + constitution
    level_bonus = (level - 1) * 5
    return base_hp + level_bonus
```

**Tools**:
```bash
# Format code
pip install black
black backend/

# Lint code
pip install flake8
flake8 backend/

# Type checking
pip install mypy
mypy backend/
```

### JavaScript/Vue (Frontend)

**Style Guide**: Vue.js Style Guide (Priority A + B)

**Key Rules**:
- Use Composition API with `<script setup>`
- CamelCase for component names (PascalCase in templates)
- camelCase for variables and functions
- UPPER_SNAKE_CASE for constants
- Use `ref` for primitive values, `reactive` for objects
- Props validation with types
- Emit events with descriptive names

Example:
```vue
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  initialValue: {
    type: Number,
    required: true,
    default: 10
  }
})

const emit = defineEmits(['update', 'save'])

const count = ref(props.initialValue)

const doubled = computed(() => count.value * 2)

function handleClick() {
  emit('update', count.value)
}
</script>
```

**Tools**:
```bash
# Lint
npm run lint  # (if configured)

# Format
npx prettier --write "src/**/*.{js,vue}"
```

---

## Testing

### Backend Testing

**Framework**: pytest

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_dice.py

# Run specific test
pytest tests/test_dice.py::test_roll_3d6
```

**Example Test**:
```python
# backend/tests/test_dice.py
import pytest
from utils.dice import roll_3d6

def test_roll_3d6():
    dice, total, has_stunt = roll_3d6()

    assert len(dice) == 3
    assert all(1 <= d <= 6 for d in dice)
    assert total == sum(dice)
    assert isinstance(has_stunt, bool)

def test_stunt_detection():
    # Test with known values (requires mocking random)
    pass
```

**Testing Best Practices**:
- Test one thing per test function
- Use descriptive test names
- Use fixtures for shared setup
- Mock external dependencies
- Aim for >80% coverage

### Frontend Testing

**Framework**: Vitest (recommended for Vite projects)

```bash
cd frontend

# Install testing dependencies
npm install -D vitest @vue/test-utils

# Run tests
npm run test

# Run with UI
npm run test:ui
```

**Example Test**:
```javascript
// frontend/src/components/__tests__/StatCard.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import StatCard from '../StatCard.vue'

describe('StatCard', () => {
  it('renders stat name', () => {
    const wrapper = mount(StatCard, {
      props: {
        statName: 'Strength',
        value: 15
      }
    })

    expect(wrapper.text()).toContain('Strength')
  })

  it('emits update event on value change', async () => {
    const wrapper = mount(StatCard, {
      props: {
        statName: 'Strength',
        value: 15
      }
    })

    await wrapper.vm.$emit('update:value', 16)

    expect(wrapper.emitted('update:value')).toBeTruthy()
    expect(wrapper.emitted('update:value')[0]).toEqual([16])
  })
})
```

---

## Debugging

### Backend Debugging

**Print Debugging**:
```python
from utils.logger import logger

logger.debug(f"Character data: {character}")
logger.info(f"Processing character ID: {character_id}")
logger.error(f"Failed to load character: {e}")
```

**Interactive Debugger** (pdb):
```python
import pdb; pdb.set_trace()  # Breakpoint
```

**VS Code Debugging**:

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": {"PYTHONPATH": "${workspaceFolder}/backend"}
    }
  ]
}
```

### Frontend Debugging

**Browser DevTools**:
- Vue DevTools extension (Chrome/Firefox)
- Console logging: `console.log()`
- Network tab for API calls
- Vue tab for component inspection

**Reactive Debugging**:
```vue
<script setup>
import { watch } from 'vue'

watch(() => character.value, (newVal) => {
  console.log('Character changed:', newVal)
}, { deep: true })
</script>
```

**VS Code Debugging**:

Add to `.vscode/launch.json`:
```json
{
  "type": "chrome",
  "request": "launch",
  "name": "Vue: Chrome",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend/src"
}
```

---

## Common Tasks

### Adding a New Data CSV File

1. Add CSV file to `backend/data/csv/`
2. Create endpoint in `backend/api/routes/data.py`:
   ```python
   @router.get("/new-data")
   async def get_new_data():
       df = pd.read_csv("data/csv/new-data.csv")
       return df.to_dict('records')
   ```
3. Update frontend data store to fetch new data
4. Update relevant components to use the data

### Adding a New Character Attribute

1. Update `backend/models/character.py`:
   ```python
   class Character(BaseModel):
       # ... existing fields ...
       new_attribute: str = ""
   ```
2. Update frontend character store
3. Add UI component to display/edit the attribute
4. Update PDF template if needed

### Updating the PDF Template

1. Modify `backend/utils/pdf.py`
2. Update HTML template structure
3. Test with sample character data
4. Verify PDF output quality

### Adding a New API Endpoint

1. Define route in appropriate file in `backend/api/routes/`
2. Add Pydantic models if needed
3. Implement business logic
4. Test via Swagger UI
5. Update frontend to call the endpoint

---

## Contributing

### Git Workflow

1. Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Add new feature: description"
   ```

3. Push to remote:
   ```bash
   git push origin feature/new-feature
   ```

4. Create pull request (if applicable)

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Example**:
```
feat: Add spell filtering by arcana

- Added arcana filter parameter to GET /api/data/spells
- Updated SpellTable component to use filter
- Added arcana selection in MagicTab

Closes #123
```

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No console errors or warnings
- [ ] API documentation updated (if applicable)
- [ ] Tested in both light and dark mode
- [ ] Tested on mobile viewport

---

## Performance Optimization

### Backend

- Use async/await for I/O operations
- Cache CSV data in memory
- Use Pydantic's `model_validate` for faster validation
- Profile with `cProfile` for bottlenecks

### Frontend

- Use `computed` for derived state
- Lazy load routes with `() => import()`
- Use `v-show` instead of `v-if` for frequently toggled elements
- Debounce expensive operations
- Use virtual scrolling for long lists (Element Plus provides this)

---

## Troubleshooting Development Issues

### Backend won't start

1. Check Python version: `python --version`
2. Verify virtual environment is activated
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check for port conflicts: `netstat -ano | findstr :8000`

### Frontend won't start

1. Delete `node_modules` and `package-lock.json`, reinstall
2. Clear Vite cache: `rm -rf node_modules/.vite`
3. Check Node version: `node --version`

### CORS errors

1. Verify backend CORS settings in `config.py`
2. Check frontend API base URL in `.env.development`
3. Ensure backend is running on expected port

### PDF generation fails

1. Confirm `backend/data/Blank-Sheet.pdf` exists (bundled with the repo).
2. Verify PyPDFForm is installed: `pip show PyPDFForm`.
3. Check logs for specific error messages.

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue.js 3 Docs](https://vuejs.org/)
- [Element Plus Docs](https://element-plus.org/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [PyPDFForm Docs](https://chinapandaman.github.io/PyPDFForm/)

### Tools
- [Swagger UI](http://localhost:8000/docs) - API testing
- [Vue DevTools](https://devtools.vuejs.org/) - Vue debugging
- [Postman](https://www.postman.com/) - API testing

---

**Happy Coding!** 🚀
