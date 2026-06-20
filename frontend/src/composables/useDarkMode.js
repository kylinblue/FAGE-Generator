/**
 * Dark mode composable for FAGE Character Generator.
 * Manages dark mode state with localStorage persistence.
 */

import { ref, watch, onMounted } from 'vue'

const DARK_MODE_KEY = 'fage_dark_mode'

// Shared state across all components
const isDark = ref(false)

export function useDarkMode() {
  /**
   * Toggle dark mode on/off.
   */
  function toggleDarkMode() {
    isDark.value = !isDark.value
  }

  /**
   * Set dark mode explicitly.
   * @param {boolean} value - True for dark mode, false for light mode
   */
  function setDarkMode(value) {
    isDark.value = value
  }

  /**
   * Apply dark mode to the document.
   */
  function applyDarkMode() {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  /**
   * Load dark mode preference from localStorage.
   */
  function loadDarkModePreference() {
    const saved = localStorage.getItem(DARK_MODE_KEY)
    if (saved !== null) {
      isDark.value = saved === 'true'
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      isDark.value = prefersDark
    }
    applyDarkMode()
  }

  /**
   * Save dark mode preference to localStorage.
   */
  function saveDarkModePreference() {
    localStorage.setItem(DARK_MODE_KEY, isDark.value.toString())
  }

  // Watch for changes and apply
  watch(isDark, () => {
    applyDarkMode()
    saveDarkModePreference()
  })

  // Initialize on mount
  onMounted(() => {
    loadDarkModePreference()
  })

  return {
    isDark,
    toggleDarkMode,
    setDarkMode
  }
}
