<template>
  <div class="magic-tab">
    <!-- Spellbook Card -->
    <el-card class="spells-card">
      <template #header>
        <div class="card-header">
          <span>Spellbook</span>
          <span v-if="knownSpells.length > 0" class="spell-count">
            ({{ knownSpells.length }} spells known)
          </span>
        </div>
      </template>

      <div v-if="loading" style="text-align: center; padding: 40px;">
        <el-icon class="is-loading" :size="40">
          <Loading />
        </el-icon>
        <p>Loading spells...</p>
      </div>

      <template v-else>
        <!-- Spell Selection Dropdown -->
        <el-form-item label="Select Spells Known">
          <el-select
            v-model="character.magic.spells"
            multiple
            filterable
            :placeholder="(character.magic?.arcana?.length || 0) > 0 ? 'Browse and select spells you know' : 'Select arcana first to view spells'"
            :disabled="(character.magic?.arcana?.length || 0) === 0"
            style="width: 100%; margin-bottom: 16px;"
            class="multi-select-expanded"
          >
            <el-option
              v-for="spell in availableSpells"
              :key="spell.Name"
              :label="`${spell.Name} (${spell.Arcana}, ${spell.MP} MP)`"
              :value="spell.Name"
            >
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>{{ spell.Name }}</span>
                <div style="display: flex; gap: 4px;">
                  <el-tag size="small" type="warning">{{ spell.Arcana }}</el-tag>
                  <el-tag size="small" type="info">{{ spell.MP }} MP</el-tag>
                </div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <!-- Known Spells Table -->
        <div v-if="knownSpells.length === 0" class="empty-state-min-height" style="text-align: center; padding: 40px;">
          <el-empty description="No spells selected. Choose spells from the dropdown above." />
        </div>

        <el-table v-else :data="knownSpells" class="table-min-height" style="width: 100%" stripe border>
          <el-table-column prop="Name" label="Spell Name" min-width="200" />
          <el-table-column prop="Arcana" label="Arcana" min-width="150" />
          <el-table-column prop="MP" label="MP Cost" width="100" />
          <el-table-column label="SP" width="80">
            <template #default="scope">
              {{ spellPower(scope.row) }}
            </template>
          </el-table-column>
          <el-table-column prop="TN" label="TN" width="80" />
          <el-table-column prop="CastTime" label="Casting Time" min-width="150" />
          <el-table-column label="Actions" width="250" fixed="right">
            <template #default="scope">
              <el-button size="small" @click="openSpellDetails(scope.row)">
                View Details
              </el-button>
              <el-button size="small" type="primary" @click="castSpell(scope.row)">
                Cast
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-card>

    <!-- Arcana Selection Card -->
    <el-card class="arcana-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>Known Arcana</span>
        </div>
      </template>
      <el-form-item label="Select Arcana">
        <el-select
          v-model="character.magic.arcana"
          multiple
          filterable
          placeholder="Select arcana you know"
          style="width: 100%;"
          class="multi-select-expanded"
        >
          <el-option
            v-for="arcana in arcanaList"
            :key="arcana"
            :label="arcana"
            :value="arcana"
          />
        </el-select>
      </el-form-item>
    </el-card>

    <!-- Spell Detail Modal -->
    <SpellDetailModal
      v-model="showSpellModal"
      :spell="selectedSpell"
      :show-cast-button="false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, h } from 'vue'
import { storeToRefs } from 'pinia'
import { useCharacterStore } from '../stores/character'
import { useDataStore } from '../stores/data'
import { useRollHistoryStore, diceWithVariants } from '../stores/rollHistory'
import { ElMessage, ElNotification, ElTag } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import SpellDetailModal from '../components/SpellDetailModal.vue'
import { groupBy, degreeRank } from '../utils/grouping'

const characterStore = useCharacterStore()
const dataStore = useDataStore()
const rollHistoryStore = useRollHistoryStore()
const { character } = storeToRefs(characterStore)

const loading = ref(false)
const selectedSpell = ref(null)
const showSpellModal = ref(false)

// Computed properties
const arcanaList = computed(() => dataStore.arcana)
const allSpells = computed(() => dataStore.spells)

// Filter spells by selected arcana
const availableSpells = computed(() => {
  const selectedArcana = character.value?.magic?.arcana || []
  if (selectedArcana.length === 0) {
    return [] // No arcana selected = no spells available
  }
  return allSpells.value.filter(spell => selectedArcana.includes(spell.Arcana) && spell.Name !== 'Arcane Blast')
})

// Get all known spells (selected spells only), grouped by arcana with each
// arcana's spells ordered Novice -> Expert -> Master.
const knownSpells = computed(() => {
  const selectedSpellNames = character.value?.magic?.spells || []
  const rows = allSpells.value.filter(spell => selectedSpellNames.includes(spell.Name) && spell.Name !== 'Arcane Blast')
  // Arcana values look like "Air - Novice"; group by the base arcana ("Air").
  return groupBy(rows, spell => String(spell.Arcana).split(' - ')[0].trim(), spell => degreeRank(spell.Degree))
})

// Spellpower = 10 + Willpower + Arcana Focus bonus (if character has the spell's element focus)
const spellPower = (spell) => {
  const willpower = character.value?.stats?.Willpower || 0
  const focusBonus = characterStore.calculateFocusBonus('Arcana', spell.Element)
  return 10 + willpower + focusBonus
}

