<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-brand">
            <img src="/FageIcon2.png" alt="FAGE Logo" class="app-logo" />
            <div>
              <h1 class="app-title">FAGE Character Generator</h1>
              <p class="app-subtitle">Fantasy AGE Character Sheet Manager</p>
            </div>
          </div>
        </div>

        <div class="header-center">
          <nav class="tab-nav">
            <a
              v-for="tab in tabs"
              :key="tab.name"
              :class="['tab-link', { active: activeTab === tab.name }]"
              @click="handleTabChange(tab.name)"
            >
              <el-icon><component :is="tab.icon" /></el-icon>
              <span>{{ tab.label }}</span>
            </a>
          </nav>
        </div>

        <div class="header-right">
          <el-button @click="saveDialogVisible = true" size="small" type="primary">
            Save
          </el-button>
          <el-button @click="loadDialogVisible = true" size="small">
            Load
          </el-button>
          <el-button @click="exportPDF" size="small">
            Export PDF
          </el-button>
          <el-tooltip
            :content="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
            placement="bottom"
          >
            <el-button
              :icon="isDark ? Sunny : Moon"
              circle
              size="large"
              @click="toggleDarkMode"
              class="theme-toggle"
            />
          </el-tooltip>
        </div>
      </div>
    </el-header>

    <!-- Width Warning Banner -->
    <div v-if="showWidthWarning" class="width-warning-banner">
      <el-icon class="warning-icon"><WarningFilled /></el-icon>
      <div class="warning-content">
        <strong>Window Too Narrow</strong>
        <span>Content may be clipped or hidden. Please expand your browser window to at least 1400px for the best experience. Current width: {{ windowWidth }}px</span>
      </div>
    </div>

    <el-container class="main-container">
      <el-aside width="380px" class="app-sidebar">
        <CharacterSidebar />
      </el-aside>

      <el-main class="app-main">
        <div class="router-content">
          <router-view />
        </div>
      </el-main>
    </el-container>

    <el-footer class="app-footer">
      <p>FAGE Character Generator v2.0</p>
      <el-button
        :icon="FolderOpened"
        size="small"
        text
        class="footer-action"
        @click="openDataFolder"
      >
        Open data folder
      </el-button>
    </el-footer>

    <!-- Save Character Dialog -->
    <SaveDialog
      v-model="saveDialogVisible"
      :character-name="character.name"
      :has-existing-character="!!character.id"
      @save="handleSave"
    />

    <!-- Load Character Dialog -->
    <LoadDialog
      v-model="loadDialogVisible"
      :characters="savedCharacters"
      @load="handleLoad"
      @delete="handleDeleteCharacter"
    />

    <!-- Stat Generation Dialog (rolled / point-buy) -->
    <StatGenerationDialog v-model="uiStore.statGenDialogVisible" />

    <!-- Floating bottom-left stack: roll history above, arbitrary dice roller below -->
    <div class="floating-corner-left">
      <RollHistory />
      <ArbitraryDiceRoller />
    </div>
  </el-container>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { User, MagicStick, Briefcase, TrendCharts, Moon, Sunny, WarningFilled, FolderOpened } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useCharacterStore } from './stores/character'
import { useDarkMode } from './composables/useDarkMode'
import CharacterSidebar from './components/CharacterSidebar.vue'
import SaveDialog from './components/SaveDialog.vue'
import LoadDialog from './components/LoadDialog.vue'
import StatGenerationDialog from './components/StatGenerationDialog.vue'
import ArbitraryDiceRoller from './components/ArbitraryDiceRoller.vue'
import RollHistory from './components/RollHistory.vue'
import { useUIStore } from './stores/ui'
import api from './utils/api'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const characterStore = useCharacterStore()
const uiStore = useUIStore()
const { isDark, toggleDarkMode } = useDarkMode()

const activeTab = ref('main')
const saveDialogVisible = ref(false)
const loadDialogVisible = ref(false)
const windowWidth = ref(window.innerWidth)

