/**
 * Form validation rules composable for FAGE Character Generator.
 * Provides reusable validation rules for character creation forms.
 */

export function useFormValidation() {
  /**
   * Validation rules for character name
   */
  const nameRules = [
    {
      required: true,
      message: 'Character name is required',
      trigger: 'blur'
    },
    {
      min: 1,
      max: 100,
      message: 'Name must be between 1 and 100 characters',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for player name
   */
  const playerNameRules = [
    {
      max: 100,
      message: 'Player name must be less than 100 characters',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for character class
   */
  const classRules = [
    {
      required: true,
      message: 'Please select a character class',
      trigger: 'change'
    },
    {
      validator: (rule, value, callback) => {
        const validClasses = ['Envoy', 'Mage', 'Rogue', 'Warrior']
        if (!validClasses.includes(value)) {
          callback(new Error('Invalid character class'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]

  /**
   * Validation rules for level
   */
  const levelRules = [
    {
      required: true,
      message: 'Level is required',
      trigger: 'blur'
    },
    {
      type: 'number',
      min: 1,
      max: 20,
      message: 'Level must be between 1 and 20',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for stat values (0-20 range)
   */
  const statRules = [
    {
      required: true,
      message: 'Stat value is required',
      trigger: 'blur'
    },
    {
      type: 'number',
      min: 0,
      max: 20,
      message: 'Stat must be between 0 and 20',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for HP/MP values
   */
  const pointsRules = [
    {
      type: 'number',
      min: 0,
      message: 'Value must be 0 or greater',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for backstory
   */
  const backstoryRules = [
    {
      max: 5000,
      message: 'Backstory must be less than 5000 characters',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for inventory item name
   */
  const itemNameRules = [
    {
      required: true,
      message: 'Item name is required',
      trigger: 'blur'
    },
    {
      min: 1,
      message: 'Item name must not be empty',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for inventory item quantity
   */
  const quantityRules = [
    {
      required: true,
      message: 'Quantity is required',
      trigger: 'blur'
    },
    {
      type: 'number',
      min: 1,
      message: 'Quantity must be at least 1',
      trigger: 'blur'
    }
  ]

  /**
   * Validation rules for currency values
   */
  const currencyRules = [
    {
      type: 'number',
      min: 0,
      message: 'Currency must be 0 or greater',
      trigger: 'blur'
    }
  ]

  /**
   * Validate entire character object
   * @param {Object} character - Character data to validate
   * @returns {Object} - Validation result with isValid and errors
   */
  function validateCharacter(character) {
    const errors = []

    // Validate name
    if (!character.name || character.name.trim().length === 0) {
      errors.push('Character name is required')
    } else if (character.name.length > 100) {
      errors.push('Character name must be less than 100 characters')
    }

    // Validate class
    const validClasses = ['Envoy', 'Mage', 'Rogue', 'Warrior']
    if (!character.char_class || !validClasses.includes(character.char_class)) {
      errors.push('Please select a valid character class')
    }

    // Validate level
    if (character.level < 1 || character.level > 20) {
      errors.push('Level must be between 1 and 20')
    }

    // Validate stats
    const statNames = ['Accuracy', 'Communication', 'Constitution', 'Dexterity', 'Fighting', 'Intelligence', 'Perception', 'Strength', 'Willpower']
    if (character.stats) {
      for (const stat of statNames) {
        const value = character.stats[stat]
        if (value === undefined || value < 0 || value > 20) {
          errors.push(`${stat} must be between 0 and 20`)
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    }
  }

  return {
    nameRules,
    playerNameRules,
    classRules,
    levelRules,
    statRules,
    pointsRules,
    backstoryRules,
    itemNameRules,
    quantityRules,
    currencyRules,
    validateCharacter
  }
}
