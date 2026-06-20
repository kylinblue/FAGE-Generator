import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // Modal visibility states
  const saveDialogVisible = ref(false)
  const loadDialogVisible = ref(false)
  const deleteDialogVisible = ref(false)
  const diceRollDialogVisible = ref(false)
  const spellDetailDialogVisible = ref(false)
  const statGenDialogVisible = ref(false)

  // Loading states for async operations
  const isLoading = ref(false)
  const loadingMessage = ref('')

  // Current active tab
  const activeTab = ref('main')

  // Dice roll result (shared across components)
  const lastDiceRoll = ref(null)

  // Selected spell for detail view
  const selectedSpell = ref(null)

  // Actions
  function showSaveDialog() {
    saveDialogVisible.value = true
  }

  function hideSaveDialog() {
    saveDialogVisible.value = false
  }

  function showLoadDialog() {
    loadDialogVisible.value = true
  }

  function hideLoadDialog() {
    loadDialogVisible.value = false
  }

  function showDeleteDialog() {
    deleteDialogVisible.value = true
  }

  function hideDeleteDialog() {
    deleteDialogVisible.value = false
  }

  function showDiceRollDialog(rollResult) {
    lastDiceRoll.value = rollResult
    diceRollDialogVisible.value = true
  }

  function hideDiceRollDialog() {
    diceRollDialogVisible.value = false
  }

  function showSpellDetail(spell) {
    selectedSpell.value = spell
    spellDetailDialogVisible.value = true
  }

  function hideSpellDetail() {
    spellDetailDialogVisible.value = false
    selectedSpell.value = null
  }

  function showStatGenDialog() {
    statGenDialogVisible.value = true
  }

  function hideStatGenDialog() {
    statGenDialogVisible.value = false
  }

  function setLoading(loading, message = '') {
    isLoading.value = loading
    loadingMessage.value = message
  }

  function setActiveTab(tab) {
    activeTab.value = tab
  }

  return {
    // State
    saveDialogVisible,
    loadDialogVisible,
    deleteDialogVisible,
    diceRollDialogVisible,
    spellDetailDialogVisible,
    statGenDialogVisible,
    isLoading,
    loadingMessage,
    activeTab,
    lastDiceRoll,
    selectedSpell,

    // Actions
    showSaveDialog,
    hideSaveDialog,
    showLoadDialog,
    hideLoadDialog,
    showDeleteDialog,
    hideDeleteDialog,
    showDiceRollDialog,
    hideDiceRollDialog,
    showSpellDetail,
    hideSpellDetail,
    showStatGenDialog,
    hideStatGenDialog,
    setLoading,
    setActiveTab
  }
})
