<template>
  <div class="character-sidebar">
    <!-- HP/MP Section -->
    <div class="sidebar-section">
      <h3 class="section-title">Health & Magic</h3>
      <div class="hp-mp-group">
        <div class="hp-mp-row">
          <label class="hp-mp-label">HP</label>
          <div class="hp-bar">
            <el-progress
              :percentage="hpPercentage"
              :color="hpColor"
              :show-text="false"
              :stroke-width="6"
            />
          </div>
          <div class="hp-mp-fractional">
            <el-input-number
              v-model="character.hp_current"
              :min="0"
              :max="character.hp_max"
              :step="1"
              size="small"
              controls-position="right"
              class="hp-mp-input"
            />
            <span class="fraction-slash">/</span>
            <el-input-number
              v-model="character.hp_max"
              :min="0"
              :step="1"
              size="small"
              controls-position="right"
              class="hp-mp-input"
            />
          </div>
        </div>

        <div class="hp-mp-row">
          <label class="hp-mp-label">MP</label>
          <div class="hp-bar">
            <el-progress
              :percentage="mpPercentage"
              color="#409eff"
              :show-text="false"
              :stroke-width="6"
            />
          </div>
          <div class="hp-mp-fractional">
            <el-input-number
              v-model="character.mp_current"
              :min="0"
              :max="character.mp_max"
              :step="1"
              size="small"
              controls-position="right"
              class="hp-mp-input"
            />
            <span class="fraction-slash">/</span>
            <el-input-number
              v-model="character.mp_max"
              :min="0"
              :step="1"
              size="small"
              controls-position="right"
              class="hp-mp-input"
            />
          </div>
        </div>
      </div>
    </div>

    <el-divider />

    <!-- Armour Section (Canadian spelling) -->
    <div class="sidebar-section">
      <h3 class="section-title">Armour</h3>
      <div class="armour-group">
        <el-form-item label="Type" class="compact-form-item">
          <el-select
            v-model="armourType"
            placeholder="Select armour"
            size="small"
            style="width: 100%"
          >
            <el-option
              v-for="armor in armorList"
              :key="armor.Name"
              :label="armor.Name"
              :value="armor.Name"
            />
          </el-select>
        </el-form-item>
        <div class="armour-stats-row">
          <div class="armour-stat">
            <label>Rating</label>
            <el-input-number
              v-model="armorRating"
              :min="0"
              :step="1"
              size="small"
              controls-position="right"
              style="width: 100%"
            />
          </div>
          <div class="armour-stat">
            <label>Penalty</label>
            <el-input-number
              v-model="armorPenalty"
              :step="1"
              size="small"
              controls-position="right"
              style="width: 100%"
            />
          </div>
        </div>
      </div>
    </div>

    <el-divider />

    <!-- Movement Section -->
    <div class="sidebar-section">
      <h3 class="section-title">Movement</h3>
      <div class="movement-row">
        <div class="movement-stat">
          <label>Move</label>
          <el-input-number
            v-model="movementMove"
            :min="0"
            :step="1"
            size="small"
            controls-position="right"
            style="width: 100%"
          />
        </div>
        <div class="movement-stat">
          <label>Charge</label>
          <el-input-number
            v-model="movementCharge"
            :min="0"
            :step="1"
            size="small"
            controls-position="right"
            style="width: 100%"
          />
        </div>
        <div class="movement-stat">
          <label>Run</label>
          <el-input-number
            v-model="movementRun"
            :min="0"
            :step="1"
            size="small"
            controls-position="right"
            style="width: 100%"
          />
        </div>
      </div>
    </div>

    <el-divider />

    <!-- Stats Section -->
    <div class="sidebar-section">
      <h3 class="section-title">Abilities</h3>
      <div class="stats-list">
        <div
          v-for="statName in statNames"
          :key="statName"
          class="stat-container"
        >
          <div
            class="stat-name"
            :class="{ 'stat-primary': isPrimaryStat(statName) }"
          >
            {{ statName }}
          </div>
          <div class="stat-row">
            <el-input-number
              v-model="character.stats[statName]"
              :min="-3"
              :max="15"
              :step="1"
              size="small"
              controls-position="right"
              class="stat-value"
              title="Range: -3 to +15"
            />
            <div class="focus-selectors">
              <el-select
                v-model="character.foci_primary[statName]"
                placeholder="Focus"
                size="small"
                class="stat-focus"
                multiple
                collapse-tags
                :max-collapse-tags="0"
              >
                <el-option
                  v-for="focus in getFociForStat(statName)"
                  :key="focus"
                  :label="focus"
                  :value="focus"
                />
              </el-select>
              <!-- Secondary focus selector for level 11+ (for double focusing) -->
              <el-select
                v-if="character.level >= 11"
                v-model="character.foci_secondary[statName]"
                placeholder="Double Focus"
                size="small"
                class="stat-focus-secondary"
                multiple
                collapse-tags
                :max-collapse-tags="0"
                title="Select foci to take twice (double focus = +4)"
              >
                <el-option
                  v-for="focus in character.foci_primary[statName] || []"
                  :key="focus"
                  :label="`${focus} (2nd)`"
                  :value="focus"
                />
              </el-select>
            </div>
            <el-button
              size="small"
              type="primary"
              @click="rollStat(statName)"
              class="roll-button"
            >
              Roll
            </el-button>
          </div>
          <!-- Display selected foci below stat -->
          <div v-if="character.foci_primary[statName]?.length > 0" class="foci-display">
            <el-tag
              v-for="(focus, index) in character.foci_primary[statName]"
              :key="index"
              size="small"
              closable
              @close="removeFocus(statName, index)"
              @click="rollStatWithFocus(statName, focus)"
              :class="['focus-tag clickable', { 'is-double-focus': isDoubleFocus(statName, focus) }]"
              type="primary"
            >
              {{ focus }} (+{{ getFocusBonusForFocus(statName, focus) }})
            </el-tag>
          </div>
          <!-- Arcana Foci nested under Intelligence for Mages (or non-mages who opted in) -->
          <template v-if="statName === 'Intelligence' && (character.char_class === 'Mage' || character.show_arcana_focus_options)">
            <div class="arcana-foci-subsection">
              <div class="stat-header">
                <span class="stat-name">Arcana</span>
                <div class="focus-selectors">
                  <el-select
                    v-model="character.foci_primary['Arcana']"
                    placeholder="Arcana Focus"
                    size="small"
                    class="stat-focus"
                    multiple
                    collapse-tags
                    :max-collapse-tags="0"
                  >
                    <el-option
                      v-for="focus in getFociForStat('Arcana')"
                      :key="focus"
                      :label="focus"
                      :value="focus"
                    />
                  </el-select>
                  <el-select
                    v-if="character.level >= 11"
                    v-model="character.foci_secondary['Arcana']"
                    placeholder="Double Arcana Focus"
                    size="small"
                    class="stat-focus-secondary"
                    multiple
                    collapse-tags
                    :max-collapse-tags="0"
                  >
                    <el-option
                      v-for="focus in character.foci_primary['Arcana'] || []"
                      :key="focus"
                      :label="`${focus} (2nd)`"
                      :value="focus"
                    />
                  </el-select>
                </div>
              </div>
              <div v-if="character.foci_primary['Arcana']?.length > 0" class="foci-display">
                <el-tag
                  v-for="(focus, index) in character.foci_primary['Arcana']"
                  :key="index"
                  size="small"
                  closable
                  @close="removeFocus('Arcana', index)"
                  @click="rollArcana(focus)"
                  :class="['focus-tag clickable', { 'is-double-focus': isDoubleFocus('Arcana', focus) }]"
                  type="primary"
                >
                  {{ focus }} (+{{ getFocusBonusForFocus('Arcana', focus) }})
                </el-tag>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <el-divider />

    <!-- Combat Options Section -->
    <div class="sidebar-section">
      <h3 class="section-title">Combat Options</h3>
      <div class="combat-option-row">
        <label class="combat-option-label" title="When on, conditional class damage extras (Envoy COM>WIL, Rogue Pinpoint DEX>target) are assumed to apply.">
          Auto-apply class damage extras
        </label>
        <el-switch v-model="character.auto_apply_damage_extras" />
      </div>
      <div class="combat-option-row">
        <label class="combat-option-label" title="When on, Arcana Focus options are shown under Intelligence even for non-Mage classes.">
          Show Arcana Focus options
        </label>
        <el-switch v-model="character.show_arcana_focus_options" />
      </div>
    </div>

    <el-divider />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useCharacterStore } from '../stores/character'
