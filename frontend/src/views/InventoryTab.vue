<template>
  <div class="inventory-tab">
    <!-- Stunts and Currency Row -->
    <el-row :gutter="20" class="stunts-currency-row">
      <!-- Stunts Section (70% width) -->
      <el-col :span="17">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <el-icon><MagicStick /></el-icon>
              <span>Favourite and Class Stunts</span>
            </div>
          </template>

      <!-- Stunt Selection Dropdown -->
      <CategorizedSelect
        v-model="localExtras.stunts"
        :options="categorizedStunts"
        placeholder="Select stunts you know"
        style="margin-bottom: 16px;"
        @change="saveExtras"
      />

      <!-- Selected Stunts Table -->
      <el-table
        v-if="selectedStunts.length > 0"
        :data="selectedStunts"
        class="table-min-height"
        style="width: 100%"
        stripe
        border
      >
        <el-table-column label="Cost (SP)" width="100" align="center">
          <template #default="scope">
            <el-tag type="warning" size="small">{{ scope.row.Cost || scope.row['SP Cost'] }} SP</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="Name" label="Stunt Name" width="200" />
        <el-table-column label="Basic Effect" min-width="400">
          <template #default="scope">
            {{ scope.row.Effect || scope.row['Basic Effect'] }}
          </template>
        </el-table-column>
      </el-table>

      <el-empty
        v-else
        class="empty-state-min-height"
        description="No stunts selected. Choose stunts from the dropdown above."
      />
        </el-card>
      </el-col>

      <!-- Currency Section (30% width) -->
      <el-col :span="7">
        <el-card class="section-card">
      <template #header>
        <div class="card-header">
          <el-icon><Coin /></el-icon>
          <span>Currency</span>
        </div>
      </template>

      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8">
            <el-form-item label="Gold">
              <el-input-number
                v-model="localExtras.currency.gold"
                :min="0"
                :step="1"
                controls-position="right"
                style="width: 100%"
                @change="handleCurrencyChange"
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="8">
            <el-form-item label="Silver">
              <el-input-number
                v-model="localExtras.currency.silver"
                :min="0"
                :step="1"
                controls-position="right"
                style="width: 100%"
                @change="handleCurrencyChange"
              />
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="8">
            <el-form-item label="Copper">
              <el-input-number
                v-model="localExtras.currency.copper"
                :min="0"
                :step="1"
                controls-position="right"
                style="width: 100%"
                @change="handleCurrencyChange"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-button type="primary" @click="normalizeCurrency" :icon="Refresh">
              Normalize Currency
            </el-button>
          </el-col>
        </el-row>

        <el-row v-if="totalCopperValue > 0" style="margin-top: 12px;">
          <el-col :span="24">
            <el-text class="currency-total">
              Total Value: {{ totalCopperValue }} copper pieces
            </el-text>
          </el-col>
        </el-row>
      </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- Inventory Row (Full Width) -->
    <el-row :gutter="20" class="inventory-row">
      <el-col :span="24">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <el-icon><Box /></el-icon>
              <span>Equipment and Special Items</span>
            </div>
          </template>
          <InventoryTable v-model="localExtras.inventory" @update:modelValue="saveExtras" />
        </el-card>
      </el-col>
    </el-row>

    <!-- Personal and Relationships Row (50/50 split) -->
    <el-row :gutter="20" class="personal-relationships-row">
      <!-- Personal Details and History Section -->
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>Personal Details and History</span>
            </div>
          </template>
          <el-form-item label="">
            <el-input
              v-model="localExtras.backstory"
              type="textarea"
              :rows="12"
              :class="{ 'text-limit-reached': (localExtras.backstory?.length || 0) >= 50000 }"
              placeholder="Write your character's backstory here..."
              @change="saveExtras"
              maxlength="50000"
            />
          </el-form-item>
        </el-card>
      </el-col>

      <!-- Relationships Section -->
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>Relationships</span>
            </div>
          </template>
          <el-form-item label="">
            <el-input
              v-model="localExtras.relationships"
              type="textarea"
              :rows="12"
              :class="{ 'text-limit-reached': (localExtras.relationships?.length || 0) >= 50000 }"
              placeholder="Describe your character's relationships with other people and organizations..."
              @change="saveExtras"
              maxlength="50000"
            />
          </el-form-item>
        </el-card>
      </el-col>
    </el-row>

    <!-- Goals and Notes Row (50/50 split) -->
    <el-row :gutter="20" class="goals-notes-row">
      <!-- Goals and Ties Section -->
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>Goals and Ties</span>
            </div>
          </template>
          <el-form-item label="">
            <el-input
              v-model="localExtras.goals_ties"
              type="textarea"
              :rows="8"
              :class="{ 'text-limit-reached': (localExtras.goals_ties?.length || 0) >= 50000 }"
              placeholder="What are your character's goals, motivations, and connections..."
              @change="saveExtras"
              maxlength="50000"
            />
          </el-form-item>
        </el-card>
      </el-col>

      <!-- Extra Notes Section -->
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>Extra Notes</span>
            </div>
          </template>
          <el-form-item label="">
            <el-input
              v-model="localExtras.extra_notes"
              type="textarea"
              :rows="8"
              :class="{ 'text-limit-reached': (localExtras.extra_notes?.length || 0) >= 50000 }"
              placeholder="Any other notes about your character..."
              @change="saveExtras"
              maxlength="50000"
            />
          </el-form-item>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCharacterStore } from '../stores/character'
import { ElMessage } from 'element-plus'
import { Box, Coin, MagicStick, Document, Refresh } from '@element-plus/icons-vue'
import InventoryTable from '../components/InventoryTable.vue'
import CategorizedSelect from '../components/CategorizedSelect.vue'
import { groupBy } from '../utils/grouping'
import axios from 'axios'

