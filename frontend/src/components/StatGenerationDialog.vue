<template>
  <el-dialog
    v-model="visible"
    title="Determining Abilities"
    width="640px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-tabs v-model="activeMode" type="card">
      <!-- Rolled Stats -->
      <el-tab-pane label="Roll Stats" name="roll">
        <p class="mode-description">
          Roll nine sets of 3d6 and apply them straight down the line to your ability scores.
        </p>

        <div class="roll-controls">
          <el-button type="primary" @click="rollAll">
            {{ rolledSets.length > 0 ? 'Re-roll All' : 'Roll 9 Sets of 3d6' }}
          </el-button>
          <span v-if="rolledSets.length > 0" class="roll-hint">
            Resulting scores will replace your current stats when you click Apply.
          </span>
        </div>

        <el-table
          v-if="rolledSets.length > 0"
          :data="rolledStatRows"
          stripe
          border
          size="small"
          style="margin-top: 12px;"
        >
          <el-table-column label="Ability" prop="ability" width="160" />
          <el-table-column label="3d6" width="160">
            <template #default="scope">
              <span class="dice-cells">
                <el-tag
                  v-for="(die, i) in scope.row.dice"
                  :key="i"
                  size="small"
                  class="die-tag"
                >{{ die }}</el-tag>
              </span>
            </template>
          </el-table-column>
          <el-table-column label="Total" prop="total" width="80" />
          <el-table-column label="Score">
            <template #default="scope">
              <strong>{{ formatSigned(scope.row.score) }}</strong>
            </template>
          </el-table-column>
        </el-table>

        <el-empty
          v-else
          description="Click the button above to roll 9 sets of 3d6."
          :image-size="60"
          style="padding: 12px 0;"
        />
      </el-tab-pane>

      <!-- Point Buy (free spend) -->
      <el-tab-pane label="Point Buy" name="pointbuy">
        <p class="mode-description">
          Start with 0 in each stat. Spend up to 13 points to raise any stat
          (1 point per increase, max +3 at creation). You may take a stat below 0
          but you gain no extra points for doing so.
        </p>

        <div class="points-header points-header--spent">
          <span>
            Points spent:
            <strong :class="{ 'points-error': pointsSpent > 13 }">{{ pointsSpent }}</strong>
            / 13
          </span>
          <span :class="{ 'points-error': pointsSpent > 13 }">
            Remaining: <strong>{{ 13 - pointsSpent }}</strong>
          </span>
        </div>

        <el-table :data="standardArrayRows" stripe border size="small">
          <el-table-column label="Ability" prop="name" />
          <el-table-column label="Score" width="180">
            <template #default="scope">
              <el-input-number
                v-model="freeBuyStats[scope.row.name]"
                :min="-3"
                :max="3"
                :step="1"
                size="small"
                controls-position="right"
                style="width: 140px;"
              />
            </template>
          </el-table-column>
        </el-table>

        <el-alert
          v-if="pointsSpent > 13"
          type="error"
          show-icon
          :closable="false"
          style="margin-top: 12px;"
        >
          You have spent more than 13 points. Reduce some stats to continue.
        </el-alert>
      </el-tab-pane>

      <!-- Standard Array (pool-based) -->
      <el-tab-pane label="Standard Array" name="standardarray">
        <p class="mode-description">
          Assign each ability one value from the array below: two 3s, two 2s, three 1s, and two 0s.
        </p>

        <div class="pool-row">
          <div class="points-header">
            <div class="pool-tiles">
              <span
                v-for="(tile, i) in pointPool"
                :key="i"
                class="pool-tile"
                :class="[`tile-${tile.value}`, { 'tile-used': tile.used }]"
              >{{ tile.value }}</span>
            </div>
          </div>
          <el-button
            :disabled="!hasAnyAssignment"
            @click="resetStandardArray"
          >
            Reset
          </el-button>
        </div>

        <el-table :data="standardArrayRows" stripe border size="small">
          <el-table-column label="Ability" prop="name" />
          <el-table-column label="Score" width="220">
            <template #default="scope">
              <div class="score-buttons">
                <button
                  v-for="value in [3, 2, 1, 0]"
                  :key="value"
                  type="button"
                  class="score-btn"
                  :class="[`score-btn-${value}`, {
                    active: standardArrayStats[scope.row.name] === value,
                    disabled: isValueLocked(value, scope.row.name)
                  }]"
                  :disabled="isValueLocked(value, scope.row.name)"
                  @click="toggleValue(scope.row.name, value)"
                >{{ value }}</button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Skip</el-button>
        <el-button
          type="primary"
          :disabled="!canApply"
          @click="handleApply"
        >
          Apply
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useCharacterStore } from '../stores/character'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue'])

