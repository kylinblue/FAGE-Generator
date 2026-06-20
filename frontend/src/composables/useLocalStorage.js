/**
 * Composable for LocalStorage operations
 */
export function useLocalStorage() {
  const CHARACTERS_KEY = 'fage_characters'
  const CURRENT_CHARACTER_KEY = 'fage_current_character'

  /**
   * Save a character to LocalStorage
   */
  function saveCharacter(character) {
    const savedCharacters = getAllCharacters()

    // Generate ID if new
    if (!character.id) {
      character.id = crypto.randomUUID()
      character.created_at = new Date().toISOString()
    }

    character.updated_at = new Date().toISOString()
    savedCharacters[character.id] = character

    localStorage.setItem(CHARACTERS_KEY, JSON.stringify(savedCharacters))
    localStorage.setItem(CURRENT_CHARACTER_KEY, character.id)

    return character.id
  }

  /**
   * Load a character from LocalStorage by ID
   */
  function loadCharacter(id) {
    const savedCharacters = getAllCharacters()
    return savedCharacters[id] || null
  }

  /**
   * Get all saved characters
   */
  function getAllCharacters() {
    const data = localStorage.getItem(CHARACTERS_KEY)
    return data ? JSON.parse(data) : {}
  }

  /**
   * Get all characters as an array
   */
  function getAllCharactersArray() {
    const characters = getAllCharacters()
    return Object.values(characters)
  }

  /**
   * Delete a character by ID
   */
  function deleteCharacter(id) {
    const savedCharacters = getAllCharacters()
    delete savedCharacters[id]
    localStorage.setItem(CHARACTERS_KEY, JSON.stringify(savedCharacters))

    // Clear current character if it was deleted
    if (getCurrentCharacterId() === id) {
      localStorage.removeItem(CURRENT_CHARACTER_KEY)
    }
  }

  /**
   * Get the current character ID
   */
  function getCurrentCharacterId() {
    return localStorage.getItem(CURRENT_CHARACTER_KEY)
  }

  /**
   * Set the current character ID
   */
  function setCurrentCharacterId(id) {
    localStorage.setItem(CURRENT_CHARACTER_KEY, id)
  }

  /**
   * Load the last used character
   */
  function loadLastCharacter() {
    const lastId = getCurrentCharacterId()
    if (lastId) {
      return loadCharacter(lastId)
    }
    return null
  }

  /**
   * Export character as JSON file
   */
  function exportCharacterJSON(character) {
    const dataStr = JSON.stringify(character, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${character.name || 'character'}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  /**
   * Import character from JSON file
   */
  function importCharacterJSON(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()

      reader.onload = (e) => {
        try {
          const character = JSON.parse(e.target.result)
          // Generate new ID to avoid conflicts
          character.id = crypto.randomUUID()
          character.imported_at = new Date().toISOString()
          resolve(character)
        } catch (error) {
          reject(new Error('Invalid JSON file'))
        }
      }

      reader.onerror = () => {
        reject(new Error('Failed to read file'))
      }

      reader.readAsText(file)
    })
  }

  /**
   * Clear all saved characters (use with caution!)
   */
  function clearAllCharacters() {
    localStorage.removeItem(CHARACTERS_KEY)
    localStorage.removeItem(CURRENT_CHARACTER_KEY)
  }

  return {
    saveCharacter,
    loadCharacter,
    getAllCharacters,
    getAllCharactersArray,
    deleteCharacter,
    getCurrentCharacterId,
    setCurrentCharacterId,
    loadLastCharacter,
    exportCharacterJSON,
    importCharacterJSON,
    clearAllCharacters
  }
}