const character = computed(() => characterStore.character)
const savedCharacters = computed(() => characterStore.getAllSavedCharacters())
const showWidthWarning = computed(() => windowWidth.value < 1400)

// Tab navigation configuration
const tabs = [
  { name: 'main', label: 'Main', icon: User },
  { name: 'magic', label: 'Magic', icon: MagicStick },
  { name: 'inventory', label: 'Inventory', icon: Briefcase },
  { name: 'levelup', label: 'Level-Up', icon: TrendCharts }
]

// Watch route changes and update active tab
watch(() => route.path, (newPath) => {
  const pathToTab = {
    '/main': 'main',
    '/magic': 'magic',
    '/inventory': 'inventory',
    '/levelup': 'levelup'
  }
  activeTab.value = pathToTab[newPath] || 'main'
}, { immediate: true })

// Handle tab changes
function handleTabChange(tabName) {
  const tabToPath = {
    'main': '/main',
    'magic': '/magic',
    'inventory': '/inventory',
    'levelup': '/levelup'
  }
  router.push(tabToPath[tabName] || '/main')
}

// Handle save
function handleSave(saveData) {
  if (saveData.mode === 'new') {
    characterStore.saveToLocalStorage(true) // Force new save
  } else {
    characterStore.saveToLocalStorage(false) // Update existing
  }
  saveDialogVisible.value = false
  ElMessage.success('Character saved successfully!')
}

// Handle load
function handleLoad(loadedCharacter) {
  characterStore.loadFromLocalStorage(loadedCharacter.id)
  loadDialogVisible.value = false
  ElMessage.success(`Loaded ${loadedCharacter.name}!`)
}

// Handle delete
function handleDeleteCharacter(characterId) {
  characterStore.deleteCharacter(characterId)
  ElMessage.success('Character deleted!')
}

// Export PDF
async function exportPDF() {
  try {
    ElMessage.info('Generating PDF...')
    const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    const response = await axios.post(
      `${API_BASE}/api/export/pdf`,
      character.value,
      { responseType: 'blob' }
    )

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${character.value.name || 'character'}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    ElMessage.success('PDF downloaded successfully!')
  } catch (error) {
    console.error('PDF export error:', error)

    // Error responses from a blob-typed request arrive as Blob — read it back.
    let detail = null
    if (error.response?.data instanceof Blob) {
      try {
        const text = await error.response.data.text()
        detail = JSON.parse(text).detail
      } catch (_) { /* not JSON */ }
    } else {
      detail = error.response?.data?.detail
    }

    if (error.response?.status === 400 && detail && typeof detail === 'object') {
      const fields = (detail.missing_fields || []).join(', ')
      ElMessage({
        type: 'warning',
        duration: 6000,
        message: `${detail.message}${fields ? ` Missing: ${fields}.` : ''}`,
      })
    } else {
      ElMessage.error(typeof detail === 'string' ? detail : 'Failed to export PDF')
    }
  }
}

// Open the local data folder via the backend (desktop app only).
async function openDataFolder() {
  try {
    const { data } = await api.post('/api/system/open-data-dir')
    ElMessage.success(`Opened ${data.opened}`)
  } catch (error) {
    // The api interceptor already surfaces an error toast.
    console.error('Open data folder error:', error)
  }
}

// Window resize handler
function handleResize() {
  windowWidth.value = window.innerWidth
}

// Load last character on mount and set up resize listener
onMounted(() => {
  const loaded = characterStore.loadLastCharacter()
  if (!loaded) {
    uiStore.showStatGenDialog()
  }
  window.addEventListener('resize', handleResize)
})

// Clean up resize listener
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style>
/* Global styles */
@import url('https://fonts.googleapis.com/css2?family=Book+Antiqua&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  width: 100%;
  max-width: none;
  overflow-x: hidden;
}