const characterStore = useCharacterStore()

const visible = ref(props.modelValue)
const activeMode = ref('roll')

// Stat order (matches "straight down the line" lookup from the rules)
const STAT_NAMES = [
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

// 3d6 → ability score lookup table (per rulebook)
const SCORE_LOOKUP = {
  3: -2,
  4: -1, 5: -1,
  6: 0, 7: 0, 8: 0,
  9: 1, 10: 1, 11: 1,
  12: 2, 13: 2, 14: 2,
  15: 3, 16: 3, 17: 3,
  18: 4
}

// Rolled-stat state
const rolledSets = ref([]) // array of { dice: [d1, d2, d3], total }

const rolledStatRows = computed(() =>
  rolledSets.value.map((set, i) => ({
    ability: STAT_NAMES[i],
    dice: set.dice,
    total: set.total,
    score: SCORE_LOOKUP[set.total] ?? 0
  }))
)

// Free-spend Point Buy state — zero-initialised, up to 13 points
const freeBuyStats = ref(makeZeroStats())

const pointsSpent = computed(() =>
  STAT_NAMES.reduce((sum, name) => sum + Math.max(0, freeBuyStats.value[name] || 0), 0)
)

// Standard Array pool: 2x 3pts, 2x 2pts, 3x 1pt, 2x 0pts (totals 13 points)
const POOL_CONFIG = [
  { value: 3, count: 2 },
  { value: 2, count: 2 },
  { value: 1, count: 3 },
  { value: 0, count: 2 }
]

const standardArrayStats = ref(makeEmptyStats())

const standardArrayRows = computed(() =>
  STAT_NAMES.map(name => ({ name }))
)

const valueUsage = computed(() => {
  const usage = {}
  for (const { value } of POOL_CONFIG) usage[value] = 0
  for (const name of STAT_NAMES) {
    const v = standardArrayStats.value[name]
    if (v !== null && v !== undefined && usage[v] !== undefined) usage[v] += 1
  }
  return usage
})

const pointPool = computed(() => {
  const tiles = []
  for (const { value, count } of POOL_CONFIG) {
    const used = valueUsage.value[value] || 0
    for (let i = 0; i < count; i++) {
      tiles.push({ value, used: i < used })
    }
  }
  return tiles
})

const poolLimits = Object.fromEntries(POOL_CONFIG.map(({ value, count }) => [value, count]))

function isValueLocked(value, statName) {
  if (standardArrayStats.value[statName] === value) return false
  const used = valueUsage.value[value] || 0
  return used >= (poolLimits[value] || 0)
}

function toggleValue(statName, value) {
  standardArrayStats.value[statName] = standardArrayStats.value[statName] === value ? null : value
}

const allAssigned = computed(() =>
  STAT_NAMES.every(name => {
    const v = standardArrayStats.value[name]
    return v !== null && v !== undefined
  })
)

const hasAnyAssignment = computed(() =>
  STAT_NAMES.some(name => {
    const v = standardArrayStats.value[name]
    return v !== null && v !== undefined
  })
)

function resetStandardArray() {
  standardArrayStats.value = makeEmptyStats()
}

const canApply = computed(() => {
  if (activeMode.value === 'roll') return rolledSets.value.length === STAT_NAMES.length
  if (activeMode.value === 'pointbuy') return pointsSpent.value <= 13
  return allAssigned.value
})

function makeEmptyStats() {
  return STAT_NAMES.reduce((acc, name) => { acc[name] = null; return acc }, {})
}

function makeZeroStats() {
  return STAT_NAMES.reduce((acc, name) => { acc[name] = 0; return acc }, {})
}

function roll3d6() {
  const dice = [
    Math.floor(Math.random() * 6) + 1,
    Math.floor(Math.random() * 6) + 1,
    Math.floor(Math.random() * 6) + 1
  ]
  return { dice, total: dice[0] + dice[1] + dice[2] }
}

function rollAll() {
  rolledSets.value = STAT_NAMES.map(() => roll3d6())
}

function formatSigned(n) {
  return n >= 0 ? `+${n}` : `${n}`
}

function applyStats(stats) {
  for (const name of STAT_NAMES) {
    characterStore.updateStat(name, stats[name] ?? 0)
  }
}

function handleApply() {
  if (activeMode.value === 'roll') {
    const stats = {}
    rolledStatRows.value.forEach(row => { stats[row.ability] = row.score })
    applyStats(stats)
    ElMessage.success('Rolled stats applied.')
  } else if (activeMode.value === 'pointbuy') {
    applyStats(freeBuyStats.value)
    ElMessage.success('Point-buy stats applied.')
  } else {
    applyStats(standardArrayStats.value)
    ElMessage.success('Standard array applied.')
  }
  visible.value = false
}

function handleClose() {
  visible.value = false
}

function resetDialogState() {
  rolledSets.value = []
  freeBuyStats.value = makeZeroStats()
  standardArrayStats.value = makeEmptyStats()
  activeMode.value = 'roll'
}

watch(() => props.modelValue, (newValue) => {
  visible.value = newValue
  if (newValue) resetDialogState()
})

watch(visible, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>

<style scoped>
.mode-description {
  font-size: 13px;
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

html.dark .mode-description {
  color: #a8a8a8;
}

.roll-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.roll-hint {
  font-size: 12px;
  color: #909399;
}

.dice-cells {
  display: inline-flex;
  gap: 4px;
}

.die-tag {
  min-width: 28px;
  text-align: center;
  font-weight: 600;
}

.pool-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.points-header {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.points-header--spent {
  justify-content: space-between;
  margin-bottom: 12px;
}

.points-error {
  color: #f56c6c;
}

html.dark .points-header {
  background-color: #2a2a2a;
  color: #e4e7ed;
}

.pool-label {
  font-weight: 500;
}

.pool-tiles {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.pool-tile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  transition: opacity 0.15s;
}

.pool-tile.tile-used {
  opacity: 0.25;
}

.tile-3 { background-color: #f56c6c; }
.tile-2 { background-color: #e6a23c; }
.tile-1 { background-color: #409eff; }
.tile-0 { background-color: #909399; }

.score-buttons {
  display: inline-flex;
  gap: 4px;
}

.score-btn {
  width: 34px;
  height: 34px;
  border-radius: 4px;
  border: 2px solid;
  background-color: transparent;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: background-color 0.15s, color 0.15s;
}

.score-btn:hover:not(:disabled) {
  filter: brightness(1.1);
}

.score-btn:disabled,
.score-btn.disabled {
  border-color: #d4d7de;
  color: #c0c4cc;
  background-color: transparent;
  cursor: not-allowed;
  opacity: 0.6;
}

html.dark .score-btn:disabled,
html.dark .score-btn.disabled {
  border-color: #4a4d52;
  color: #6c6e72;
}

.score-btn-3 { border-color: #f56c6c; color: #f56c6c; }
.score-btn-3.active { background-color: #f56c6c; color: #fff; }

.score-btn-2 { border-color: #e6a23c; color: #e6a23c; }
.score-btn-2.active { background-color: #e6a23c; color: #fff; }

.score-btn-1 { border-color: #409eff; color: #409eff; }
.score-btn-1.active { background-color: #409eff; color: #fff; }

.score-btn-0 { border-color: #909399; color: #909399; }
.score-btn-0.active { background-color: #909399; color: #fff; }

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
