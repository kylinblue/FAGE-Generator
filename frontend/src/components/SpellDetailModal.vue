<template>
  <el-dialog
    v-model="dialogVisible"
    :title="spell?.Name || 'Spell Details'"
    width="600px"
    @close="handleClose"
  >
    <div v-if="spell" class="spell-details">
      <!-- Spell Header Info -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="Requirement">
          <el-tag>{{ spell.Arcana }}{{ spell.Degree ? ` (${spell.Degree})` : '' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="MP Cost">
          <strong>{{ spell.MP || 0 }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="Type">
          <el-tag :type="getSpellTypeTag(spell.SpellType)">
            {{ spell.SpellType || 'N/A' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="Target Number">
          <strong>{{ spell.TN || 0 }}</strong>
        </el-descriptions-item>
        <el-descriptions-item label="Casting Time" :span="2">
          {{ spell.CastTime || 'N/A' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="spell.Test" label="Test" :span="2">
          {{ spell.Test }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- Spell Effect -->
      <div class="effect-section">
        <h4>Effect</h4>
        <div class="effect-text" v-html="spell.Effect || 'No description available.'"></div>
      </div>

      <!-- Source Reference -->
      <div v-if="spell.Source || spell.Page" class="source-section">
        <el-text size="small" type="info">
          Source: {{ spell.Source || 'Unknown' }}
          <span v-if="spell.Page"> (Page {{ spell.Page }})</span>
        </el-text>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Close</el-button>
        <el-button
          v-if="showCastButton"
          type="primary"
          @click="handleCast"
        >
          Cast Spell
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  spell: {
    type: Object,
    default: null
  },
  showCastButton: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'cast'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const getSpellTypeTag = (type) => {
  const typeMap = {
    'Attack': 'danger',
    'Defense': 'success',
    'Utility': 'info',
    'Healing': 'success'
  }
  return typeMap[type] || ''
}

const handleClose = () => {
  dialogVisible.value = false
}

const handleCast = () => {
  emit('cast', props.spell)
  dialogVisible.value = false
}
</script>

<style scoped>
.spell-details {
  padding: 10px 0;
}

.effect-section {
  margin-top: 20px;
}

.effect-section h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

html.dark .effect-section h4 {
  color: #e5e7eb;
}

.effect-text {
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
}

html.dark .effect-text {
  background-color: #2a2a2a;
  color: #e5e7eb;
}

.source-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