import { useDataStore } from '../stores/data'
import { useRollHistoryStore, diceWithVariants } from '../stores/rollHistory'
import { ElMessage, ElNotification, ElTag } from 'element-plus'

const characterStore = useCharacterStore()
const dataStore = useDataStore()
const rollHistoryStore = useRollHistoryStore()

const character = computed(() => characterStore.character)
const fociData = computed(() => dataStore.foci)

// Load foci data and armor on mount
onMounted(async () => {
  await dataStore.fetchFoci()
  await dataStore.fetchArmor()
})

// Get armor list from store - clean up any encoding issues
const armorList = computed(() => {
  return dataStore.armor.map(armor => ({
    ...armor,
    Name: armor.Name?.trim() || 'None'
  }))
})

// Stat names in order
const statNames = [
  'Accuracy',
  'Communication',
  'Constitution',
  'Dexterity',
  'Fighting',
  'Intelligence',
  'Perception',
  'Strength',
  'Willpower'
]

// HP/MP percentage calculations
const hpPercentage = computed(() => {
  if (character.value.hp_max === 0) return 0
  return Math.round((character.value.hp_current / character.value.hp_max) * 100)
})

const mpPercentage = computed(() => {
  if (character.value.mp_max === 0) return 0
  return Math.round((character.value.mp_current / character.value.mp_max) * 100)
})

