# FAGE-pyGenerator Variable Dictionary

---

## Table of Contents

1. [Backend Configuration](#backend-configuration)
2. [Pydantic Models](#pydantic-models)
3. [Pinia Stores](#pinia-stores)
4. [API Request/Response Models](#api-requestresponse-models)
5. [CSV Data Schemas](#csv-data-schemas)
6. [Vue Component Props](#vue-component-props)

---

## Backend Configuration

**File:** `backend/config.py`

| Variable | Type | Default | Description |
|---|---|---|---|
| `HOST` | str | `"0.0.0.0"` | Uvicorn bind host |
| `PORT` | int | `8000` | Uvicorn listen port |
| `RELOAD` | bool | `True` | Auto-reload on file change (dev mode) |
| `STORAGE_DIR` | str | `"storage/characters"` | Directory for character JSON files |
| `CSV_DIR` | str | `"data/csv"` | Directory for game data CSV files |
| `LOG_LEVEL` | str | `"INFO"` | Logging level: DEBUG / INFO / WARNING / ERROR / CRITICAL |
| `LOG_FILE` | str | `""` | Log file path; empty = console only |
| `CORS_ORIGINS` | List[str] | `["http://localhost:5173", ...]` | Allowed CORS origins |

---

## Pydantic Models

**File:** `backend/models/character.py`

### Stats

Nine fields — `Accuracy`, `Communication`, `Constitution`, `Dexterity`, `Fighting`, `Intelligence`, `Perception`, `Strength`, `Willpower` — all `int`, range 0–20, default `0`.

### Foci

Ten fields mirroring stat names plus `Arcana`. Each is `List[str]` of selected focus names (e.g. `Fighting: ["Brawling", "Heavy Blades"]`). Used for both `foci_primary` and `foci_secondary`.

### Equipment

| Field | Type | Description |
|---|---|---|
| `armor` | Optional[str] | Equipped armor name |
| `melee_weapons` | List[str] | Equipped melee weapon names |
| `ranged_weapons` | List[str] | Equipped ranged weapon names |

### Magic

| Field | Type | Description |
|---|---|---|
| `arcana` | List[str] | Known arcana (e.g. `["Fire", "Air"]`) |
| `spells` | List[str] | Known spell names |

### Extras

| Field | Type | Description |
|---|---|---|
| `inventory` | List[{item: str, quantity: int}] | Carried items |
| `currency` | {gold, silver, copper: int ≥ 0} | Currency |
| `stunts` | List[str] | Selected stunt names |
| `backstory` | str | Backstory text |
| `relationships` | str | Relationships text |
| `goals_ties` | str | Goals and ties text |
| `extra_notes` | str | Freeform notes |

### Character (root model)

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | str | UUID, auto-generated | Unique identifier |
| `name` | str | 1–100 chars | Character name |
| `player_name` | Optional[str] | max 100 chars | Player's real name |
| `char_class` | str | `Envoy\|Mage\|Rogue\|Warrior` | Character class |
| `background` | Optional[str] | — | Chosen background |
| `level` | int | 1–20 | Character level |
| `ancestry` | Optional[str] | — | Character ancestry |
| `social_class` | Optional[str] | — | Social standing |
| `speed` | int | ≥ 0 | Movement speed |
| `defense` | int | ≥ 0 | Defense rating |
| `experience` | int | ≥ 0 | Total XP |
| `photo` | Optional[str] | Base64 | Portrait image |
| `stats` | Stats | — | Nine ability scores |
| `hp_current` / `hp_max` | int | ≥ 0 | Hit points |
| `mp_current` / `mp_max` | int | ≥ 0 | Magic points |
| `foci_primary` | Foci | — | Primary focus selections |
| `foci_secondary` | Foci | — | Secondary focus selections (level 11+) |
| `talents` | List[str] | — | Selected talent names |
| `specializations` | List[str] | — | Selected specialization names |
| `equipment` | Equipment | — | Armor and weapons |
| `magic` | Magic | — | Arcana and spells |
| `extras` | Extras | — | Inventory, currency, stunts, narrative |
| `created_at` / `updated_at` | str | ISO 8601 | Timestamps |

---

## Pinia Stores

### character store — `frontend/src/stores/character.js`

Single reactive `character` object. Fields mirror the Pydantic `Character` model with these frontend-specific notes:

- `char_class` defaults to `'Warrior'`
- Optional strings default to `''` (not `null`) on the frontend
- `stats` all default to `0`

#### Computed (getters)

| Name | Formula |
|---|---|
| `hpMax` | `Constitution + 10 + classBonus + (level-1)*4`; Warrior adds +5 |
| `mpMax` | Mage: `Intelligence + 10 + (level-1)*3`; Envoy: `floor((Intelligence+10)/2)`; others: `0` |

#### Actions

| Function | Signature | Description |
|---|---|---|
| `updateStat` | `(statName, value)` | Update one stat; recalculates HP/MP |
| `updatePrimaryFoci` | `(stat, string[])` | Replace primary foci for a stat |
| `updateSecondaryFoci` | `(stat, string[])` | Replace secondary foci for a stat |
| `updateExtras` | `(extras)` | Merge into extras section |
| `calculateFocusBonus` | `(stat, focusName?) → number` | `0` no focus; `+2` lvl 1–10; `+3` lvl 11+; `+4` double focus |
| `rollDice` | `(modifier?) → RollResult` | Roll 3d6 with optional modifier |
| `saveToLocalStorage` | `()` | Persist character to `localStorage` |
| `loadFromLocalStorage` | `(id) → boolean` | Load character by ID |
| `loadLastCharacter` | `() → boolean` | Load most recently saved character |
| `getAllSavedCharacters` | `() → Character[]` | All characters from `localStorage` |
| `deleteCharacter` | `(id)` | Remove character from `localStorage` |
| `reset` | `()` | Reset to initial state |

---

### data store — `frontend/src/stores/data.js`

Cached game data fetched from the API. All `fetch*` actions are async and skip the network call if data is already loaded.

#### State

| Variable | Type | Description |
|---|---|---|
| `backgrounds` | string[] | Background names |
| `armor` | object[] | Armor objects |
| `meleeWeapons` | object[] | Melee weapon objects |
| `rangedWeapons` | object[] | Ranged weapon objects |
| `foci` | `{stat: string[]}` | Focus names keyed by stat |
| `talents` | object[] | Talent objects |
| `specializations` | object[] | Specialization objects |
| `arcana` | string[] | Arcana names |
| `spells` | object[] | Spell objects |
| `stunts` | object[] | Stunt objects |
| `levelupTables` | `{className: object[]}` | Level progression per class |
| `loading` | `{[key]: boolean}` | Per-resource loading flags |

#### Actions

`fetch<Resource>()` pattern for each state key above (e.g. `fetchArmor()`, `fetchSpells(arcanaFilter?)`). Also:

| Function | Description |
|---|---|
| `fetchTalents(charClass?)` | Optionally filter by class |
| `fetchSpecializations(charClass?)` | Optionally filter by class |
| `fetchSpells(arcanaFilter?)` | Optionally filter by arcana |
| `fetchLevelupTable(className)` | Fetch one class's progression table |
| `fetchEssentialData()` | Batch-fetch backgrounds, armor, weapons |
| `clearCache()` | Reset all cached state |

---

### ui store — `frontend/src/stores/ui.js`

#### State

| Variable | Type | Default | Description |
|---|---|---|---|
| `saveDialogVisible` | boolean | `false` | Save dialog open |
| `loadDialogVisible` | boolean | `false` | Load dialog open |
| `deleteDialogVisible` | boolean | `false` | Delete confirmation open |
| `diceRollDialogVisible` | boolean | `false` | Dice roll result dialog open |
| `spellDetailDialogVisible` | boolean | `false` | Spell detail modal open |
| `isLoading` | boolean | `false` | Global loading overlay active |
| `loadingMessage` | string | `''` | Loading overlay message |
| `activeTab` | string | `'main'` | Active tab: `main`, `inventory`, `magic`, `levelup` |
| `lastDiceRoll` | RollResult\|null | `null` | Last dice roll result |
| `selectedSpell` | object\|null | `null` | Spell shown in detail modal |

Actions follow a `show<X>() / hide<X>()` pair for each dialog, plus `setLoading(bool, message?)` and `setActiveTab(tab)`.

---

## API Request/Response Models

**File:** `backend/api/routes/actions.py`

### DiceRollRequest / RollResult

| Field | Direction | Type | Description |
|---|---|---|---|
| `modifier` | request | int (default 0) | Bonus/penalty added to roll |
| `dice` | response | List[int] | Three die values (1–6 each) |
| `roll_total` | response | int | Sum of the three dice |
| `final_total` | response | int | `roll_total + modifier` |
| `has_stunt` | response | bool | True if any two dice match |
| `stunt_points` | response | int | Dragon die value when stunt triggered |

### SpellRollRequest

`spell_name: str`, `intelligence: int` (0–20), `focus_bonus: int = 0`

### AttackRollRequest

`weapon_name: str`, `stat_value: int` (0–20), `focus_bonus: int = 0`, `is_melee: bool = True`

---

## CSV Data Schemas

**Location:** `backend/data/csv/`

### Armour.csv

`Name`, `Rating` (damage reduction), `Penalty` (Dex/speed), `Strain` (Con strain)

### MeleeWeapons.csv

`Weapon`, `Group` (e.g. Heavy Blades), `Skill` (stat used), `Damage`, `BonusHit`, `BonusDamage`

### RangeWeapons.csv

`Weapon`, `Range` (short/long bands), `Reload`

### Focus-List.csv

Columns are stat names. Each cell in a column is a valid focus name for that stat.

### Talents.csv / Specs.csv

`Name`, `Talent` (group), `Degree` (Novice/Expert/Master), `DegreeLong`, `Class1`, `Class2`, `Requirements`, `Effect`, `Page`, `Source`

### Spell-List.csv

`Element`, `Degree`, `Arcana`, `Name`, `SpellType`, `MP`, `CastTime`, `TN`, `Test`, `Effect`, `Page`, `Source`

### Stunts-list.csv

`Name`, `SP Cost`, `Effect`

### Class Level Tables (`Envoy.csv`, `Mage.csv`, `Rogue.csv`, `Warrior.csv`)

`Level` (1–20) plus class-specific ability/bonus columns for each level.

---

## Vue Component Props

### StatCard.vue

| Prop | Type | Description |
|---|---|---|
| `statName` | string | Stat name |
| `value` | number (0–20) | Current stat value |
| `isPrimary` | boolean | Primary focus active for this stat |
| `focusBonus` | number (default 0) | Focus bonus; added to displayed modifier |

Computed: `modifier = value + focusBonus`. Emits: `update:value`, `update:isPrimary`, `roll`.

### DiceRoller.vue

| Prop | Type | Description |
|---|---|---|
| `result` | RollResult | Roll output |
| `title` | string | Dialog title |
| `targetNumber` | number\|null | TN for success check |
