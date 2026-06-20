<template>
  <div class="categorized-select" ref="selectRef">
    <el-popover
      :visible="dropdownVisible"
      placement="bottom-start"
      :width="popoverWidth"
      trigger="manual"
      popper-class="categorized-select-popper"
      @hide="dropdownVisible = false"
    >
      <template #reference>
        <div
          class="select-trigger"
          @click="toggleDropdown"
        >
          <div class="selected-tags" v-if="selectedValues.length > 0">
            <el-tag
              v-for="value in selectedValues"
              :key="value"
              closable
              @close="removeSelection(value)"
              class="selected-tag"
              type="info"
            >
              {{ getLabelForValue(value) }}
            </el-tag>
          </div>
          <span v-else class="placeholder">{{ placeholder }}</span>
          <el-icon class="dropdown-icon" :class="{ 'is-reverse': dropdownVisible }">
            <ArrowDown />
          </el-icon>
        </div>
      </template>

      <div class="dropdown-content">
        <!-- Categorized options -->
        <div class="options-container">
          <div
            v-for="category in categorizedOptions"
            :key="category.name"
            class="category-group"
          >
            <div class="category-header">{{ category.name }}</div>
            <div
              v-for="option in category.options"
              :key="option.value"
              class="option-item"
              :class="{ 'is-selected': isSelected(option.value) }"
              @click="toggleOption(option.value)"
            >
              <span class="option-label">{{ option.name }}</span>
              <div class="option-tags">
                <el-tag size="small" type="warning">{{ option.category }}</el-tag>
                <el-tag size="small" type="info">{{ option.cost }}</el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-popover>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    required: true,
    // Expected format: [{ value: 'name', label: 'Name (cost)', category: 'Combat' }, ...]
  },
  placeholder: {
    type: String,
    default: 'Select options'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const selectRef = ref(null)
const dropdownVisible = ref(false)
const selectedValues = ref([...props.modelValue])
const popoverWidth = ref('auto')

// Organize options by category
const categorizedOptions = computed(() => {
  const categories = {}

  props.options.forEach(option => {
    const category = option.category || 'Other'
    if (!categories[category]) {
      categories[category] = []
    }
    categories[category].push(option)
  })

  // Convert to array format with sorting
  return Object.entries(categories).map(([name, options]) => ({
    name,
    options: options.sort((a, b) => a.label.localeCompare(b.label))
  })).sort((a, b) => a.name.localeCompare(b.name))
})

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  selectedValues.value = [...newValue]
})

// Update popover width when dropdown opens
const updatePopoverWidth = async () => {
  await nextTick()
  if (selectRef.value) {
    const width = selectRef.value.offsetWidth
    popoverWidth.value = width
  }
}

// Toggle dropdown visibility
const toggleDropdown = () => {
  dropdownVisible.value = !dropdownVisible.value
  if (dropdownVisible.value) {
    updatePopoverWidth()
  }
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const selectElement = event.target.closest('.categorized-select')
  const popperElement = event.target.closest('.categorized-select-popper')

  if (!selectElement && !popperElement && dropdownVisible.value) {
    dropdownVisible.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  updatePopoverWidth()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Check if option is selected
const isSelected = (value) => {
  return selectedValues.value.includes(value)
}

// Toggle option selection
const toggleOption = (value) => {
  const index = selectedValues.value.indexOf(value)

  if (index > -1) {
    selectedValues.value.splice(index, 1)
  } else {
    selectedValues.value.push(value)
  }

  emit('update:modelValue', selectedValues.value)
  emit('change', selectedValues.value)
}

// Remove a selected value
const removeSelection = (value) => {
  const index = selectedValues.value.indexOf(value)
  if (index > -1) {
    selectedValues.value.splice(index, 1)
    emit('update:modelValue', selectedValues.value)
    emit('change', selectedValues.value)
  }
}

// Get label for a value
const getLabelForValue = (value) => {
  const option = props.options.find(opt => opt.value === value)
  return option ? option.label : value
}
</script>

<style scoped>
.categorized-select {
  width: 100%;
}

.select-trigger {
  min-height: 40px;
  padding: 4px 8px;
  border: 1px solid var(--el-border-color);
  border-radius: var(--el-border-radius-base);
  background-color: var(--el-fill-color-blank);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: border-color 0.2s;
  position: relative;
}

.select-trigger:hover {
  border-color: var(--el-border-color-hover);
}

.selected-tags {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  min-height: 24px;
}

.selected-tag {
  margin: 2px 0;
}

.placeholder {
  flex: 1;
  color: var(--el-text-color-placeholder);
  user-select: none;
}

.dropdown-icon {
  margin-left: auto;
  transition: transform 0.3s;
}

.dropdown-icon.is-reverse {
  transform: rotate(180deg);
}

.dropdown-content {
  max-height: 400px;
  display: flex;
  flex-direction: column;
}

.options-container {
  overflow-y: auto;
  max-height: 400px;
}

.category-group {
  margin-bottom: 4px;
}

.category-header {
  padding: 8px 12px;
  font-weight: 600;
  font-size: 13px;
  color: var(--el-text-color-regular);
  background-color: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
  position: sticky;
  top: 0;
  z-index: 5;
}

.option-item {
  padding: 8px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  user-select: none;
}

.option-item:hover {
  background-color: var(--el-fill-color-light);
}

.option-item.is-selected {
  background-color: var(--el-color-primary-light-9);
}

.option-label {
  flex: 1;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.option-tags {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

</style>

<style>
/* Global styles for the popper */
.categorized-select-popper {
  padding: 0 !important;
}

.categorized-select-popper .el-popover__title {
  display: none;
}
</style>