// HP color based on percentage
const hpColor = computed(() => {
  const pct = hpPercentage.value
  if (pct > 70) return '#67c23a'
  if (pct > 30) return '#e6a23c'
  return '#f56c6c'
})

// Armour values (Canadian spelling) — bound to character store so PDF export sees the choice
const armourType = computed({
  get: () => character.value.equipment?.armor ?? '',
  set: (value) => {
    if (!character.value.equipment) character.value.equipment = {}
    const next = value || null
    if (character.value.equipment.armor !== next) {
      // Picking a different armour clears any manual overrides so the new
      // armour's CSV defaults take effect.
      character.value.equipment.armor_rating = null
      character.value.equipment.armor_penalty = null
    }
    character.value.equipment.armor = next
  }
})

// Rating/Penalty: null in the store means "use the armour's CSV default";
// any number is a user override that persists across reloads.
const selectedArmorDefaults = computed(() => {
  const name = character.value.equipment?.armor
  if (!name) return null
  return armorList.value.find(a => a.Name === name) || null
})

const armorRating = computed({
  get: () => {
    const v = character.value.equipment?.armor_rating
    if (v !== null && v !== undefined) return v
    return selectedArmorDefaults.value?.Rating ?? 0
  },
  set: (value) => {
    if (!character.value.equipment) character.value.equipment = {}
    character.value.equipment.armor_rating = value
  }
})

const armorPenalty = computed({
  get: () => {
    const v = character.value.equipment?.armor_penalty
    if (v !== null && v !== undefined) return v
    return selectedArmorDefaults.value?.Penalty ?? 0
  },
  set: (value) => {
    if (!character.value.equipment) character.value.equipment = {}
    character.value.equipment.armor_penalty = value
  }
})

// Movement values (defaults as specified)
const movementMove = ref(10)
const movementCharge = ref(5)
const movementRun = ref(20)

// Dice roll state (notification instead of dialog)
const lastRoll = ref(null)

// Get foci options for a specific stat
function getFociForStat(statName) {
  if (!fociData.value || typeof fociData.value !== 'object') return []

  // fociData is a dictionary mapping stat names to arrays of foci
  return fociData.value[statName] || []
}

// Primary/secondary stat mapping by class
const primaryStats = computed(() => {
  const classMap = {
    'Envoy': ['Communication', 'Fighting', 'Intelligence', 'Willpower'],
    'Mage': ['Accuracy', 'Intelligence', 'Perception', 'Willpower'],
    'Rogue': ['Accuracy', 'Communication', 'Dexterity', 'Perception'],
    'Warrior': ['Constitution', 'Dexterity', 'Fighting', 'Strength']
  }
  return classMap[character.value.char_class] || []
})

