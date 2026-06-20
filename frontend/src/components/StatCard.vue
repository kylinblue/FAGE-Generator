<template>
  <el-card class="stat-card" :class="{ 'primary-stat': isPrimary }">
    <div class="stat-content">
      <div class="stat-header">
        <h3>{{ statName }}</h3>
        <el-checkbox
          v-model="isPrimaryLocal"
          @change="$emit('update:isPrimary', $event)"
          size="small"
        >
          Primary
        </el-checkbox>
      </div>

      <div class="stat-value">
        <el-input-number
          :model-value="value"
          @update:model-value="$emit('update:value', $event)"
          :min="0"
          :max="20"
          :step="1"
          size="large"
        />
      </div>

      <div class="stat-modifier">
        Modifier: <strong>{{ modifier }}</strong>
      </div>

      <el-button
        type="primary"
        @click="$emit('roll')"
        class="roll-button"
      >
        🎲 Roll
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  statName: {
    type: String,
    required: true
  },
  value: {
    type: Number,
    required: true,
    default: 10
  },
  isPrimary: {
    type: Boolean,
    default: false
  },
  focusBonus: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:value', 'update:isPrimary', 'roll'])

const isPrimaryLocal = ref(props.isPrimary)

// Modifier is the stat value itself in AGE system
const modifier = computed(() => {
  return props.value + props.focusBonus
})

watch(() => props.isPrimary, (newVal) => {
  isPrimaryLocal.value = newVal
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.stat-card.primary-stat {
  border: 2px solid var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.stat-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.stat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.stat-value {
  width: 100%;
  display: flex;
  justify-content: center;
}

.stat-value :deep(.el-input-number) {
  width: 120px;
}

.stat-modifier {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.roll-button {
  width: 100%;
}
</style>
