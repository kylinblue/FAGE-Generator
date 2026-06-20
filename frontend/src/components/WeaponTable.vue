<template>
  <div class="weapon-table">
    <el-table
      :data="weapons"
      :height="height"
      :row-key="getRowKey"
      @selection-change="handleSelectionChange"
      style="width: 100%"
    >
      <el-table-column
        v-if="selectionMode === 'multiple'"
        type="selection"
        width="55"
        :reserve-selection="true"
      />
      <el-table-column
        v-else-if="selectionMode === 'single'"
        width="55"
      >
        <template #default="scope">
          <el-radio
            :model-value="isSelected(scope.row)"
            @change="handleSingleSelection(scope.row)"
          >
            <span></span>
          </el-radio>
        </template>
      </el-table-column>

      <el-table-column
        prop="Weapon"
        label="Weapon"
        :min-width="weaponType === 'melee' ? 150 : 120"
        sortable
      />
      <el-table-column
        prop="Group"
        label="Group"
        width="120"
        sortable
      />
      <el-table-column
        v-if="weaponType === 'melee'"
        prop="Skill"
        label="Skill"
        width="80"
      />
      <el-table-column
        prop="Damage"
        label="Damage"
        width="100"
        sortable
      />
      <el-table-column
        v-if="weaponType === 'ranged'"
        prop="Short Range"
        label="Short Range"
        width="110"
      />
      <el-table-column
        v-if="weaponType === 'ranged'"
        prop="Long Range"
        label="Long Range"
        width="110"
      />
      <el-table-column
        v-if="weaponType === 'ranged'"
        prop="Reload"
        label="Reload"
        width="100"
      />
      <el-table-column
        v-if="weaponType === 'melee'"
        prop="Special"
        label="Special"
        :min-width="100"
        show-overflow-tooltip
      />
      <el-table-column
        v-if="showRollButton"
        label="Actions"
        width="180"
        fixed="right"
      >
        <template #default="scope">
          <el-button
            size="small"
            @click="handleAttack(scope.row)"
          >
            Attack
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="handleDamage(scope.row)"
          >
            Damage
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  weapons: {
    type: Array,
    required: true,
    default: () => []
  },
  weaponType: {
    type: String,
    required: true,
    validator: (value) => ['melee', 'ranged'].includes(value)
  },
  selectionMode: {
    type: String,
    default: 'multiple',
    validator: (value) => ['single', 'multiple', 'none'].includes(value)
  },
  modelValue: {
    type: Array,
    default: () => []
  },
  height: {
    type: String,
    default: '300px'
  },
  showRollButton: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'attack', 'damage', 'selection-change'])

const selectedWeapons = ref([...props.modelValue])

// Generate unique row key
const getRowKey = (row) => {
  return row.Weapon || row.Name || JSON.stringify(row)
}

// Check if a weapon is selected (for single selection mode)
const isSelected = (weapon) => {
  return selectedWeapons.value.some(w => getRowKey(w) === getRowKey(weapon))
}

// Handle selection change for multiple selection
const handleSelectionChange = (selection) => {
  selectedWeapons.value = selection
  emit('update:modelValue', selection)
  emit('selection-change', selection)
}

// Handle single selection
const handleSingleSelection = (weapon) => {
  const isCurrentlySelected = isSelected(weapon)
  if (isCurrentlySelected) {
    selectedWeapons.value = []
  } else {
    selectedWeapons.value = [weapon]
  }
  emit('update:modelValue', selectedWeapons.value)
  emit('selection-change', selectedWeapons.value)
}

// Handle attack roll button click
const handleAttack = (weapon) => {
  emit('attack', weapon)
}

// Handle damage roll button click
const handleDamage = (weapon) => {
  emit('damage', weapon)
}

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  selectedWeapons.value = [...newValue]
}, { deep: true })
</script>

<style scoped>
.weapon-table {
  width: 100%;
}

:deep(.el-radio__label) {
  display: none;
}
</style>