const characterStore = useCharacterStore()

// Local extras data
const localExtras = ref({
  inventory: [],
  currency: {
    gold: 0,
    silver: 0,
    copper: 0
  },
  stunts: [],
  backstory: '',
  relationships: '',
  goals_ties: '',
  extra_notes: ''
})

// Available stunts from backend
const availableStunts = ref([])

// Transform stunts to categorized format for the dropdown
const categorizedStunts = computed(() => {
  return availableStunts.value.map(stunt => ({
    value: stunt.Name,
    name: stunt.Name,
    label: `${stunt.Name} (${stunt.Cost || stunt['SP Cost']} SP)`,
    category: stunt.Type || 'Other',
    cost: `${stunt.Cost || stunt['SP Cost']} SP`
  }))
})

// Selected stunts with full details, grouped by type (Combat / Social / Magic ...)
const selectedStunts = computed(() => {
  const rows = availableStunts.value.filter(stunt =>
    localExtras.value.stunts.includes(stunt.Name)
  )
  return groupBy(rows, stunt => stunt.Type || 'Other')
})

// Total currency value in copper
const totalCopperValue = ref(0)

// Load character extras on mount
onMounted(async () => {
  // Load stunts from backend
  await loadStunts()

  // Initialize from character store
  if (characterStore.character.extras) {
    localExtras.value = {
      inventory: characterStore.character.extras.inventory || [],
      currency: {
        gold: characterStore.character.extras.currency?.gold || 0,
        silver: characterStore.character.extras.currency?.silver || 0,
        copper: characterStore.character.extras.currency?.copper || 0
      },
      stunts: characterStore.character.extras.stunts || [],
      backstory: characterStore.character.extras.backstory || '',
      relationships: characterStore.character.extras.relationships || '',
      goals_ties: characterStore.character.extras.goals_ties || '',
      extra_notes: characterStore.character.extras.extra_notes || ''
    }
  }

  calculateTotalValue()
})

// Watch for character changes
watch(
  () => characterStore.character.extras,
  (newExtras) => {
    if (newExtras) {
      localExtras.value = {
        inventory: newExtras.inventory || [],
        currency: {
          gold: newExtras.currency?.gold || 0,
          silver: newExtras.currency?.silver || 0,
          copper: newExtras.currency?.copper || 0
        },
        stunts: newExtras.stunts || [],
        backstory: newExtras.backstory || '',
        relationships: newExtras.relationships || '',
        goals_ties: newExtras.goals_ties || '',
        extra_notes: newExtras.extra_notes || ''
      }
      calculateTotalValue()
    }
  },
  { deep: true }
)

// Load stunts from backend
async function loadStunts() {
  try {
    const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
    const response = await axios.get(`${API_BASE}/api/data/stunts`)
    availableStunts.value = response.data
  } catch (error) {
    console.error('Error loading stunts:', error)
    ElMessage.error('Failed to load stunts')
  }
}

// Handle currency change
function handleCurrencyChange() {
  calculateTotalValue()
  saveExtras()
}

// Calculate total currency value in copper
function calculateTotalValue() {
  totalCopperValue.value =
    localExtras.value.currency.copper +
    localExtras.value.currency.silver * 10 +
    localExtras.value.currency.gold * 100
}

// Normalize currency (convert to highest denominations)
function normalizeCurrency() {
  const total =
    localExtras.value.currency.copper +
    localExtras.value.currency.silver * 10 +
    localExtras.value.currency.gold * 100

  localExtras.value.currency = {
    gold: Math.floor(total / 100),
    silver: Math.floor((total % 100) / 10),
    copper: total % 10
  }

  totalCopperValue.value = total
  saveExtras()
  ElMessage.success('Currency normalized')
}

// Save extras to character store
function saveExtras() {
  characterStore.updateExtras(localExtras.value)
}
</script>

<style scoped>
.inventory-tab {
  padding: 0;
}

.section-card {
  margin-bottom: 16px;
}

.stunts-currency-row {
  margin-bottom: 16px;
}

.stunts-currency-row .section-card {
  height: 100%;
  margin-bottom: 0;
}

.inventory-row {
  margin-bottom: 16px;
}

.personal-relationships-row {
  margin-bottom: 16px;
}

.personal-relationships-row .section-card {
  height: 100%;
  margin-bottom: 0;
}

.goals-notes-row {
  margin-bottom: 16px;
}

.goals-notes-row .section-card {
  height: 100%;
  margin-bottom: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 16px;
}

.currency-total {
  margin-left: 20px;
  color: var(--el-text-color-secondary);
}

/* Multi-select expanded to show all tags */
.multi-select-expanded :deep(.el-select__wrapper) {
  min-height: 40px;
  height: auto !important;
  padding: 4px 8px;
}

.multi-select-expanded :deep(.el-select__selection) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  width: 100%;
}

.multi-select-expanded :deep(.el-tag) {
  max-width: none !important;
  margin: 2px 0;
}

/* Remove number input spinner buttons */
:deep(input[type="number"]) {
  -moz-appearance: textfield;
}

:deep(input[type="number"]::-webkit-outer-spin-button),
:deep(input[type="number"]::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  margin: 0;
}

/* Empty state minimum height */
.empty-state-min-height {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Table minimum height */
.table-min-height {
  min-height: 300px;
}

/* Text limit reached warning */
.text-limit-reached :deep(.el-textarea__inner) {
  border-color: #f56c6c !important;
  box-shadow: 0 0 0 1px #f56c6c inset !important;
}

.text-limit-reached :deep(.el-textarea__inner:focus) {
  border-color: #f56c6c !important;
  box-shadow: 0 0 0 1px #f56c6c inset !important;
}
</style>
