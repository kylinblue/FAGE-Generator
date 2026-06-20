<template>
  <div class="main-tab">
    <!-- Character Profile Section -->
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>Character Profile</span>
        </div>
      </template>

      <el-row :gutter="20">
        <!-- Profile Fields Column -->
        <el-col :span="18">
          <el-form label-position="top">
            <el-row :gutter="20">
              <el-col :span="24">
                <el-form-item label="Name">
                  <el-input
                    v-model="character.name"
                    placeholder="Enter character name"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Ancestry">
                  <el-input
                    v-model="character.ancestry"
                    placeholder="Enter ancestry"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Social Class">
                  <el-input
                    v-model="character.social_class"
                    placeholder="Outsider"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="24">
                <el-form-item label="Background">
                  <el-select
                    v-model="character.background"
                    placeholder="Criminal"
                    filterable
                    style="width: 100%"
                  >
                    <el-option
                      v-for="bg in backgrounds"
                      :key="bg"
                      :label="bg"
                      :value="bg"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="19">
                <el-form-item label="Class">
                  <el-select v-model="character.char_class" placeholder="Warrior" style="width: 100%">
                    <el-option label="Envoy" value="Envoy" />
                    <el-option label="Mage" value="Mage" />
                    <el-option label="Rogue" value="Rogue" />
                    <el-option label="Warrior" value="Warrior" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="5">
                <el-form-item label="Level">
                  <el-input-number
                    v-model="character.level"
                    :min="1"
                    :max="20"
                    :step="1"
                    controls-position="right"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="Speed">
                  <el-input-number
                    v-model="character.speed"
                    :min="0"
                    :step="1"
                    controls-position="right"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Defence">
                  <el-input-number
                    v-model="character.defense"
                    :min="0"
                    :step="1"
                    controls-position="right"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="Experience">
                  <el-input-number
                    v-model="character.experience"
                    :min="0"
                    :step="1"
                    controls-position="right"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-col>

        <!-- Photo Column -->
        <el-col :span="6">
          <PhotoUpload v-model="character.photo" />
        </el-col>
      </el-row>
    </el-card>

    <!-- Talents Selection -->
    <el-card class="talents-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>Talents</span>
          <el-tag type="warning" size="small">
            Filtered by class: {{ character.char_class }}
          </el-tag>
        </div>
      </template>

      <!-- Talent Selection Dropdown -->
      <el-select
        v-model="character.talents"
        placeholder="Select talents"
        multiple
        filterable
        style="width: 100%; margin-bottom: 16px;"
        class="multi-select-expanded"
      >
        <el-option
          v-for="talent in talents"
          :key="`${talent.Name}-${talent.DegreeLong || talent.Degree}`"
          :label="`${talent.Name} (${talent.DegreeLong || talent.Degree})`"
          :value="`${talent.Name}|${talent.DegreeLong || talent.Degree}`"
        />
      </el-select>

      <!-- Selected Talents Table -->
      <el-table
        v-if="selectedTalents.length > 0"
        :data="selectedTalents"
        class="table-min-height"
        style="width: 100%"
        stripe
        border
      >
        <el-table-column prop="Name" label="Name" width="200" />
        <el-table-column label="Degree" width="120">
          <template #default="scope">
            <el-tag
              :type="(scope.row.DegreeLong || scope.row.Degree) === 'Novice' || scope.row.Degree === 1 ? 'primary' :
                     (scope.row.DegreeLong || scope.row.Degree) === 'Expert' || scope.row.Degree === 2 ? 'warning' : 'danger'"
              size="small"
            >
              {{ scope.row.DegreeLong || scope.row.Degree }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Requirements" width="200">
          <template #default="scope">
            <span v-html="scope.row.Requirements"></span>
          </template>
        </el-table-column>
        <el-table-column label="Effect" min-width="300">
          <template #default="scope">
            <span v-html="scope.row.Effect"></span>
          </template>
        </el-table-column>
      </el-table>

      <el-empty
        v-else
        class="empty-state-min-height"
        description="No talents selected. Choose talents from the dropdown above."
      />
    </el-card>

    <!-- Specializations Selection -->
    <el-card class="specializations-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>Specializations</span>
          <el-tag type="warning" size="small">
            Filtered by class: {{ character.char_class }}
          </el-tag>
        </div>
      </template>

      <!-- Specialization Selection Dropdown -->
      <el-select
        v-model="character.specializations"
        placeholder="Select specializations"
        multiple
        filterable
        style="width: 100%; margin-bottom: 16px;"
        class="multi-select-expanded"
      >
        <el-option
          v-for="spec in specializations"
          :key="`${spec.Name || spec.Specialization}-${spec.DegreeLong || spec.Degree}`"
          :label="`${spec.Name || spec.Specialization} (${spec.DegreeLong || spec.Degree || 'Novice'})`"
          :value="`${spec.Name || spec.Specialization}|${spec.DegreeLong || spec.Degree || 'Novice'}`"
        />
      </el-select>

      <!-- Selected Specializations Table -->
      <el-table
        v-if="selectedSpecializations.length > 0"
        :data="selectedSpecializations"
        class="table-min-height"
        style="width: 100%"
        stripe
        border
      >
        <el-table-column prop="Name" label="Name" width="200" />
        <el-table-column label="Degree" width="120">
          <template #default="scope">
            <el-tag
              :type="(scope.row.DegreeLong || scope.row.Degree) === 'Novice' || scope.row.Degree === 1 ? 'primary' :
                     (scope.row.DegreeLong || scope.row.Degree) === 'Expert' || scope.row.Degree === 2 ? 'warning' : 'danger'"
              size="small"
            >
              {{ scope.row.DegreeLong || scope.row.Degree }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Requirements" width="200">
          <template #default="scope">
            <span v-html="scope.row.Requirements"></span>
          </template>
        </el-table-column>
        <el-table-column label="Effect" min-width="300">
          <template #default="scope">
            <span v-html="scope.row.Effect || scope.row.Description"></span>
          </template>
        </el-table-column>
      </el-table>

      <el-empty
        v-else
        class="empty-state-min-height"
        description="No specializations selected. Choose specializations from the dropdown above."
      />
    </el-card>

    <!-- Special Features (player-authored, edited directly in Special_Features.csv) -->
    <el-card class="special-features-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>Special Features</span>
          <div style="display: flex; gap: 8px; align-items: center;">
            <el-tag type="info" size="small">
              Edit backend/data/csv/Special_Features.csv
            </el-tag>
            <el-button size="small" @click="reloadSpecialFeatures">Reload</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-if="specialFeatures.length > 0"
        :data="specialFeatures"
        class="table-min-height"
        style="width: 100%"
        stripe
        border
      >
        <el-table-column prop="Source" label="Source" width="220" />
        <el-table-column prop="Name" label="Name" width="220" />
        <el-table-column prop="Effect" label="Effect" min-width="300" />
      </el-table>

      <el-empty
        v-else
        class="empty-state-min-height"
        description="No special features. Add rows to backend/data/csv/Special_Features.csv (Source,Name,Effect) and click Reload."
      />
    </el-card>

    <!-- Equipment Section -->
    <el-card class="equipment-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>Equipment</span>
        </div>
      </template>

      <!-- Melee Weapons -->
      <el-divider>Melee Weapons</el-divider>
      <div class="weapon-section">
        <el-select
          v-model="character.equipment.melee_weapons"
          placeholder="Select melee weapons"
          multiple
          filterable
          style="width: 100%; margin-bottom: 16px;"
        >
          <el-option
            v-for="weapon in meleeWeapons"
            :key="weapon.Weapon"
            :label="weapon.Weapon"
            :value="weapon.Weapon"
          />
        </el-select>

        <!-- Display Selected Weapons -->
        <el-table
          v-if="selectedMeleeWeapons.length > 0"
          :data="selectedMeleeWeapons"
          style="width: 100%"
          stripe
          border
        >
          <el-table-column label="Weapon" min-width="180">
            <template #default="scope">
              {{ scope.row.Weapon }}
            </template>
          </el-table-column>
          <el-table-column label="Group" min-width="140">
            <template #default="scope">
              {{ scope.row.Group }}
            </template>
          </el-table-column>
          <el-table-column label="Damage" min-width="120">
            <template #default="scope">
              {{ scope.row.Damage }}
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="200">
            <template #default="scope">
              <el-button size="small" @click="rollWeaponAttack(scope.row, 'melee')">
                Attack
              </el-button>
              <el-button size="small" type="primary" @click="rollWeaponDamage(scope.row, 'melee')">
                Damage
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Ranged Weapons -->
      <el-divider>Ranged Weapons</el-divider>
      <div class="weapon-section">
        <el-select
          v-model="character.equipment.ranged_weapons"
          placeholder="Select ranged weapons"
          multiple
          filterable
          style="width: 100%; margin-bottom: 16px;"
        >
          <el-option
            v-for="weapon in rangedWeapons"
            :key="weapon.Weapon"
            :label="weapon.Weapon"
            :value="weapon.Weapon"
          />
        </el-select>

        <!-- Display Selected Weapons -->
        <el-table
          v-if="selectedRangedWeapons.length > 0"
          :data="selectedRangedWeapons"
          style="width: 100%"
          stripe
          border
        >
          <el-table-column label="Weapon" min-width="180">
            <template #default="scope">
              {{ scope.row.Weapon }}
            </template>
          </el-table-column>
          <el-table-column label="Group" min-width="140">
            <template #default="scope">
              {{ scope.row.Group }}
            </template>
          </el-table-column>
          <el-table-column label="Damage" width="120">
            <template #default="scope">
              {{ scope.row.Damage }}
            </template>
          </el-table-column>
          <el-table-column label="Short Range" width="120">
            <template #default="scope">
              {{ scope.row['Short Range'] }}
            </template>
          </el-table-column>
          <el-table-column label="Long Range" width="120">
            <template #default="scope">
              {{ scope.row['Long Range'] }}
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="200">
            <template #default="scope">
              <el-button size="small" @click="rollWeaponAttack(scope.row, 'ranged')">
                Attack
              </el-button>
              <el-button size="small" type="primary" @click="rollWeaponDamage(scope.row, 'ranged')">
                Damage
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Weapon Groups -->
      <el-divider>Weapon Groups</el-divider>
      <el-select
        v-model="character.extras.weapon_groups"
        placeholder="Select weapon groups"
        multiple
        filterable
        style="width: 100%; margin-bottom: 16px;"
      >
          <el-option label="Axes" value="Axes" />
          <el-option label="Black Powder" value="Black Powder" />
          <el-option label="Bludgeons" value="Bludgeons" />
          <el-option label="Bows" value="Bows" />
          <el-option label="Brawling" value="Brawling" />
          <el-option label="Dueling" value="Dueling" />
          <el-option label="Heavy Blades" value="Heavy Blades" />
          <el-option label="Lances" value="Lances" />
          <el-option label="Light Blades" value="Light Blades" />
          <el-option label="Polearms" value="Polearms" />
          <el-option label="Slings" value="Slings" />
          <el-option label="Spears" value="Spears" />
          <el-option label="Staves" value="Staves" />
        </el-select>
    </el-card>

    <!-- Actions -->
    <el-card class="actions-card" style="margin-top: 20px;">
      <el-space wrap>
        <el-button @click="resetCharacter" type="danger">
          New Character
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, h } from 'vue'
import { ElMessage, ElMessageBox, ElNotification, ElTag } from 'element-plus'
import { useCharacterStore } from '../stores/character'
import { useDataStore } from '../stores/data'
import { useUIStore } from '../stores/ui'
import ArmorSelect from '../components/ArmorSelect.vue'
import PhotoUpload from '../components/PhotoUpload.vue'
import { resolveDamageExtras } from '../utils/calculations'
import { groupBy, degreeRank } from '../utils/grouping'
import { useRollHistoryStore, diceWithVariants } from '../stores/rollHistory'

const characterStore = useCharacterStore()
const dataStore = useDataStore()
const uiStore = useUIStore()
const rollHistoryStore = useRollHistoryStore()

// Last attack roll per weapon — keyed by weapon name. Used by damage rolls
// to apply level-16 stunt-die-to-damage extras for matching classes.
const lastAttackRoll = ref({})

const character = computed(() => characterStore.character)
const backgrounds = computed(() => dataStore.backgrounds)
const armorList = computed(() => dataStore.armor)
const meleeWeapons = computed(() => dataStore.meleeWeapons)
const rangedWeapons = computed(() => dataStore.rangedWeapons)
const talents = computed(() => dataStore.talents)
const specializations = computed(() => dataStore.specializations)
const specialFeatures = computed(() => dataStore.specialFeatures)

// Selected talents (full objects based on stored strings).
// Grouped by title with degrees ordered Novice -> Expert -> Master.
const selectedTalents = computed(() => {
  if (!character.value.talents || character.value.talents.length === 0) return []
  const rows = character.value.talents
    .map(talentStr => {
      const [name, degree] = talentStr.split('|')
      return talents.value.find(t =>
        t.Name === name && (t.DegreeLong === degree || String(t.Degree) === degree)
      )
    })
    .filter(Boolean)
  return groupBy(rows, t => t.Name, t => degreeRank(t.DegreeLong || t.Degree))
})

// Selected specializations (full objects based on stored strings).
// Grouped by title with degrees ordered Novice -> Expert -> Master.
const selectedSpecializations = computed(() => {
  if (!character.value.specializations || character.value.specializations.length === 0) return []
  const rows = character.value.specializations
    .map(specStr => {
      const [name, degree] = specStr.split('|')
      return specializations.value.find(s =>
        (s.Name === name || s.Specialization === name) &&
        (s.DegreeLong === degree || String(s.Degree) === degree || (!s.Degree && degree === 'Novice'))
      )
    })
    .filter(Boolean)
  return groupBy(rows, s => s.Name || s.Specialization, s => degreeRank(s.DegreeLong || s.Degree))
})

// Get selected weapons as full objects
const selectedMeleeWeapons = computed(() => {
  if (!character.value.equipment.melee_weapons) return []
  return meleeWeapons.value.filter(w =>
    character.value.equipment.melee_weapons.includes(w.Weapon)
  )
})

const selectedRangedWeapons = computed(() => {
  if (!character.value.equipment.ranged_weapons) return []
  return rangedWeapons.value.filter(w =>
    character.value.equipment.ranged_weapons.includes(w.Weapon)
  )
})

onMounted(async () => {
  await dataStore.fetchBackgrounds()
  await dataStore.fetchArmor()
  await dataStore.fetchMeleeWeapons()
  await dataStore.fetchRangedWeapons()
  await dataStore.fetchTalents(character.value.char_class)
  await dataStore.fetchSpecializations(character.value.char_class)
  await dataStore.fetchSpecialFeatures()
})

async function reloadSpecialFeatures() {
  try {
    await dataStore.fetchSpecialFeatures()
    ElMessage.success('Special Features reloaded')
  } catch (e) {
    ElMessage.error('Failed to reload Special Features')
  }
}

// Watch for class changes and refetch talents/specializations
watch(() => character.value.char_class, async (newClass) => {
  if (newClass) {
    await dataStore.fetchTalents(newClass)
    await dataStore.fetchSpecializations(newClass)
  }
})

// Watch for Dexterity changes and recalculate defense
watch(() => character.value.stats.Dexterity, (newDexterity) => {
  // Recalculate defense when Dexterity changes
  const armorRating = character.value.equipment.armor
    ? (armorList.value.find(a => a.Name === character.value.equipment.armor)?.Rating || 0)
    : 0
  character.value.defense = 10 + newDexterity + armorRating
})

// Roll weapon attack (3d6 + Skill + Group Focus + BonusHit)
async function rollWeaponAttack(weapon, weaponType) {
  try {
    // Determine skill based on weapon
    const skill = weaponType === 'ranged' ? 'Accuracy' : weapon.Skill || 'Fighting'
    const skillValue = character.value.stats[skill] || 0

    // Get group focus bonus (check if character has focus in weapon group)
    const weaponGroup = weapon.Group
    const groupFoci = character.value.foci_primary[skill] || []
    const hasFocus = groupFoci.includes(weaponGroup)
    const focusBonus = hasFocus ? characterStore.calculateFocusBonus(skill, weaponGroup) : 0

    // BonusHit (from weapon, default to 0 if not specified)
    const bonusHit = parseInt(weapon.BonusHit) || 0

    // Roll 3d6
    const response = characterStore.rollCheck(skillValue + focusBonus + bonusHit)
    const dice = response.dice
    const rollTotal = response.roll_total

    // Final total from roll_check (already includes modifier)
    const finalTotal = response.final_total

    // Check for stunt
    const hasStunt = response.has_stunt
    const stuntPoints = response.stunt_points

    // Stash for the next damage roll on this weapon
    lastAttackRoll.value[weapon.Weapon] = response

    // Display notification — stunt die (the non-matching 3rd die) shown red on a stunt
    const diceDisplay = h('div', { class: 'dice-display-inline' }, [
      ...dice.map((die, idx) => h(ElTag, {
        size: 'large',
        type: hasStunt && idx === 2 ? 'danger' : undefined,
        class: ['die-tag-inline', hasStunt && idx === 2 ? 'die-tag-stunt' : null]
      }, () => die))
    ])

    const lineTexts = [
      `Roll: ${dice.join(', ')} = ${rollTotal}`,
      `${skill}: ${skillValue >= 0 ? '+' : ''}${skillValue}`
    ]
    if (hasFocus) lineTexts.push(`Focus (${weaponGroup}): +${focusBonus}`)
    if (bonusHit > 0) lineTexts.push(`Weapon: +${bonusHit}`)

    const lines = lineTexts.map(t => h('p', {}, t))
    lines.push(h('p', { class: 'final-result' }, `Total: ${finalTotal}`))
    if (hasStunt) lines.push(h('p', { class: 'stunt-notice' }, `✨ Stunt! SP: ${stuntPoints}`))

    const details = h('div', { class: 'roll-details' }, lines)

    rollHistoryStore.add({
      kind: 'attack',
      title: `${weapon.Weapon} Attack`,
      dice: diceWithVariants(dice, { hasStunt }),
      lines: lineTexts,
      totalLabel: 'Total',
      totalValue: finalTotal,
      stuntPoints: hasStunt ? stuntPoints : 0
    })

    ElNotification({
      title: `${weapon.Weapon} Attack`,
      message: h('div', {}, [diceDisplay, details]),
      type: hasStunt ? 'success' : 'info',
      position: 'bottom-right',
      duration: 5000,
      customClass: 'dice-roll-notification'
    })
  } catch (error) {
    console.error('Attack roll error:', error)
    ElMessage.error('Failed to roll attack')
  }
}

// Roll weapon damage
async function rollWeaponDamage(weapon, weaponType) {
  try {
    const numDice = parseInt(weapon.Dice) || 1
    const mod = parseInt(weapon.Mod) || 0
    const bonusDamage = parseInt(weapon.BonusDamage) || 0

    // Stat added to damage (DamageStat overrides default)
    const skill = weaponType === 'ranged' ? 'Accuracy' : weapon.Skill || 'Fighting'
    const defaultStat = skill === 'Accuracy' ? 'Perception' : 'Strength'
    const statToAdd = weapon.DamageStat || defaultStat
    const statModifier = character.value.stats[statToAdd] || 0

    // Focus bonus at level 6+
    let focusBonus = 0
    if (character.value.level >= 6) {
      const weaponGroup = weapon.Group
      const groupFoci = character.value.foci_primary[skill] || []
      if (groupFoci.includes(weaponGroup)) {
        focusBonus = characterStore.calculateFocusBonus(skill, weaponGroup)
      }
    }

    // Class-based extras (Pinpoint d6, stunt-die-to-damage at level 16+, etc.)
    const attackRoll = lastAttackRoll.value[weapon.Weapon] || null
    const extras = resolveDamageExtras({
      character: character.value,
      weapon,
      weaponType,
      attackRoll
    })

    const damage = characterStore.rollDamage({
      numDice,
      modifier: mod + bonusDamage,
      statBonus: statModifier + focusBonus + (extras.statBonus || 0),
      bonusDice: extras.bonusDice,
      stuntBonus: extras.stuntBonus
    })

    // Bonus dice (e.g. Rogue pinpoint) shown green, after the regular dice
    const diceDisplay = h('div', { class: 'dice-display-inline' }, [
      ...damage.dice.map(d => h(ElTag, { size: 'large', class: 'die-tag-inline' }, () => d)),
      ...damage.bonus_dice.map(d => h(ElTag, {
        size: 'large',
        type: 'success',
        class: 'die-tag-inline die-tag-bonus'
      }, () => d))
    ])

    // Dice line: combines weapon mod + bonusDamage inline, plus bonus dice in parens
    const weaponMod = mod + bonusDamage
    let diceLine = `Dice: ${damage.dice.join(', ')}`
    if (weaponMod > 0) diceLine += ` + ${weaponMod}`
    else if (weaponMod < 0) diceLine += ` - ${Math.abs(weaponMod)}`
    if (damage.bonus_dice.length) {
      const bonusSum = damage.bonus_dice.reduce((s, d) => s + d, 0)
      const bonusLabel = extras.bonusDiceLabel || 'bonus'
      diceLine += ` (+${bonusSum} ${bonusLabel})`
    }

    const lineTexts = [diceLine]
    lineTexts.push(`${statToAdd}: ${statModifier >= 0 ? '+' : ''}${statModifier}`)
    if (focusBonus > 0) lineTexts.push(`Focus: +${focusBonus}`)
    if (damage.stunt_bonus > 0) lineTexts.push(`Stunt die: +${damage.stunt_bonus}`)

    const hasExtras = damage.bonus_dice.length > 0 || damage.stunt_bonus > 0
    const totalValue = hasExtras
      ? `${damage.base_total} (${damage.final_total})`
      : `${damage.final_total}`

    const lines = lineTexts.map(t => h('p', {}, t))
    lines.push(h('p', { class: 'final-result' }, `Total Damage: ${totalValue}`))

    const details = h('div', { class: 'roll-details' }, lines)

    rollHistoryStore.add({
      kind: 'damage',
      title: `${weapon.Weapon} Damage`,
      dice: diceWithVariants(damage.dice, { bonusDice: damage.bonus_dice }),
      lines: lineTexts,
      totalLabel: 'Total Damage',
      totalValue
    })

    ElNotification({
      title: `${weapon.Weapon} Damage`,
      message: h('div', {}, [diceDisplay, details]),
      type: 'success',
      position: 'bottom-right',
      duration: 5000,
      customClass: 'dice-roll-notification'
    })
  } catch (error) {
    console.error('Damage roll error:', error)
    ElMessage.error('Failed to roll damage')
  }
}

// Handle armor selection change - update defense and apply penalty
function handleArmorChange(armorDetails) {
  if (!armorDetails) {
    // No armor selected - calculate defense without armor bonus
    character.value.defense = 10 + character.value.stats.Dexterity
    return
  }

  // Calculate defense: 10 + Dexterity + Armor Rating
  const armorRating = armorDetails.Rating || 0
  character.value.defense = 10 + character.value.stats.Dexterity + armorRating

  // Note: Armor Penalty is typically applied to certain checks/actions
  // rather than directly to speed. The penalty value is stored with the armor
  // and can be referenced when making relevant skill checks.

  ElMessage.success(`Armor equipped: ${armorDetails.Name} (Defense: ${character.value.defense})`)
}

function resetCharacter() {
  ElMessageBox.confirm(
    'Creating a new character will discard all current character information. This action cannot be undone. Continue?',
    'New Character',
    {
      confirmButtonText: 'New Character',
      cancelButtonText: 'Cancel',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(() => {
    characterStore.reset()
    uiStore.showStatGenDialog()
    ElMessage.success('New character created!')
  }).catch(() => {
    // User cancelled
  })
}
</script>

<style scoped>
.main-tab {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

/* Profile form label styling */
.profile-card :deep(.el-form-item__label) {
  font-weight: 600;
  font-size: 13px;
  color: #303133;
  padding-bottom: 6px;
  margin-bottom: 0;
}

html.dark .profile-card :deep(.el-form-item__label) {
  color: #fff;
}

.profile-card :deep(.el-form-item) {
  margin-bottom: 16px;
}

.weapon-section {
  margin-bottom: 16px;
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
</style>