// Check if a stat is primary for current class
function isPrimaryStat(statName) {
  return primaryStats.value.includes(statName)
}

// Check if a focus is a double focus (appears in both primary and secondary)
function isDoubleFocus(statName, focusName) {
  const secondaryFoci = character.value.foci_secondary[statName] || []
  return secondaryFoci.includes(focusName)
}

// Get focus bonus for a specific focus
function getFocusBonusForFocus(statName, focusName) {
  return characterStore.calculateFocusBonus(statName, focusName)
}

// Remove a focus
function removeFocus(statName, index) {
  const foci = character.value.foci_primary[statName] || []
  const focusName = foci[index]

  // Also remove from secondary if it's a double focus
  const secondaryFoci = character.value.foci_secondary[statName] || []
  const secondaryIndex = secondaryFoci.indexOf(focusName)
  if (secondaryIndex > -1) {
    secondaryFoci.splice(secondaryIndex, 1)
  }

  // Remove from primary
  foci.splice(index, 1)
}

// Roll a stat WITHOUT focus (plain stat roll)
async function rollStat(statName) {
  try {
    const statValue = character.value.stats[statName] || 0
    const focusBonus = 0 // No focus for plain stat roll
    const modifier = statValue + focusBonus

    const response = await characterStore.rollDice(modifier)

    lastRoll.value = {
      title: `${statName} Roll (No Focus)`,
      dice: response.dice,
      roll_total: response.roll_total,
      statValue: statValue,
      focusBonus: focusBonus,
      modifier: modifier,
      final_total: response.final_total,
      has_stunt: response.has_stunt,
      stunt_points: response.stunt_points
    }

    showRollNotification(lastRoll.value)
  } catch (error) {
    ElMessage.error('Failed to roll dice')
    console.error('Roll error:', error)
  }
}

// Roll a stat WITH a specific focus
async function rollStatWithFocus(statName, focusName) {
  try {
    const statValue = character.value.stats[statName] || 0
    const focusBonus = characterStore.calculateFocusBonus(statName, focusName)
    const modifier = statValue + focusBonus

    const response = await characterStore.rollDice(modifier)

    lastRoll.value = {
      title: `${statName} - ${focusName}`,
      dice: response.dice,
      roll_total: response.roll_total,
      statValue: statValue,
      focusBonus: focusBonus,
      modifier: modifier,
      final_total: response.final_total,
      has_stunt: response.has_stunt,
      stunt_points: response.stunt_points
    }

    showRollNotification(lastRoll.value)
  } catch (error) {
    ElMessage.error('Failed to roll dice')
    console.error('Roll error:', error)
  }
}

// Roll for arcana (uses Intelligence with arcana as focus)
async function rollArcana(arcanaName) {
  try {
    const intelligenceValue = character.value.stats.Intelligence || 0
    // Arcana uses Intelligence stat - look up focus in the Arcana foci category
    const focusBonus = characterStore.calculateFocusBonus('Arcana', arcanaName)
    const modifier = intelligenceValue + focusBonus

    const response = await characterStore.rollDice(modifier)

    lastRoll.value = {
      title: `${arcanaName} Roll`,
      dice: response.dice,
      roll_total: response.roll_total,
      statValue: intelligenceValue,
      focusBonus: focusBonus,
      modifier: modifier,
      final_total: response.final_total,
      has_stunt: response.has_stunt,
      stunt_points: response.stunt_points
    }

    showRollNotification(lastRoll.value)
  } catch (error) {
    ElMessage.error('Failed to roll dice')
    console.error('Roll error:', error)
  }
}