// Methods
const fetchArcana = async () => {
  try {
    loading.value = true
    await dataStore.fetchArcana()
  } catch (error) {
    console.error('Failed to fetch arcana:', error)
    ElMessage.error('Failed to load arcana list')
  } finally {
    loading.value = false
  }
}

const fetchSpells = async () => {
  try {
    loading.value = true
    await dataStore.fetchSpells()
  } catch (error) {
    console.error('Failed to fetch spells:', error)
    ElMessage.error('Failed to load spells')
  } finally {
    loading.value = false
  }
}

const openSpellDetails = (spell) => {
  selectedSpell.value = spell
  showSpellModal.value = true
}

// Cast spell - just roll, no MP deduction
const castSpell = async (spell) => {
  try {
    // Get Intelligence value
    const intelligenceValue = character.value.stats.Intelligence || 0

    // Get arcana focus name for this spell (Element field matches focus names, e.g. "Air Arcana")
    const arcanaFocusName = spell.Element
    const arcanaFoci = character.value.foci_primary.Arcana || []
    const hasFocus = arcanaFoci.includes(arcanaFocusName)
    const focusBonus = hasFocus ? characterStore.calculateFocusBonus('Arcana', arcanaFocusName) : 0

    // Roll 3d6
    const response = await characterStore.rollDice(0)
    const dice = response.dice
    const rollTotal = response.roll_total

    // Calculate final total
    const finalTotal = rollTotal + intelligenceValue + focusBonus

    // Check for stunt
    const hasStunt = response.has_stunt
    const stuntPoints = response.stunt_points

    // Display notification — stunt die (the non-matching 3rd die) shown red on a stunt
    const diceDisplay = h('div', { class: 'dice-display-inline' }, [
      ...dice.map((die, idx) => h(ElTag, {
        size: 'large',
        type: hasStunt && idx === 2 ? 'danger' : undefined,
        class: ['die-tag-inline', hasStunt && idx === 2 ? 'die-tag-stunt' : null]
      }, () => die))
    ])

    const targetNumber = parseInt(spell.TN) || 0
    const success = finalTotal >= targetNumber

    const lineTexts = [
      `Roll: ${dice.join(', ')} = ${rollTotal}`,
      `Intelligence: ${intelligenceValue >= 0 ? '+' : ''}${intelligenceValue}`
    ]
    if (hasFocus) lineTexts.push(`Focus (${arcanaFocusName}): +${focusBonus}`)
    lineTexts.push(`TN: ${spell.TN}`)
    lineTexts.push(`MP Cost: ${spell.MP}`)

    const lines = lineTexts.map(t => h('p', {}, t))
    lines.push(h('p', {
      class: 'final-result',
      style: success ? 'color: #67c23a; font-weight: bold' : 'color: #f56c6c; font-weight: bold'
    }, `Total: ${finalTotal} — ${success ? 'SUCCESS' : 'FAILURE'}`))
    if (hasStunt) lines.push(h('p', { class: 'stunt-notice' }, `✨ Stunt! SP: ${stuntPoints}`))

    const details = h('div', { class: 'roll-details' }, lines)

    rollHistoryStore.add({
      kind: 'spell',
      title: `Cast: ${spell.Name}`,
      dice: diceWithVariants(dice, { hasStunt }),
      lines: lineTexts,
      totalLabel: 'Total',
      totalValue: `${finalTotal} — ${success ? 'SUCCESS' : 'FAILURE'}`,
      totalClass: success ? 'success' : 'danger',
      stuntPoints: hasStunt ? stuntPoints : 0
    })

    ElNotification({
      title: `Cast: ${spell.Name}`,
      message: h('div', {}, [diceDisplay, details]),
      type: success ? 'success' : 'error',
      position: 'bottom-right',
      duration: 5000,
      customClass: 'dice-roll-notification'
    })
  } catch (error) {
    console.error('Cast spell error:', error)
    ElMessage.error('Failed to cast spell')
  }
}

// Watch arcana changes and auto-remove spells from deselected arcana
watch(
  () => character.value?.magic?.arcana,
  (newArcana) => {
    // Safety checks
    if (!character.value?.magic?.spells || !character.value?.magic?.arcana) {
      return
    }
    if (character.value.magic.spells.length === 0) {
      return
    }

    // Get currently selected arcana
    const selectedArcana = new Set(newArcana || [])

    // Filter out spells whose arcana is no longer selected
    const updatedSpells = character.value.magic.spells.filter(spellName => {
      const spell = allSpells.value.find(s => s.Name === spellName)
      return spell && selectedArcana.has(spell.Arcana)
    })

    // Update if any spells were removed
    if (updatedSpells.length !== character.value.magic.spells.length) {
      const removedCount = character.value.magic.spells.length - updatedSpells.length
      character.value.magic.spells = updatedSpells
      ElMessage.info(`${removedCount} spell(s) removed due to arcana deselection`)
    }
  },
  { deep: true }
)

// Lifecycle
onMounted(async () => {
  await fetchArcana()
  await fetchSpells()
})
</script>

<style scoped>
.magic-tab {
  padding: 0;
}

.card-header {
  font-weight: bold;
  font-size: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.spell-count {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
}

/* Multi-select expanded to show all tags */
.multi-select-expanded :deep(.el-select__wrapper) {
  min-height: 40px;
  height: auto !important;
}

.multi-select-expanded :deep(.el-tag) {
  max-width: none !important;
  margin: 2px 0;
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
</style>
