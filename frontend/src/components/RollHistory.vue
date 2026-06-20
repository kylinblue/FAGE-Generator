<template>
  <div class="roll-history" :class="{ collapsed: !expanded }">
    <button
      v-if="!expanded"
      class="rh-toggle"
      type="button"
      @click="expanded = true"
      title="Open roll history"
    >
      <el-icon><Document /></el-icon>
      <span>History</span>
      <span v-if="store.entries.length" class="rh-badge">{{ store.entries.length }}</span>
    </button>

    <div v-else class="rh-panel">
      <div class="rh-header">
        <span class="rh-title">Roll History</span>
        <div class="rh-actions">
          <button
            v-if="store.entries.length"
            class="rh-action"
            type="button"
            @click="store.clear"
            title="Clear history"
            aria-label="Clear history"
          >
            <el-icon><Delete /></el-icon>
          </button>
          <button
            class="rh-action"
            type="button"
            @click="expanded = false"
            title="Minimize"
            aria-label="Minimize history"
          >
            <el-icon><Minus /></el-icon>
          </button>
        </div>
      </div>

      <div class="rh-body">
        <div v-if="!store.entries.length" class="rh-empty">
          No rolls yet. Roll an attack, damage, spell, or ability to see it here.
        </div>

        <div
          v-for="entry in store.entries"
          :key="entry.id"
          class="rh-entry"
        >
          <div class="rh-entry-head">
            <span class="rh-entry-title">{{ entry.title }}</span>
            <span class="rh-entry-time">{{ formatTime(entry.ts) }}</span>
          </div>

          <div class="dice-display-inline">
            <el-tag
              v-for="(d, i) in entry.dice"
              :key="i"
              size="small"
              :type="variantType(d.variant)"
              class="die-tag-inline"
            >{{ d.value }}</el-tag>
          </div>

          <div class="roll-details">
            <p v-for="(line, i) in entry.lines" :key="i">{{ line }}</p>
            <p
              class="final-result"
              :style="totalStyle(entry.totalClass)"
            >{{ entry.totalLabel }}: {{ entry.totalValue }}</p>
            <p v-if="entry.stuntPoints" class="stunt-notice">
              ✨ Stunt! SP: {{ entry.stuntPoints }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Document, Minus, Delete } from '@element-plus/icons-vue'
import { useRollHistoryStore } from '../stores/rollHistory'

const store = useRollHistoryStore()
const expanded = ref(false)

function variantType(variant) {
  if (variant === 'stunt') return 'danger'
  if (variant === 'bonus') return 'success'
  return undefined
}

function totalStyle(cls) {
  if (cls === 'success') return 'color: #67c23a; font-weight: bold'
  if (cls === 'danger') return 'color: #f56c6c; font-weight: bold'
  return ''
}

function formatTime(ts) {
  const d = new Date(ts)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.roll-history {
  display: inline-block;
}

.rh-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 999px;
  background: linear-gradient(90deg, #5a3a8a 0%, #9c5fd1 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.rh-toggle:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

.rh-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.25);
  font-size: 12px;
  font-weight: 700;
}

.rh-panel {
  width: 256px;
  max-height: 48vh;
  background-color: var(--el-bg-color, #fff);
  border: 1px solid var(--el-border-color, #dcdfe6);
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.rh-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #5a3a8a 0%, #9c5fd1 100%);
  color: white;
  padding: 8px 12px;
  flex-shrink: 0;
}

.rh-title {
  font-weight: 700;
  letter-spacing: 0.5px;
}

.rh-actions {
  display: flex;
  gap: 6px;
}

.rh-action {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.rh-action:hover {
  background: rgba(255, 255, 255, 0.35);
}

.rh-body {
  padding: 8px;
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rh-empty {
  padding: 16px 8px;
  text-align: center;
  color: var(--el-text-color-secondary);
  font-size: 13px;
  font-style: italic;
}

.rh-entry {
  background-color: var(--el-fill-color-lighter, #fafbfc);
  border: 1px solid var(--el-border-color-lighter, #ebeef5);
  border-radius: 6px;
  padding: 8px 10px;
}

html.dark .rh-entry {
  background-color: #222;
  border-color: #333;
}

.rh-entry-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.rh-entry-title {
  font-weight: 700;
  font-size: 13px;
  color: var(--el-text-color-primary);
}

.rh-entry-time {
  font-size: 11px;
  color: var(--el-text-color-secondary);
}

.rh-entry .dice-display-inline {
  display: flex;
  gap: 4px;
  margin: 4px 0;
  flex-wrap: wrap;
}

.rh-entry .die-tag-inline {
  font-size: 13px;
  padding: 2px 8px;
  font-weight: bold;
}

.rh-entry .roll-details {
  font-size: 12px;
  line-height: 1.5;
}

.rh-entry .roll-details p {
  margin: 2px 0;
}

.rh-entry .final-result {
  font-size: 13px;
  font-weight: bold;
  margin-top: 4px;
  padding-top: 4px;
  border-top: 1px solid var(--el-border-color-lighter, #ebeef5);
}

.rh-entry .stunt-notice {
  color: #67c23a;
  font-weight: bold;
}

html.dark .rh-panel {
  background-color: #1a1a1a;
  border-color: #333;
}
</style>
