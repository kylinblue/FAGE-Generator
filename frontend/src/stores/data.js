import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const useDataStore = defineStore('data', () => {
  // State - cached data from backend
  const backgrounds = ref([])
  const armor = ref([])
  const meleeWeapons = ref([])
  const rangedWeapons = ref([])
  const foci = ref({})
  const talents = ref([])
  const specializations = ref([])
  const arcana = ref([])
  const spells = ref([])
  const stunts = ref([])
  const specialFeatures = ref([])
  const levelupTables = ref({})

  // Loading states
  const loading = ref({
    backgrounds: false,
    armor: false,
    meleeWeapons: false,
    rangedWeapons: false,
    foci: false,
    talents: false,
    specializations: false,
    arcana: false,
    spells: false,
    stunts: false,
    specialFeatures: false,
    levelupTables: false
  })

  // Fetch backgrounds
  async function fetchBackgrounds() {
    if (backgrounds.value.length > 0) return // Already cached

    loading.value.backgrounds = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/backgrounds`)
      backgrounds.value = response.data
    } catch (error) {
      console.error('Failed to fetch backgrounds:', error)
      throw error
    } finally {
      loading.value.backgrounds = false
    }
  }

  // Fetch armor
  async function fetchArmor() {
    if (armor.value.length > 0) return // Already cached

    loading.value.armor = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/armor`)
      armor.value = response.data
    } catch (error) {
      console.error('Failed to fetch armor:', error)
      throw error
    } finally {
      loading.value.armor = false
    }
  }

  // Fetch melee weapons
  async function fetchMeleeWeapons() {
    if (meleeWeapons.value.length > 0) return // Already cached

    loading.value.meleeWeapons = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/weapons/melee`)
      meleeWeapons.value = response.data
    } catch (error) {
      console.error('Failed to fetch melee weapons:', error)
      throw error
    } finally {
      loading.value.meleeWeapons = false
    }
  }

  // Fetch ranged weapons
  async function fetchRangedWeapons() {
    if (rangedWeapons.value.length > 0) return // Already cached

    loading.value.rangedWeapons = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/weapons/ranged`)
      rangedWeapons.value = response.data
    } catch (error) {
      console.error('Failed to fetch ranged weapons:', error)
      throw error
    } finally {
      loading.value.rangedWeapons = false
    }
  }

  // Fetch foci
  async function fetchFoci() {
    if (Object.keys(foci.value).length > 0) return // Already cached

    loading.value.foci = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/foci`)
      foci.value = response.data
    } catch (error) {
      console.error('Failed to fetch foci:', error)
      throw error
    } finally {
      loading.value.foci = false
    }
  }

  // Fetch talents (with optional class filter)
  async function fetchTalents(charClass = null) {
    loading.value.talents = true
    try {
      const params = charClass ? { char_class: charClass } : {}
      const response = await axios.get(`${API_BASE}/api/data/talents`, { params })
      talents.value = response.data
    } catch (error) {
      console.error('Failed to fetch talents:', error)
      throw error
    } finally {
      loading.value.talents = false
    }
  }

  // Fetch specializations (with optional class filter)
  async function fetchSpecializations(charClass = null) {
    loading.value.specializations = true
    try {
      const params = charClass ? { char_class: charClass } : {}
      const response = await axios.get(`${API_BASE}/api/data/specializations`, { params })
      specializations.value = response.data
    } catch (error) {
      console.error('Failed to fetch specializations:', error)
      throw error
    } finally {
      loading.value.specializations = false
    }
  }

  // Fetch arcana
  async function fetchArcana() {
    if (arcana.value.length > 0) return // Already cached

    loading.value.arcana = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/arcana`)
      arcana.value = response.data
    } catch (error) {
      console.error('Failed to fetch arcana:', error)
      throw error
    } finally {
      loading.value.arcana = false
    }
  }

  // Fetch spells (with optional arcana filter)
  async function fetchSpells(arcanaFilter = null) {
    loading.value.spells = true
    try {
      const params = arcanaFilter ? { arcana: arcanaFilter } : {}
      const response = await axios.get(`${API_BASE}/api/data/spells`, { params })
      spells.value = response.data
    } catch (error) {
      console.error('Failed to fetch spells:', error)
      throw error
    } finally {
      loading.value.spells = false
    }
  }

  // Fetch stunts
  async function fetchStunts() {
    if (stunts.value.length > 0) return // Already cached

    loading.value.stunts = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/stunts`)
      stunts.value = response.data
    } catch (error) {
      console.error('Failed to fetch stunts:', error)
      throw error
    } finally {
      loading.value.stunts = false
    }
  }

  // Fetch user-authored special features (always re-fetches so manual CSV edits show up)
  async function fetchSpecialFeatures() {
    loading.value.specialFeatures = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/special-features`)
      specialFeatures.value = response.data
    } catch (error) {
      console.error('Failed to fetch special features:', error)
      throw error
    } finally {
      loading.value.specialFeatures = false
    }
  }

  // Fetch level-up table for a specific class
  async function fetchLevelupTable(className) {
    loading.value.levelupTables = true
    try {
      const response = await axios.get(`${API_BASE}/api/data/levelup/${className}`)
      levelupTables.value[className] = response.data
    } catch (error) {
      console.error('Failed to fetch level-up table:', error)
      throw error
    } finally {
      loading.value.levelupTables = false
    }
  }

  // Fetch all essential data at once (for initialization)
  async function fetchEssentialData() {
    await Promise.all([
      fetchBackgrounds(),
      fetchArmor(),
      fetchMeleeWeapons(),
      fetchRangedWeapons()
    ])
  }

  // Clear all cached data (for refresh)
  function clearCache() {
    backgrounds.value = []
    armor.value = []
    meleeWeapons.value = []
    rangedWeapons.value = []
    foci.value = {}
    talents.value = []
    specializations.value = []
    arcana.value = []
    spells.value = []
    stunts.value = []
    specialFeatures.value = []
    levelupTables.value = {}
  }

  return {
    // State
    backgrounds,
    armor,
    meleeWeapons,
    rangedWeapons,
    foci,
    talents,
    specializations,
    arcana,
    spells,
    stunts,
    specialFeatures,
    levelupTables,
    loading,

    // Actions
    fetchBackgrounds,
    fetchArmor,
    fetchMeleeWeapons,
    fetchRangedWeapons,
    fetchFoci,
    fetchTalents,
    fetchSpecializations,
    fetchArcana,
    fetchSpells,
    fetchStunts,
    fetchSpecialFeatures,
    fetchLevelupTable,
    fetchEssentialData,
    clearCache
  }
})
