<template>
  <div class="character-sheet" :style="{ fontSize: fontSize + 'px' }">
    <div class="sheet-header">
      <h1 class="character-name">{{ character.name || 'Unnamed Character' }}</h1>
      <div class="character-info">
        <div class="info-row">
          <span class="label">Class:</span>
          <span class="value">{{ character.char_class }}</span>
        </div>
        <div class="info-row">
          <span class="label">Level:</span>
          <span class="value">{{ character.level }}</span>
        </div>
        <div class="info-row">
          <span class="label">Player:</span>
          <span class="value">{{ character.player_name || 'N/A' }}</span>
        </div>
        <div class="info-row">
          <span class="label">Background:</span>
          <span class="value">{{ character.background || 'N/A' }}</span>
        </div>
      </div>
    </div>

    <div class="sheet-section">
      <h2>Abilities</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Ability</th>
            <th>Score</th>
            <th>Modifier</th>
            <th>Foci</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, stat) in character.stats" :key="stat">
            <td>{{ stat }}</td>
            <td>{{ value }}</td>
            <td>+{{ value }}</td>
            <td>{{ formatFoci(stat) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sheet-section">
      <h2>Health & Resources</h2>
      <div class="resources">
        <div class="resource-box">
          <div class="resource-label">Hit Points</div>
          <div class="resource-value">{{ character.hp_current }} / {{ character.hp_max }}</div>
        </div>
        <div class="resource-box">
          <div class="resource-label">Magic Points</div>
          <div class="resource-value">{{ character.mp_current }} / {{ character.mp_max }}</div>
        </div>
      </div>
    </div>

    <div class="sheet-section" v-if="character.equipment.armor">
      <h2>Armor</h2>
      <div class="equipment-item">
        <strong>{{ character.equipment.armor }}</strong>
      </div>
    </div>

    <div class="sheet-section" v-if="meleeWeapons.length > 0">
      <h2>Melee Weapons</h2>
      <table class="weapons-table">
        <thead>
          <tr>
            <th>Weapon</th>
            <th>Group</th>
            <th>Damage</th>
            <th>Special</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="weapon in meleeWeapons" :key="weapon.Weapon">
            <td>{{ weapon.Weapon }}</td>
            <td>{{ weapon.Group }}</td>
            <td>{{ weapon.Damage }}</td>
            <td>{{ weapon.Special || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sheet-section" v-if="rangedWeapons.length > 0">
      <h2>Ranged Weapons</h2>
      <table class="weapons-table">
        <thead>
          <tr>
            <th>Weapon</th>
            <th>Group</th>
            <th>Damage</th>
            <th>Short Range</th>
            <th>Long Range</th>
            <th>Reload</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="weapon in rangedWeapons" :key="weapon.Weapon">
            <td>{{ weapon.Weapon }}</td>
            <td>{{ weapon.Group }}</td>
            <td>{{ weapon.Damage }}</td>
            <td>{{ weapon['Short Range'] }}</td>
            <td>{{ weapon['Long Range'] }}</td>
            <td>{{ weapon.Reload }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sheet-section" v-if="character.talents && character.talents.length > 0">
      <h2>Talents</h2>
      <div class="talents-list">
        <div v-for="talent in character.talents" :key="talent" class="talent-item">
          {{ talent }}
        </div>
      </div>
    </div>

    <div class="sheet-section" v-if="character.specializations && character.specializations.length > 0">
      <h2>Specializations</h2>
      <div class="specializations-list">
        <div v-for="spec in character.specializations" :key="spec" class="spec-item">
          {{ spec }}
        </div>
      </div>
    </div>

    <div class="sheet-section" v-if="character.magic && character.magic.arcana && character.magic.arcana.length > 0">
      <h2>Arcana</h2>
      <div class="arcana-list">
        <span v-for="arcana in character.magic.arcana" :key="arcana" class="arcana-tag">
          {{ arcana }}
        </span>
      </div>
    </div>

    <div class="sheet-section" v-if="character.extras && character.extras.inventory && character.extras.inventory.length > 0">
      <h2>Inventory</h2>
      <table class="inventory-table">
        <thead>
          <tr>
            <th>Item</th>
            <th>Quantity</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in character.extras.inventory" :key="index">
            <td>{{ item.item }}</td>
            <td>{{ item.quantity }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="sheet-section" v-if="character.extras && hasCurrency">
      <h2>Currency</h2>
      <div class="currency">
        <span><strong>Gold:</strong> {{ character.extras.currency.gold }}</span>
        <span><strong>Silver:</strong> {{ character.extras.currency.silver }}</span>
        <span><strong>Copper:</strong> {{ character.extras.currency.copper }}</span>
      </div>
    </div>

    <div class="sheet-section" v-if="character.extras && character.extras.backstory">
      <h2>Backstory</h2>
      <div class="backstory">
        {{ character.extras.backstory }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  character: {
    type: Object,
    required: true
  },
  fontSize: {
    type: Number,
    default: 12
  }
})

const meleeWeapons = computed(() => {
  return props.character.equipment?.melee_weapons || []
})

const rangedWeapons = computed(() => {
  return props.character.equipment?.ranged_weapons || []
})

const hasCurrency = computed(() => {
  const currency = props.character.extras?.currency
  if (!currency) return false
  return currency.gold > 0 || currency.silver > 0 || currency.copper > 0
})

// Format foci with counts (e.g., "Brawling (2)" if selected twice)
function formatFoci(stat) {
  const primaryFoci = props.character.foci_primary?.[stat] || []
  const secondaryFoci = props.character.foci_secondary?.[stat] || []
  const allFoci = [...primaryFoci, ...secondaryFoci]

  if (allFoci.length === 0) return '-'

  const counted = {}
  allFoci.forEach(focus => {
    counted[focus] = (counted[focus] || 0) + 1
  })

  const formatted = Object.entries(counted).map(([name, count]) => {
    return count > 1 ? `${name} (${count})` : name
  })

  return formatted.join(', ')
}
</script>

<style scoped>
.character-sheet {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  background: white;
}

.sheet-header {
  border-bottom: 3px solid #333;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.character-name {
  font-size: 2em;
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.character-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.info-row {
  display: flex;
  gap: 8px;
}

.label {
  font-weight: bold;
  color: #555;
}

.value {
  color: #333;
}

.sheet-section {
  margin-bottom: 25px;
  page-break-inside: avoid;
}

.sheet-section h2 {
  font-size: 1.4em;
  color: #2c3e50;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
  margin-bottom: 10px;
}

.stats-table,
.weapons-table,
.inventory-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.stats-table th,
.stats-table td,
.weapons-table th,
.weapons-table td,
.inventory-table th,
.inventory-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.stats-table th,
.weapons-table th,
.inventory-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.resources {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.resource-box {
  border: 2px solid #333;
  padding: 10px 20px;
  border-radius: 5px;
  text-align: center;
  min-width: 150px;
}

.resource-label {
  font-weight: bold;
  font-size: 0.9em;
  color: #555;
  margin-bottom: 5px;
}

.resource-value {
  font-size: 1.5em;
  font-weight: bold;
  color: #2c3e50;
}

.equipment-item {
  padding: 10px;
  background-color: #f9f9f9;
  border-left: 4px solid #409eff;
  margin-top: 10px;
}

.talents-list,
.specializations-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.talent-item {
  background-color: #e8f4fd;
  padding: 8px 15px;
  border-radius: 4px;
  border: 1px solid #409eff;
}

.spec-item {
  background-color: #d1fae5;
  padding: 8px 15px;
  border-radius: 4px;
  border: 1px solid #10b981;
}

.arcana-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.arcana-tag {
  background-color: #f3e8ff;
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #a855f7;
  font-weight: 500;
}

.currency {
  display: flex;
  gap: 20px;
  margin-top: 10px;
  padding: 10px;
  background-color: #fffbeb;
  border: 1px solid #fbbf24;
  border-radius: 4px;
}

.backstory {
  padding: 15px;
  background-color: #f9fafb;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  line-height: 1.6;
  margin-top: 10px;
  white-space: pre-wrap;
}

/* Print-specific styles */
@media print {
  .character-sheet {
    max-width: none;
    padding: 10mm;
  }

  .sheet-section {
    page-break-inside: avoid;
  }
}
</style>