// Show roll result as bottom-right notification AND push to roll history
function showRollNotification(roll) {
  const diceDisplay = h('div', { class: 'dice-display-inline' }, [
    ...roll.dice.map((die, idx) => h(ElTag, {
      size: 'large',
      type: roll.has_stunt && idx === 2 ? 'danger' : undefined,
      class: ['die-tag-inline', roll.has_stunt && idx === 2 ? 'die-tag-stunt' : null]
    }, () => die))
  ])

  const lineTexts = [
    `Roll: ${roll.dice.join(', ')} = ${roll.roll_total}`,
    `Stat: ${roll.statValue >= 0 ? '+' : ''}${roll.statValue}`
  ]
  if (roll.focusBonus > 0) lineTexts.push(`Focus: +${roll.focusBonus}`)

  const lines = lineTexts.map(t => h('p', {}, t))
  lines.push(h('p', { class: 'final-result' }, `Total: ${roll.final_total}`))
  if (roll.has_stunt) lines.push(h('p', { class: 'stunt-notice' }, `✨ Stunt! SP: ${roll.stunt_points}`))

  const details = h('div', { class: 'roll-details' }, lines)

  ElNotification({
    title: roll.title,
    message: h('div', {}, [diceDisplay, details]),
    type: roll.has_stunt ? 'success' : 'info',
    position: 'bottom-right',
    duration: 5000,
    customClass: 'dice-roll-notification'
  })

  rollHistoryStore.add({
    kind: 'check',
    title: roll.title,
    dice: diceWithVariants(roll.dice, { hasStunt: roll.has_stunt }),
    lines: lineTexts,
    totalLabel: 'Total',
    totalValue: roll.final_total,
    stuntPoints: roll.has_stunt ? roll.stunt_points : 0
  })
}

</script>

<style scoped>
.character-sidebar {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
  background-color: var(--paper-surface, #fafbfc);
  background-image: var(--paper-texture);
}

html.dark .character-sidebar {
  background-color: #1a1a1a;
}

.sidebar-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #303133;
}

html.dark .section-title {
  color: #fff;
}

.stat-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compact-form-item {
  margin-bottom: 0 !important;
}

.compact-form-item :deep(.el-form-item__label) {
  font-size: 13px;
  padding: 0 12px 0 0;
  margin-bottom: 0;
}

.compact-form-item :deep(.el-form-item__content) {
  flex: 1;
}

.compact-form-item :deep(.el-input__inner) {
  font-size: 13px;
}

/* HP/MP Fractional View */
.hp-mp-group {
  display: flex;
  flex-direction: row;
  gap: 8px;
}

