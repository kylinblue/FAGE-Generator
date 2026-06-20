<template>
  <div class="arb-dice-roller" :class="{ collapsed: !expanded }">
    <button
      v-if="!expanded"
      class="arb-toggle"
      type="button"
      @click="expanded = true"
      title="Open dice roller"
    >
      <el-icon><Coin /></el-icon>
      <span>Roll Dice</span>
    </button>

    <div v-else class="arb-panel">
      <div class="arb-header">
        <span class="arb-title">Roll Dice</span>
        <button
          class="arb-close"
          type="button"
          @click="expanded = false"
          title="Minimize"
          aria-label="Minimize dice roller"
        >
          <el-icon><Minus /></el-icon>
        </button>
      </div>

      <div class="arb-body">
        <div class="arb-row">
          <label class="arb-label" for="arb-num">Number:</label>
          <el-input-number
            id="arb-num"
            v-model="numDice"
            :min="1"
            :max="100"
            size="small"
            controls-position="right"
            class="arb-input"
          />
        </div>
        <div class="arb-row">
          <label class="arb-label" for="arb-sides">Sides:</label>
          <el-input-number
            id="arb-sides"
            v-model="sides"
            :min="2"
            :max="1000"
            size="small"
            controls-position="right"
            class="arb-input"
          />
        </div>
        <div class="arb-row">
          <label class="arb-label" for="arb-mod">Modifier:</label>
          <el-input-number
            id="arb-mod"
            v-model="modifier"
            :min="-999"
            :max="999"
            size="small"
            controls-position="right"
            class="arb-input"
          />
        </div>

        <el-button
          type="primary"
          class="arb-roll"
          @click="roll"
        >
          Roll
        </el-button>

        <div v-if="result" class="arb-output">
          <span class="arb-formula">
            ({{ result.dice.join(', ') }})<template v-if="result.modifier !== 0">
              {{ result.modifier > 0 ? ' + ' : ' − ' }}{{ Math.abs(result.modifier) }}</template>
            =
          </span>
          <span class="arb-total">{{ result.total }}</span>
        </div>
        <div class="arb-hint">Total: (#, #, #) + N = SUM</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Coin, Minus } from '@element-plus/icons-vue'

const expanded = ref(false)
const numDice = ref(3)
const sides = ref(6)
const modifier = ref(0)
const result = ref(null)

function roll() {
  const n = Math.max(1, Math.min(100, Number(numDice.value) || 1))
  const s = Math.max(2, Math.min(1000, Number(sides.value) || 6))
  const mod = Number(modifier.value) || 0
  const dice = Array.from({ length: n }, () => 1 + Math.floor(Math.random() * s))
  const sum = dice.reduce((a, b) => a + b, 0)
  result.value = { dice, modifier: mod, total: sum + mod }
}
</script>

<style scoped>
.arb-dice-roller {
  /* Positioning handled by parent .floating-corner-left stack in App.vue. */
  display: inline-block;
}

.arb-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(90deg, #0d5a8a 0%, #2196f3 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.arb-toggle:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

.arb-panel {
  width: 260px;
  background-color: var(--el-bg-color, #fff);
  border: 1px solid var(--el-border-color, #dcdfe6);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

.arb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #0d5a8a 0%, #2196f3 100%);
  color: white;
  padding: 8px 12px;
}

.arb-title {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.arb-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.arb-close:hover {
  background: rgba(255, 255, 255, 0.35);
}

.arb-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.arb-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.arb-label {
  font-weight: 600;
  color: var(--el-text-color-primary);
  min-width: 70px;
}

.arb-input {
  width: 110px;
}

.arb-roll {
  width: 100%;
}

.arb-output {
  margin-top: 4px;
  font-size: 14px;
  min-height: 24px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  word-break: break-word;
}

.arb-formula {
  color: var(--el-text-color-regular);
}

.arb-total {
  font-weight: 700;
  color: var(--el-color-primary);
  font-size: 16px;
}

.arb-hint {
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

html.dark .arb-panel {
  background-color: #1a1a1a;
  border-color: #333;
}
</style>
