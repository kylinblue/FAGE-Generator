<template>
  <div class="armor-select">
    <el-form-item :label="label">
      <el-select
        :model-value="modelValue"
        @update:model-value="handleChange"
        placeholder="Select armor"
        filterable
        clearable
        style="width: 100%"
      >
        <el-option
          v-for="armor in armorList"
          :key="armor.Name"
          :label="formatArmorLabel(armor)"
          :value="armor.Name"
        >
          <div class="armor-option">
            <span class="armor-name">{{ armor.Name }}</span>
            <span class="armor-stats">
              Rating: {{ armor.Rating }} |
              Penalty: {{ armor.Penalty }} |
              Strain: {{ armor.Strain }}
            </span>
          </div>
        </el-option>
      </el-select>
    </el-form-item>

    <!-- Display selected armor details -->
    <div v-if="selectedArmorDetails" class="armor-details">
      <el-descriptions :column="2" size="small" border>
        <el-descriptions-item label="Name">
          {{ selectedArmorDetails.Name }}
        </el-descriptions-item>
        <el-descriptions-item label="Rating">
          {{ selectedArmorDetails.Rating }}
        </el-descriptions-item>
        <el-descriptions-item label="Penalty">
          {{ selectedArmorDetails.Penalty }}
        </el-descriptions-item>
        <el-descriptions-item label="Strain">
          {{ selectedArmorDetails.Strain }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="selectedArmorDetails.Special"
          label="Special"
          :span="2"
        >
          {{ selectedArmorDetails.Special }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: null
  },
  armorList: {
    type: Array,
    required: true,
    default: () => []
  },
  label: {
    type: String,
    default: 'Armor'
  },
  showDetails: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// Find the selected armor details
const selectedArmorDetails = computed(() => {
  if (!props.modelValue || !props.armorList.length) {
    return null
  }
  return props.armorList.find(armor => armor.Name === props.modelValue) || null
})

// Format armor label for the dropdown
const formatArmorLabel = (armor) => {
  return `${armor.Name} (Rating: ${armor.Rating})`
}

// Handle armor selection change
const handleChange = (value) => {
  emit('update:modelValue', value)
  const armorDetails = value
    ? props.armorList.find(armor => armor.Name === value)
    : null
  emit('change', armorDetails)
}
</script>

<style scoped>
.armor-select {
  width: 100%;
}

.armor-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.armor-name {
  font-weight: 500;
}

.armor-stats {
  font-size: 12px;
  color: #909399;
  margin-left: 10px;
}

.armor-details {
  margin-top: 15px;
}
</style>
