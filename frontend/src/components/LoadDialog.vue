<template>
  <el-dialog
    v-model="visible"
    title="Load Character"
    width="700px"
    @close="handleClose"
  >
    <div v-if="characters.length === 0" class="empty-state">
      <el-empty description="No saved characters found">
        <el-button type="primary" @click="handleClose">
          Create New Character
        </el-button>
      </el-empty>
    </div>

    <div v-else>
      <el-input
        v-model="searchText"
        placeholder="Search characters..."
        clearable
        style="margin-bottom: 15px;"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-table
        :data="filteredCharacters"
        height="400"
        highlight-current-row
        @current-change="handleCurrentChange"
        style="width: 100%"
      >
        <el-table-column
          prop="name"
          label="Character Name"
          min-width="150"
          sortable
        >
          <template #default="scope">
            <div class="character-name">
              <strong>{{ scope.row.name || 'Unnamed Character' }}</strong>
            </div>
          </template>
        </el-table-column>

        <el-table-column
          prop="char_class"
          label="Class"
          width="100"
          sortable
        />

        <el-table-column
          prop="level"
          label="Level"
          width="80"
          sortable
        />

        <el-table-column
          label="Last Modified"
          width="150"
          sortable
          :sort-method="sortByDate"
        >
          <template #default="scope">
            {{ formatDate(scope.row.updated_at) }}
          </template>
        </el-table-column>

        <el-table-column
          label="Actions"
          width="100"
          fixed="right"
        >
          <template #default="scope">
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(scope.row)"
              circle
            />
          </template>
        </el-table-column>
      </el-table>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button
          type="primary"
          @click="handleLoad"
          :disabled="!selectedCharacter"
        >
          Load Character
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Search, Delete } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  characters: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'load', 'delete'])

const visible = ref(props.modelValue)
const searchText = ref('')
const selectedCharacter = ref(null)

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  visible.value = newValue
  if (newValue) {
    // Reset selection when dialog opens
    selectedCharacter.value = null
    searchText.value = ''
  }
})

// Update parent when dialog visibility changes
watch(visible, (newValue) => {
  emit('update:modelValue', newValue)
})

// Filter characters based on search
const filteredCharacters = computed(() => {
  if (!searchText.value) {
    return props.characters
  }
  const search = searchText.value.toLowerCase()
  return props.characters.filter(char =>
    (char.name || '').toLowerCase().includes(search) ||
    (char.char_class || '').toLowerCase().includes(search) ||
    (char.player_name || '').toLowerCase().includes(search)
  )
})

const handleCurrentChange = (row) => {
  selectedCharacter.value = row
}

const handleClose = () => {
  visible.value = false
}

const handleLoad = () => {
  if (selectedCharacter.value) {
    emit('load', selectedCharacter.value)
    visible.value = false
  }
}

const handleDelete = (character) => {
  ElMessageBox.confirm(
    `Are you sure you want to delete "${character.name || 'Unnamed Character'}"? This action cannot be undone.`,
    'Delete Character',
    {
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(() => {
    emit('delete', character)
  }).catch(() => {
    // User cancelled
  })
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

const sortByDate = (a, b) => {
  const dateA = new Date(a.updated_at || 0)
  const dateB = new Date(b.updated_at || 0)
  return dateB - dateA // Most recent first
}
</script>

<style scoped>
.empty-state {
  padding: 40px 0;
}

.character-name {
  display: flex;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
