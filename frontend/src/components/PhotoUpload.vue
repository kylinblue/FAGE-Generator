<template>
  <div class="photo-upload">
    <div class="photo-container">
      <div v-if="photoPreview" class="photo-preview">
        <img :src="photoPreview" alt="Character Photo" />
        <div class="photo-overlay">
          <el-button
            type="danger"
            :icon="Delete"
            circle
            size="small"
            @click="removePhoto"
            class="remove-btn"
          />
        </div>
      </div>
      <div v-else class="photo-placeholder">
        <el-icon :size="48" color="#ccc">
          <User />
        </el-icon>
        <p>No Photo</p>
      </div>
    </div>

    <el-upload
      :show-file-list="false"
      :before-upload="beforeUpload"
      :on-change="handleChange"
      accept="image/*"
      :auto-upload="false"
    >
      <el-button :icon="Upload" type="primary">
        {{ photoPreview ? 'Change Photo' : 'Upload Photo' }}
      </el-button>
    </el-upload>

    <p class="hint">Max size: 5MB. Formats: JPG, PNG, GIF</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Upload, Delete } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const photoPreview = ref(props.modelValue)

// Watch for external changes to modelValue
watch(() => props.modelValue, (newVal) => {
  photoPreview.value = newVal
})

// Validate file before upload
function beforeUpload(file) {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('Please upload an image file!')
    return false
  }

  if (!isLt5M) {
    ElMessage.error('Image size must be less than 5MB!')
    return false
  }

  return true
}

// Handle file selection
function handleChange(file) {
  const rawFile = file.raw

  if (!rawFile) {
    return
  }

  // Validate
  const isValid = beforeUpload(rawFile)
  if (!isValid) {
    return
  }

  // Read file as base64
  const reader = new FileReader()

  reader.onload = (e) => {
    const base64String = e.target.result
    photoPreview.value = base64String
    emit('update:modelValue', base64String)
    ElMessage.success('Photo uploaded successfully!')
  }

  reader.onerror = () => {
    ElMessage.error('Failed to read image file')
  }

  reader.readAsDataURL(rawFile)
}

// Remove photo
function removePhoto() {
  photoPreview.value = null
  emit('update:modelValue', null)
  ElMessage.info('Photo removed')
}
</script>

<style scoped>
.photo-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 20px;
}

.photo-container {
  width: 200px;
  height: 200px;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background-color: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-preview {
  width: 100%;
  height: 100%;
  position: relative;
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.photo-preview:hover .photo-overlay {
  opacity: 1;
}

.remove-btn {
  background-color: rgba(255, 255, 255, 0.9) !important;
}

.photo-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #999;
}

.photo-placeholder p {
  margin: 0;
  font-size: 14px;
}

.hint {
  font-size: 12px;
  color: #909399;
  margin: 0;
  text-align: center;
}

/* Dark mode support */
html.dark .photo-container {
  background-color: #1a1a1a;
  border-color: #3a3a3a;
}

html.dark .photo-placeholder {
  color: #666;
}

html.dark .hint {
  color: #666;
}
</style>