.hp-mp-row {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.hp-mp-label {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
}

html.dark .hp-mp-label {
  color: #a8a8a8;
}

.hp-mp-fractional {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
}

.hp-mp-input {
  flex: 1;
  max-width: 75px;
}

.hp-mp-input :deep(.el-input__inner) {
  text-align: center;
  padding: 0 4px;
}

.fraction-slash {
  font-size: 16px;
  font-weight: bold;
  color: #606266;
}

html.dark .fraction-slash {
  color: #a8a8a8;
}

.hp-bar {
  margin-top: 2px;
  width: 100%;
}

/* Soften the progress track so the unfilled portion reads as a subtle groove
   instead of the harsh near-black Element Plus default (--el-border-color-lighter),
   which looked like a 1px black border around the HP/MP bars in dark mode. */
html.dark .hp-bar :deep(.el-progress-bar__outer) {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Armour Section */
.armour-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.armour-stats-row {
  display: flex;
  gap: 12px;
}

.armour-stat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.armour-stat label {
  font-size: 12px;
  font-weight: 500;
  color: #606266;
}

html.dark .armour-stat label {
  color: #a8a8a8;
}

/* Combat Options Section */
.combat-option-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.combat-option-label {
  font-size: 13px;
  color: #606266;
  cursor: help;
}

html.dark .combat-option-label {
  color: #a8a8a8;
}

/* Movement Section */
.movement-row {
  display: flex;
  gap: 12px;
}

.movement-stat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.movement-stat label {
  font-size: 12px;
  font-weight: 500;
  color: #606266;
}

html.dark .movement-stat label {
  color: #a8a8a8;
}

/* Stats list */
.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-name {
  font-size: 12px;
  font-weight: 600;
  color: #606266;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-name.stat-primary {
  font-weight: 700;
  color: #004E83;
}

html.dark .stat-name {
  color: #a8a8a8;
}

html.dark .stat-name.stat-primary {
  color: #4A9EDB;
  font-weight: 700;
}

.stat-row {
  display: grid;
  grid-template-columns: 70px 1fr 60px;
  gap: 6px;
  align-items: center;
  overflow: hidden;
}

.stat-value {
  width: 70px;
}

.focus-selectors {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.stat-focus,
.stat-focus-secondary {
  width: 100%;
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

.stat-focus :deep(.el-select__wrapper),
.stat-focus-secondary :deep(.el-select__wrapper) {
  padding: 0 8px;
  min-height: 24px;
  height: auto !important;
  max-width: 100%;
  box-sizing: border-box;
}

.stat-focus :deep(.el-select__selection),
.stat-focus-secondary :deep(.el-select__selection) {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  width: 100%;
}

.stat-focus :deep(.el-tag),
.stat-focus-secondary :deep(.el-tag) {
  max-width: none !important;
  margin: 1px 0;
  font-size: 12px;
}

.stat-focus-secondary :deep(.el-select__wrapper) {
  border: 2px dashed #1a3a5c;
}

.stat-focus-secondary :deep(.el-tag) {
  background-color: #6d28d9;
  border-color: #6d28d9;
  color: white;
}

.stat-focus-secondary :deep(.el-tag .el-tag__close) {
  color: white;
}

.stat-focus-secondary :deep(.el-tag .el-tag__close:hover) {
  background-color: #4c1d95;
  color: white;
}

.roll-button {
  width: 60px;
  padding: 4px 8px;
}

/* Focus display below stats */
.foci-display {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding-left: 0;
  margin-top: 2px;
}

.focus-tag {
  font-size: 11px;
  margin: 0;
}

.focus-tag.clickable {
  cursor: pointer;
  user-select: none;
}

.focus-tag.clickable:hover {
  opacity: 0.8;
  transform: scale(1.05);
  transition: all 0.2s ease;
}

/* Double focus highlight — deep filled purple, matches the secondary-select tags. */
.focus-tag.is-double-focus {
  --el-tag-bg-color: #6d28d9;
  --el-tag-border-color: #6d28d9;
  --el-tag-text-color: #ffffff;
  --el-tag-hover-color: #ffffff;
  background-color: #6d28d9;
  border-color: #6d28d9;
  color: #ffffff;
}

.focus-tag.is-double-focus .el-tag__close {
  color: #ffffff;
}

.focus-tag.is-double-focus .el-tag__close:hover {
  background-color: #4c1d95;
  color: #ffffff;
}

/* Arcana foci */
.arcana-foci-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.arcana-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.arcana-name {
  font-size: 13px;
  font-weight: 500;
  color: #606266;
  flex: 1;
}

html.dark .arcana-name {
  color: #a8a8a8;
}


/* Scrollbar styling */
.character-sidebar::-webkit-scrollbar {
  width: 8px;
}

.character-sidebar::-webkit-scrollbar-track {
  background: #f5f7fa;
}

html.dark .character-sidebar::-webkit-scrollbar-track {
  background: #0a0a0a;
}

.character-sidebar::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 4px;
}

html.dark .character-sidebar::-webkit-scrollbar-thumb {
  background: #3a3a3a;
}

.character-sidebar::-webkit-scrollbar-thumb:hover {
  background: #909399;
}

html.dark .character-sidebar::-webkit-scrollbar-thumb:hover {
  background: #4a4a4a;
}

/* Notification styles */
:global(.dice-roll-notification) {
  min-width: 300px !important;
}

:global(.dice-roll-notification .dice-display-inline) {
  display: flex;
  gap: 8px;
  margin: 12px 0;
  justify-content: center;
}

:global(.dice-roll-notification .die-tag-inline) {
  font-size: 20px;
  padding: 8px 12px;
  font-weight: bold;
}

:global(.dice-roll-notification .roll-details) {
  font-size: 13px;
  line-height: 1.6;
}

:global(.dice-roll-notification .roll-details p) {
  margin: 4px 0;
}

:global(.dice-roll-notification .final-result) {
  font-size: 16px;
  font-weight: bold;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e4e7ed;
}

:global(.dice-roll-notification .stunt-notice) {
  color: #67c23a;
  font-weight: bold;
}
</style>
