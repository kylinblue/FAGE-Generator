<template>
  <div class="focus-select">
    <el-form-item :label="`${statName} - Focus (1)`">
      <el-select
        :model-value="primaryFoci"
        @update:model-value="updatePrimaryFoci"
        placeholder="Select primary foci"
        multiple
        collapse-tags
        collapse-tags-tooltip
        filterable
        clearable
        style="width: 100%"
      >
        <el-option
          v-for="focus in availableFoci"
          :key="focus"
          :label="focus"
          :value="focus"
        />
      </el-select>
    </el-form-item>

    <!-- Secondary focus only available at level 11+ -->
    <el-form-item
      v-if="characterLevel >= 11"
      :label="`${statName} - Focus (2)`"
    >
      <el-select
        :model-value="secondaryFoci"
        @update:model-value="updateSecondaryFoci"
        placeholder="Select secondary foci"
        multiple
        collapse-tags
        collapse-tags-tooltip
        filterable
        clearable
        style="width: 100%"
        :disabled="!primaryFoci || primaryFoci.length === 0"
      >
        <el-option
          v-for="focus in primaryFoci"
          :key="focus"
          :label="`${focus} (2)`"
          :value="focus"
        />
      </el-select>
      <div v-if="!primaryFoci || primaryFoci.length === 0" class="hint-text">
        Select a primary focus first
      </div>
    </el-form-item>

    <!-- Display formatted foci with counts -->
    <div v-if="formattedFoci" class="foci-display">
      <el-tag
        v-for="(fociText, index) in formattedFoci.split(', ')"
        :key="index"
        type="info"
        size="small"
        style="margin-right: 5px; margin-bottom: 5px;"
      >
        {{ fociText }}
      </el-tag>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  statName: {
    type: String,
    required: true
  },
  primaryFoci: {
    type: Array,
    default: () => []
  },
  secondaryFoci: {
    type: Array,
    default: () => []
  },
  availableFoci: {
    type: Array,
    default: () => []
  },
  characterLevel: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['update:primaryFoci', 'update:secondaryFoci'])

function updatePrimaryFoci(value) {
  emit('update:primaryFoci', value)

  // Clear secondary foci if primary focus was removed
  if (props.secondaryFoci && props.secondaryFoci.length > 0) {
    const validSecondary = props.secondaryFoci.filter(sf => value.includes(sf))
    if (validSecondary.length !== props.secondaryFoci.length) {
      emit('update:secondaryFoci', validSecondary)
    }
  }
}

function updateSecondaryFoci(value) {
  emit('update:secondaryFoci', value)
}

// Format foci with counts (e.g., "Brawling (2)" if selected twice)
const formattedFoci = computed(() => {
  const allFoci = [...(props.primaryFoci || []), ...(props.secondaryFoci || [])]
  if (allFoci.length === 0) return ''

  const counted = {}
  allFoci.forEach(focus => {
    counted[focus] = (counted[focus] || 0) + 1
  })

  const formatted = Object.entries(counted).map(([name, count]) => {
    return count > 1 ? `${name} (${count})` : name
  })

  return formatted.join(', ')
})
</script>

<style scoped>
.focus-select {
  margin-bottom: 15px;
}

.hint-text {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.foci-display {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}
</style>
