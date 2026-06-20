<template>
  <div class="levelup-tab">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-icon><TrendCharts /></el-icon>
          <span v-if="characterStore.character.char_class">
            Level-Up Progression [{{ characterStore.character.char_class }} Level {{ characterStore.character.level }}]
          </span>
          <span v-else>Level-Up Progression</span>
        </div>
      </template>

      <!-- Class Selection Info -->
      <el-alert
        v-if="!characterStore.character.char_class"
        title="No Class Selected"
        type="warning"
        description="Please select a character class in the Main tab to view progression table."
        :closable="false"
        show-icon
      />

      <div v-else class="progression-container">
        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <el-icon class="is-loading" :size="50">
            <Loading />
          </el-icon>
          <p>Loading progression table...</p>
        </div>

        <!-- Error State -->
        <el-alert
          v-else-if="error"
          title="Error Loading Progression Table"
          type="error"
          :description="error"
          show-icon
        />

        <!-- Progression Table (Full Display) -->
        <div v-else-if="progressionData.length > 0">
          <!-- Next Level Preview -->
          <el-card
            v-if="nextLevelData"
            class="next-level-card"
            shadow="hover"
          >
            <template #header>
              <div class="next-level-header">
                <el-icon><Promotion /></el-icon>
                <span>Next Level ({{ nextLevelData.Level }})</span>
              </div>
            </template>

            <div class="next-level-content">
              <span v-if="nextLevelData.Specializations && nextLevelData.Specializations !== '-'">
                <strong>Specializations:</strong> <span v-html="nextLevelData.Specializations"></span>
              </span>
              <span v-if="nextLevelData.Talents && nextLevelData.Talents !== '-'">
                <strong>Talents:</strong> <span v-html="nextLevelData.Talents"></span>
              </span>
              <span v-if="nextLevelData.Features && nextLevelData.Features !== '-'">
                <strong>Features:</strong> <span v-html="nextLevelData.Features"></span>
              </span>
              <span v-if="nextLevelData.Ability && nextLevelData.Ability !== '-'">
                <strong>Ability:</strong> <span v-html="nextLevelData.Ability"></span>
              </span>
              <span v-if="nextLevelData.Focus && nextLevelData.Focus !== '-'">
                <strong>Focus:</strong> <span v-html="nextLevelData.Focus"></span>
              </span>
              <span v-if="nextLevelData.Stunt && nextLevelData.Stunt !== 'No'">
                <strong>Stunt:</strong> <span v-html="nextLevelData.Stunt"></span>
              </span>
            </div>
          </el-card>

          <el-table
            :data="progressionData"
            style="width: 100%"
            :row-class-name="tableRowClassName"
            border
            stripe
          >
            <!-- Level Column -->
            <el-table-column
              prop="Level"
              label="Level"
              width="80"
              align="center"
              fixed
            >
              <template #default="scope">
                <el-tag
                  v-if="scope.row.Level === characterStore.character.level"
                  type="success"
                  effect="dark"
                >
                  {{ scope.row.Level }}
                </el-tag>
                <span v-else>{{ scope.row.Level }}</span>
              </template>
            </el-table-column>

            <!-- Specializations Column -->
            <el-table-column
              prop="Specializations"
              label="Specializations"
              width="150"
              align="center"
            >
              <template #default="scope">
                <span v-if="scope.row.Specializations" v-html="scope.row.Specializations"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>

            <!-- Talents Column -->
            <el-table-column
              prop="Talents"
              label="Talents"
              width="250"
              align="center"
            >
              <template #default="scope">
                <span v-if="scope.row.Talents !== null && scope.row.Talents !== undefined && scope.row.Talents !== ''" v-html="scope.row.Talents"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>

            <!-- Features Column (Class-specific features) -->
            <el-table-column
              prop="Features"
              label="Features"
              min-width="200"
            >
              <template #default="scope">
                <span v-if="scope.row.Features" v-html="scope.row.Features"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>

            <!-- Ability Column -->
            <el-table-column
              prop="Ability"
              label="Ability"
              width="120"
              align="center"
            >
              <template #default="scope">
                <span v-if="scope.row.Ability !== null && scope.row.Ability !== undefined && scope.row.Ability !== '' && scope.row.Ability !== '-'" v-html="scope.row.Ability"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>

            <!-- Focus Column -->
            <el-table-column
              prop="Focus"
              label="Focus"
              width="120"
              align="center"
            >
              <template #default="scope">
                <span v-if="scope.row.Focus !== null && scope.row.Focus !== undefined && scope.row.Focus !== '' && scope.row.Focus !== '-'" v-html="scope.row.Focus"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>

            <!-- Stunt Column -->
            <el-table-column
              prop="Stunt"
              label="Stunt"
              width="100"
              align="center"
            >
              <template #default="scope">
                <span v-if="scope.row.Stunt !== null && scope.row.Stunt !== undefined && scope.row.Stunt !== '' && scope.row.Stunt !== 'No'" v-html="scope.row.Stunt"></span>
                <span v-else class="empty-cell">—</span>
              </template>
            </el-table-column>
          </el-table>

          <!-- Advancement Guide -->
          <el-card class="guide-card" shadow="never">
            <template #header>
              <div class="guide-header">
                <el-icon><QuestionFilled /></el-icon>
                <span>Advancement Guide</span>
              </div>
            </template>

            <el-descriptions :column="2" border>
              <el-descriptions-item label="Health">
                Gain 1d6 + Constitution from levels 2-10, then just Constitution from 11-20
              </el-descriptions-item>
              <el-descriptions-item label="Specialization">
                Choose a specialization from those available to you
              </el-descriptions-item>
              <el-descriptions-item label="Talent">
                Choose a talent from those available to you
              </el-descriptions-item>
              <el-descriptions-item label="Features">
                Class-specific features gained at this level
              </el-descriptions-item>
              <el-descriptions-item label="Ability">
                Increase an ability score by 1. To increase past 5, this costs two advancements. The level determines if this is a primary or secondary ability
              </el-descriptions-item>
              <el-descriptions-item label="Focus">
                Choose a focus from either a primary or secondary ability, as indicated
              </el-descriptions-item>
              <el-descriptions-item label="Stunt">
                Learn a new class stunt, or improve a basic stunt
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>

        <!-- Empty State -->
        <el-empty
          v-else
          description="No progression data available"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useCharacterStore } from '../stores/character'
