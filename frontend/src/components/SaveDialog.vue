<template>
  <el-dialog
    v-model="visible"
    title="Save Character"
    width="500px"
    @close="handleClose"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="Character Name" required>
        <el-input
          v-model="formData.characterName"
          placeholder="Enter character name"
          :disabled="true"
        >
          <template #append>
            <el-tooltip content="Edit name in main tab">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="Save As">
        <el-radio-group v-model="saveMode">
          <el-radio label="update">Update existing character</el-radio>
          <el-radio label="new">Save as new character</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-alert
        v-if="saveMode === 'update'"
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom: 15px;"
      >
        This will update the currently loaded character.
      </el-alert>

      <el-alert
        v-if="saveMode === 'new'"
        type="warning"
        :closable="false"
        show-icon
        style="margin-bottom: 15px;"
      >
        This will create a new saved character.
      </el-alert>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button
          type="primary"
          @click="handleSave"
          :disabled="!formData.characterName"
        >
          Save
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  characterName: {
    type: String,
    default: ''
  },
  hasExistingCharacter: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const visible = ref(props.modelValue)
const saveMode = ref(props.hasExistingCharacter ? 'update' : 'new')
const formData = ref({
  characterName: props.characterName
})

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  visible.value = newValue
})

watch(() => props.characterName, (newValue) => {
  formData.value.characterName = newValue
})

watch(() => props.hasExistingCharacter, (newValue) => {
  saveMode.value = newValue ? 'update' : 'new'
})

// Update parent when dialog visibility changes
watch(visible, (newValue) => {
  emit('update:modelValue', newValue)
})

const handleClose = () => {
  visible.value = false
}

const handleSave = () => {
  emit('save', {
    mode: saveMode.value,
    characterName: formData.value.characterName
  })
  visible.value = false
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
