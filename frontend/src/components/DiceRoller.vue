<template>
  <div class="dice-roller">
    <div v-if="result" class="dice-result">
      <h3 v-if="title" class="result-title">{{ title }}</h3>

      <div class="dice-display">
        <el-tag
          v-for="(die, index) in result.dice"
          :key="`base-${index}`"
          :type="getDiceType(die)"
          size="large"
          class="dice-tag dice-roll-animation"
          :style="{ animationDelay: `${index * 0.1}s` }"
          effect="dark"
        >
          {{ die }}
        </el-tag>
        <el-tag
          v-for="(die, index) in result.bonus_dice || []"
          :key="`bonus-${index}`"
          :type="getDiceType(die)"
          size="large"
          class="dice-tag dice-roll-animation bonus-die"
          :style="{ animationDelay: `${(result.dice.length + index) * 0.1}s` }"
          effect="dark"
        >
          {{ die }}
        </el-tag>
      </div>

      <div class="result-info">
        <div class="result-row">
          <span class="result-label">Roll:</span>
          <span class="result-value">{{ diceTotal }}</span>
        </div>
        <template v-if="isDamage">
          <div v-if="result.modifier" class="result-row">
            <span class="result-label">Modifier:</span>
            <span class="result-value">{{ result.modifier >= 0 ? '+' : '' }}{{ result.modifier }}</span>
          </div>
          <div v-if="result.stat_bonus" class="result-row">
            <span class="result-label">Stat:</span>
            <span class="result-value">+{{ result.stat_bonus }}</span>
          </div>
          <div v-if="result.stunt_bonus" class="result-row">
            <span class="result-label">Stunt die:</span>
            <span class="result-value">+{{ result.stunt_bonus }}</span>
          </div>
        </template>
        <div v-else-if="modifier !== 0" class="result-row">
          <span class="result-label">Modifier:</span>
          <span class="result-value">{{ modifier >= 0 ? '+' : '' }}{{ modifier }}</span>
        </div>
        <div class="result-row total">
          <span class="result-label">Total:</span>
          <span class="result-value">{{ totalValue }}</span>
        </div>
      </div>

      <el-alert
        v-if="result.has_stunt"
        type="warning"
        :closable="false"
        class="stunt-alert"
      >
        <template #title>
          <div class="stunt-title">
            <el-icon><Star /></el-icon>
            <span>Stunt Point Available!</span>
          </div>
        </template>
      </el-alert>

      <el-alert
        v-if="targetNumber !== null"
        :type="isSuccess ? 'success' : 'error'"
        :closable="false"
        class="success-alert"
      >
        <template #title>
          <div class="success-title">
            <span v-if="isSuccess">Success!</span>
            <span v-else>Failed</span>
            <span class="tn-text">(TN: {{ targetNumber }})</span>
          </div>
        </template>
      </el-alert>
    </div>

    <div v-else class="no-result">
      <el-empty description="No dice rolled yet" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Star } from '@element-plus/icons-vue'

const props = defineProps({
  result: {
    type: Object,
    default: null
  },
  title: {
    type: String,
    default: ''
  },
  targetNumber: {
    type: Number,
    default: null
  }
})

const isDamage = computed(() => {
  return props.result && 'final_total' in props.result && 'base_total' in props.result
})

const totalValue = computed(() => {
  if (!props.result) return 0
  if (isDamage.value) return props.result.final_total
  return props.result.total ?? props.result.final_total ?? 0
})

const diceTotal = computed(() => {
  if (!props.result?.dice) return 0
  const base = props.result.dice.reduce((sum, die) => sum + die, 0)
  const bonus = (props.result.bonus_dice || []).reduce((sum, die) => sum + die, 0)
  return base + bonus
})

const modifier = computed(() => {
  if (!props.result || isDamage.value) return 0
  const total = props.result.total ?? props.result.final_total ?? 0
  return total - props.result.dice.reduce((sum, die) => sum + die, 0)
})

const isSuccess = computed(() => {
  if (props.targetNumber === null) return null
  return totalValue.value >= props.targetNumber
})

function getDiceType(value) {
  // Color dice based on value
  if (value === 6) return 'success'
  if (value === 1) return 'danger'
  return 'primary'
}
</script>

<style scoped>
.dice-roller {
  padding: 16px;
}

.dice-result {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

.result-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.dice-display {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.dice-tag {
  font-size: 28px;
  font-weight: bold;
  padding: 16px 20px;
  min-width: 60px;
  text-align: center;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.dice-tag:hover {
  transform: scale(1.1);
}

.dice-tag.bonus-die {
  outline: 2px dashed var(--el-color-warning);
  outline-offset: 2px;
}

/* Dice roll animation */
.dice-roll-animation {
  animation: rollDice 0.6s ease-out;
}

@keyframes rollDice {
  0% {
    transform: rotate(0deg) scale(0);
    opacity: 0;
  }
  50% {
    transform: rotate(180deg) scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: rotate(360deg) scale(1);
    opacity: 1;
  }
}

.result-info {
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: fadeIn 0.5s ease-out 0.3s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 16px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.result-row.total {
  font-size: 18px;
  font-weight: bold;
  background-color: var(--el-color-primary-light-9);
  border: 1px solid var(--el-color-primary);
}

.result-label {
  color: var(--el-text-color-secondary);
}

.result-value {
  color: var(--el-text-color-primary);
  font-weight: 600;
}

.stunt-alert,
.success-alert {
  width: 100%;
  max-width: 400px;
  animation: slideIn 0.5s ease-out 0.5s both;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.stunt-alert {
  animation: pulse 1.5s ease-in-out 0.8s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
}

.stunt-title,
.success-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.tn-text {
  margin-left: 8px;
  font-size: 14px;
  opacity: 0.8;
}

.no-result {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