import { ElMessage } from 'element-plus'
import {
  TrendCharts,
  Loading,
  QuestionFilled,
  Promotion
} from '@element-plus/icons-vue'
import axios from 'axios'

const characterStore = useCharacterStore()

// State
const progressionData = ref([])
const loading = ref(false)
const error = ref(null)

// Next level data
const nextLevelData = computed(() => {
  const currentLevel = characterStore.character.level
  const nextLevel = progressionData.value.find(
    row => row.Level === currentLevel + 1
  )
  return nextLevel || null
})

// Load progression data on mount
onMounted(() => {
  loadProgressionTable()
})

// Watch for class changes
watch(
  () => characterStore.character.char_class,
  () => {
    loadProgressionTable()
  }
)

// Load progression table from backend
async function loadProgressionTable() {
  const charClass = characterStore.character.char_class

  if (!charClass) {
    progressionData.value = []
    return
  }

  loading.value = true
  error.value = null

  try {
    const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    const response = await axios.get(
      `${API_BASE}/api/data/levelup/${charClass}`
    )
    progressionData.value = response.data
  } catch (err) {
    console.error('Error loading progression table:', err)
    error.value = err.response?.data?.detail || 'Failed to load progression table'
    ElMessage.error('Failed to load level-up progression table')
  } finally {
    loading.value = false
  }
}

// Highlight current level row
function tableRowClassName({ row }) {
  if (row.Level === characterStore.character.level) {
    return 'current-level-row'
  }
  if (row.Level < characterStore.character.level) {
    return 'past-level-row'
  }
  return ''
}
</script>

<style scoped>
.levelup-tab {
  padding: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 16px;
}

.progression-container {
  margin-top: 16px;
}

.current-level {
  margin-bottom: 16px;
  padding: 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  text-align: center;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
}

.empty-cell {
  color: var(--el-text-color-placeholder);
  font-style: italic;
}

.guide-card {
  margin-top: 24px;
}

.guide-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.next-level-card {
  margin-bottom: 24px;
  border: 2px solid var(--el-color-primary);
}

.next-level-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--el-color-primary);
}

.next-level-content {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 0;
  align-items: center;
}

.next-level-content span {
  padding: 0 16px;
  border-right: 2px solid var(--el-border-color);
}

.next-level-content span:last-child {
  border-right: none;
}

:deep(.current-level-row) {
  background-color: var(--el-color-success-light-9);
  font-weight: 600;
}

:deep(.past-level-row) {
  opacity: 0.6;
}

:deep(.el-table) {
  font-size: 14px;
}
</style>