body {
  font-family: 'Book Antiqua', 'Palatino Linotype', Palatino, serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: var(--paper-bg, #f5f7fa);
  background-image: var(--paper-texture);
  transition: background-color 0.3s ease;
  width: 100%;
  max-width: none;
  margin: 0;
  padding: 0;
}

/* Header font styling */
h1, h2, h3, h4, h5, h6,
.section-title,
.card-header,
.app-title {
  font-family: 'Ringbearer Medium', Georgia, serif !important;
  font-variant: small-caps;
  color: #004E83;
}

html.dark h1, html.dark h2, html.dark h3, html.dark h4, html.dark h5, html.dark h6,
html.dark .section-title,
html.dark .card-header {
  color: #4A9EDB;
}

/* Dark mode body background */
html.dark body {
  background-color: #0a0a0a;
}

#app {
  width: 100% !important;
  max-width: none !important;
  min-height: 100vh;
  margin: 0 !important;
  padding: 0 !important;
}
</style>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: none;
}

.app-header {
  background: linear-gradient(90deg, #0d5a8a 0%, #2196f3 100%);
  color: white;
  padding: 20px 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
  height: auto;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 32px;
}

.header-left {
  flex-shrink: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 6px;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: white !important;
}

.app-subtitle {
  font-size: 13px;
  opacity: 0.9;
  margin: 0;
  color: white;
}

/* Tab Navigation */
.tab-nav {
  display: flex;
  gap: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 6px;
  border-radius: 8px;
}

.tab-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

.tab-link.active {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Main container with sidebar */
.main-container {
  flex: 1;
  overflow: hidden;
  width: 100%;
  max-width: none;
}

.app-sidebar {
  background-color: var(--paper-surface, #fafbfc);
  background-image: var(--paper-texture);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
  height: 100%;
}

html.dark .app-sidebar {
  background-color: #1a1a1a;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
}

.app-main {
  flex: 1;
  padding: 20px;
  background-color: var(--paper-bg, #f5f7fa);
  background-image: var(--paper-texture);
  transition: background-color 0.3s ease;
  overflow-y: auto;
  width: 100%;
  max-width: none;
}

.router-content {
  width: 100%;
  margin: 0;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 16px;
  font-size: 14px;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.app-footer p {
  margin: 0;
}

.footer-action {
  color: rgba(255, 255, 255, 0.85);
  /* text buttons default to a transparent border at higher specificity, so
     force the border to make it visible against the dark footer. */
  border: 1px solid rgba(255, 255, 255, 0.35) !important;
}

.footer-action:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.6) !important;
}

html.dark .footer-action {
  border-color: rgba(255, 255, 255, 0.25) !important;
}

html.dark .footer-action:hover {
  border-color: rgba(255, 255, 255, 0.45) !important;
}

.theme-toggle {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
  transform: scale(1.1);
}

.theme-toggle:active {
  transform: scale(0.95);
}

/* Header buttons styling */
.header-right :deep(.el-button) {
  color: white;
  background-color: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.header-right :deep(.el-button--primary) {
  background-color: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}

.header-right :deep(.el-button):hover {
  background-color: rgba(255, 255, 255, 0.35);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Dark mode adjustments */
html.dark .app-main {
  background-color: #0a0a0a;
}

/* Width Warning Banner */
.width-warning-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  background-color: #fff3cd;
  border-bottom: 3px solid #ffc107;
  color: #856404;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 9;
  position: relative;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.warning-icon {
  font-size: 24px;
  color: #ffc107;
  flex-shrink: 0;
}

.warning-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.warning-content strong {
  font-size: 16px;
  color: #664d03;
}

.warning-content span {
  font-size: 14px;
}

html.dark .width-warning-banner {
  background-color: #4a3a00;
  border-bottom-color: #ffc107;
  color: #ffe599;
}

html.dark .warning-content strong {
  color: #ffe599;
}

/* Bottom-left floating gadget stack: history above, dice roller below. */
.floating-corner-left {
  position: fixed;
  left: 20px;
  bottom: 20px;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}
</style>
