<template>
  <div class="inventory-table">
    <div class="table-header">
      <span class="header-title">Inventory</span>
      <el-button
        type="primary"
        size="small"
        @click="addItem"
        :icon="Plus"
      >
        Add Item
      </el-button>
    </div>

    <el-table
      :data="inventoryData"
      style="width: 100%"
      :empty-text="'No items in inventory'"
      max-height="400"
    >
      <el-table-column label="Item" min-width="200">
        <template #default="scope">
          <el-input
            v-model="scope.row.item"
            placeholder="Item name"
            @change="handleItemChange(scope.$index)"
            :disabled="!scope.row.editing && !scope.row.isNew"
          />
        </template>
      </el-table-column>

      <el-table-column label="Quantity" width="150">
        <template #default="scope">
          <el-input-number
            v-model="scope.row.quantity"
            :min="1"
            :max="9999"
            @change="handleItemChange(scope.$index)"
            :disabled="!scope.row.editing && !scope.row.isNew"
          />
        </template>
      </el-table-column>

      <el-table-column label="Actions" width="150" align="center">
        <template #default="scope">
          <el-button
            v-if="scope.row.editing || scope.row.isNew"
            type="success"
            size="small"
            @click="saveItem(scope.$index)"
            :icon="Check"
            circle
          />
          <el-button
            v-if="scope.row.editing || scope.row.isNew"
            type="info"
            size="small"
            @click="cancelEdit(scope.$index)"
            :icon="Close"
            circle
          />
          <el-button
            v-if="!scope.row.editing && !scope.row.isNew"
            type="primary"
            size="small"
            @click="editItem(scope.$index)"
            :icon="Edit"
            circle
          />
          <el-button
            v-if="!scope.row.editing && !scope.row.isNew"
            type="danger"
            size="small"
            @click="removeItem(scope.$index)"
            :icon="Delete"
            circle
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Plus, Delete, Edit, Check, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

// Internal inventory data with editing state
const inventoryData = ref([])

// Initialize inventory data from props
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue && newValue.length > 0) {
      inventoryData.value = newValue.map(item => ({
        ...item,
        editing: false,
        isNew: false,
        original: { ...item }
      }))
    } else {
      inventoryData.value = []
    }
  },
  { immediate: true }
)

// Add new item
function addItem() {
  inventoryData.value.push({
    item: '',
    quantity: 1,
    editing: true,
    isNew: true,
    original: null
  })
}

// Edit existing item
function editItem(index) {
  inventoryData.value[index].editing = true
  inventoryData.value[index].original = {
    item: inventoryData.value[index].item,
    quantity: inventoryData.value[index].quantity
  }
}

// Save item (finish editing)
function saveItem(index) {
  const item = inventoryData.value[index]

  // Validate item name
  if (!item.item || item.item.trim() === '') {
    ElMessage.warning('Item name cannot be empty')
    return
  }

  // Validate quantity
  if (!item.quantity || item.quantity < 1) {
    ElMessage.warning('Quantity must be at least 1')
    return
  }

  item.editing = false
  item.isNew = false
  delete item.original

  emitUpdate()
  ElMessage.success('Item saved')
}

// Cancel edit
function cancelEdit(index) {
  const item = inventoryData.value[index]

  if (item.isNew) {
    // Remove new item if cancelled
    inventoryData.value.splice(index, 1)
  } else {
    // Restore original values
    item.item = item.original.item
    item.quantity = item.original.quantity
    item.editing = false
    delete item.original
  }
}

// Remove item
function removeItem(index) {
  inventoryData.value.splice(index, 1)
  emitUpdate()
  ElMessage.success('Item removed')
}

// Handle item change
function handleItemChange(index) {
  // Auto-save when editing existing items
  const item = inventoryData.value[index]
  if (!item.isNew && !item.editing) {
    emitUpdate()
  }
}

// Emit update to parent
function emitUpdate() {
  const cleanData = inventoryData.value
    .filter(item => !item.isNew && !item.editing)
    .map(({ item, quantity }) => ({ item, quantity }))
  emit('update:modelValue', cleanData)
}
</script>

<style scoped>
.inventory-table {
  width: 100%;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
}

:deep(.el-input-number) {
  width: 100%;
}
</style>
