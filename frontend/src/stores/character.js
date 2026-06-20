import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useCharacterStore = defineStore('character', () => {
  // State
  const character = ref({
    id: '',
    name: '',
    player_name: '',
    char_class: 'Warrior',
    background: null,
    level: 1,
    ancestry: '',
    social_class: '',
    speed: 0,
    defense: 0,
    experience: 0,
    photo: null,
    stats: {
      Accuracy: 0,
      Communication: 0,
      Constitution: 0,
      Dexterity: 0,
      Fighting: 0,
      Intelligence: 0,
      Perception: 0,
      Strength: 0,
      Willpower: 0
    },
    foci_primary: {
      Accuracy: [],
      Arcana: [],
      Communication: [],
      Constitution: [],
      Dexterity: [],
      Fighting: [],
      Intelligence: [],
      Perception: [],
      Strength: [],
      Willpower: []
    },
    foci_secondary: {
      Accuracy: [],
      Arcana: [],
      Communication: [],
      Constitution: [],
      Dexterity: [],
      Fighting: [],
      Intelligence: [],
      Perception: [],
      Strength: [],
      Willpower: []
    },
    talents: [],
    specializations: [],
    equipment: {
      armor: null,
      armor_rating: null,
      armor_penalty: null,
      melee_weapons: [],
      ranged_weapons: []
    },
    hp_current: 0,
    hp_max: 0,
    mp_current: 0,
    mp_max: 0,
    magic: {
      arcana: [],
      spells: []
    },
    extras: {
      inventory: [],
      currency: {
        gold: 0,
        silver: 0,
        copper: 0
      },
      stunts: [],
      weapon_groups: [],
      backstory: '',
      relationships: '',
      goals_ties: '',
      extra_notes: ''
    },
    auto_apply_damage_extras: true,
    show_arcana_focus_options: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  })

  // Computed properties
  const hpMax = computed(() => {
    // Base HP calculation: Constitution + 10 + class bonuses
    let base = character.value.stats.Constitution + 10

    // Add class-specific bonuses
    if (character.value.char_class === 'Warrior') {
      base += 5 // Warriors get bonus HP
    }

    // Add level bonuses (simplified - actual calculation would be more complex)
    base += (character.value.level - 1) * 4

    return base
  })

  const mpMax = computed(() => {
    // Only Mages and some classes get MP
    if (character.value.char_class === 'Mage') {
      return character.value.stats.Intelligence + 10 + (character.value.level - 1) * 3
    } else if (character.value.char_class === 'Envoy') {
      return Math.floor((character.value.stats.Intelligence + 10) / 2)
    }
    return 0
  })

  // Actions
  function updateStat(statName, value) {
    character.value.stats[statName] = value
    // Recalculate HP/MP if needed
    if (statName === 'Constitution') {
      character.value.hp_max = hpMax.value
    }
    if (statName === 'Intelligence' && ['Mage', 'Envoy'].includes(character.value.char_class)) {
      character.value.mp_max = mpMax.value
    }
    character.value.updated_at = new Date().toISOString()
  }

  function rollD6(n) {
    if (n <= 0) return []
    const out = []
    for (let i = 0; i < n; i++) out.push(Math.floor(Math.random() * 6) + 1)
    return out
  }

  function rollCheck(modifier = 0, targetNumber = null) {
    const dice = rollD6(3)
    const rollTotal = dice[0] + dice[1] + dice[2]
    const hasStunt = dice[0] === dice[1] || dice[0] === dice[2] || dice[1] === dice[2]
    const finalTotal = rollTotal + modifier
    return {
      dice,
      roll_total: rollTotal,
      final_total: finalTotal,
      has_stunt: hasStunt,
      stunt_points: hasStunt ? dice[2] : 0,
      target_number: targetNumber,
      success: targetNumber !== null ? finalTotal >= targetNumber : null
    }
  }

  function rollDice(modifier = 0) {
    return rollCheck(modifier)
  }

  function rollDamage({ numDice = 0, modifier = 0, statBonus = 0, bonusDice = 0, stuntBonus = 0 } = {}) {
    const dice = rollD6(numDice)
    const bonus = rollD6(bonusDice)
    const baseTotal = dice.reduce((s, d) => s + d, 0) + modifier + statBonus
    const extraTotal = bonus.reduce((s, d) => s + d, 0) + stuntBonus
    return {
      dice,
      bonus_dice: bonus,
      modifier,
      stat_bonus: statBonus,
      stunt_bonus: stuntBonus,
      base_total: baseTotal,
      extra_total: extraTotal,
      final_total: baseTotal + extraTotal
    }
  }

  function saveToLocalStorage() {
    const savedCharacters = JSON.parse(localStorage.getItem('fage_characters') || '{}')

    // Generate ID if new character
    if (!character.value.id) {
      character.value.id = crypto.randomUUID()
      character.value.created_at = new Date().toISOString()
    }

    character.value.updated_at = new Date().toISOString()
    savedCharacters[character.value.id] = character.value

    localStorage.setItem('fage_characters', JSON.stringify(savedCharacters))
    localStorage.setItem('fage_current_character', character.value.id)
  }

  function loadFromLocalStorage(id) {
    const savedCharacters = JSON.parse(localStorage.getItem('fage_characters') || '{}')

    if (savedCharacters[id]) {
      character.value = savedCharacters[id]
      localStorage.setItem('fage_current_character', id)
      return true
    }
    return false
  }

  function loadLastCharacter() {
    const lastId = localStorage.getItem('fage_current_character')
    if (lastId) {
      return loadFromLocalStorage(lastId)
    }
    return false
  }

  function getAllSavedCharacters() {
    const savedCharacters = JSON.parse(localStorage.getItem('fage_characters') || '{}')
    return Object.values(savedCharacters)
  }

  function deleteCharacter(id) {
    const savedCharacters = JSON.parse(localStorage.getItem('fage_characters') || '{}')
    delete savedCharacters[id]
    localStorage.setItem('fage_characters', JSON.stringify(savedCharacters))

    // If we deleted the current character, clear the current ID
    if (localStorage.getItem('fage_current_character') === id) {
      localStorage.removeItem('fage_current_character')
    }
  }

  function reset() {
    character.value = {
      id: '',
      name: '',
      player_name: '',
      char_class: 'Warrior',
      background: null,
      level: 1,
      ancestry: '',
      social_class: '',
      speed: 0,
      defense: 0,
      experience: 0,
      photo: null,
      stats: {
        Accuracy: 0,
        Communication: 0,
        Constitution: 0,
        Dexterity: 0,
        Fighting: 0,
        Intelligence: 0,
        Perception: 0,
        Strength: 0,
        Willpower: 0
      },
      foci_primary: {
        Accuracy: [],
        Arcana: [],
        Communication: [],
        Constitution: [],
        Dexterity: [],
        Fighting: [],
        Intelligence: [],
        Perception: [],
        Strength: [],
        Willpower: []
      },
      foci_secondary: {
        Accuracy: [],
        Arcana: [],
        Communication: [],
        Constitution: [],
        Dexterity: [],
        Fighting: [],
        Intelligence: [],
        Perception: [],
        Strength: [],
        Willpower: []
      },
      talents: [],
      specializations: [],
      equipment: {
        armor: null,
        armor_rating: null,
        armor_penalty: null,
        melee_weapons: [],
        ranged_weapons: []
      },
      hp_current: 0,
      hp_max: 0,
      mp_current: 0,
      mp_max: 0,
      magic: {
        arcana: [],
        spells: []
      },
      extras: {
        inventory: [],
        currency: {
          gold: 0,
          silver: 0,
          copper: 0
        },
        stunts: [],
        weapon_groups: [],
        backstory: '',
        relationships: '',
        goals_ties: '',
        extra_notes: ''
      },
      auto_apply_damage_extras: true,
      show_arcana_focus_options: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  }

  function updatePrimaryFoci(stat, value) {
    character.value.foci_primary[stat] = value
    character.value.updated_at = new Date().toISOString()
  }

  function updateSecondaryFoci(stat, value) {
    character.value.foci_secondary[stat] = value
    character.value.updated_at = new Date().toISOString()
  }

  function updateExtras(extras) {
    // Shallow merge so callers passing a partial extras object (e.g. the
    // Inventory tab, which doesn't manage weapon_groups) don't clobber
    // fields they aren't responsible for.
    character.value.extras = { ...character.value.extras, ...extras }
    character.value.updated_at = new Date().toISOString()
  }

  // Calculate focus bonus for a specific focus
  // - focusName: the specific focus being rolled (e.g., "Arcane Lore")
  // - If focusName is null/undefined, returns 0 (rolling without focus)
  // Returns: +2 at level 1-10, +3 at level 11+ with single focus, +4 with double focus
  function calculateFocusBonus(stat, focusName = null) {
    // If no focus specified, return 0 (rolling the stat directly)
    if (!focusName) return 0

    const level = character.value.level
    const primaryFoci = character.value.foci_primary[stat] || []
    const secondaryFoci = character.value.foci_secondary[stat] || []

    // Check if this focus exists in primary foci
    const hasPrimary = primaryFoci.includes(focusName)
    if (!hasPrimary) return 0

    // Check if this focus is ALSO in secondary (double focus)
    const hasSecondary = secondaryFoci.includes(focusName)

    if (hasSecondary) {
      // Double focus: always +4
      return 4
    } else if (level >= 11) {
      // Single focus at level 11+: +3
      return 3
    } else {
      // Single focus at level 1-10: +2
      return 2
    }
  }

  // Double foci require level 11+. If the level drops below the threshold,
  // clear all secondary foci so stale +4 bonuses don't survive a level rollback.
  watch(
    () => character.value.level,
    (newLevel) => {
      if (newLevel < 11) {
        for (const stat of Object.keys(character.value.foci_secondary)) {
          if (character.value.foci_secondary[stat].length > 0) {
            character.value.foci_secondary[stat] = []
          }
        }
      }
    }
  )

  return {
    character,
    hpMax,
    mpMax,
    updateStat,
    updatePrimaryFoci,
    updateSecondaryFoci,
    updateExtras,
    calculateFocusBonus,
    rollDice,
    rollCheck,
    rollDamage,
    saveToLocalStorage,
    loadFromLocalStorage,
    loadLastCharacter,
    getAllSavedCharacters,
    deleteCharacter,
    reset
  }
})
