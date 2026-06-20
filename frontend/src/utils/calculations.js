/**
 * Calculate maximum HP based on character stats and class
 */
export function calculateMaxHP(constitution, charClass, level = 1) {
  let base = constitution + 10

  // Class-specific bonuses
  const classBonus = {
    'Warrior': 5,
    'Rogue': 0,
    'Mage': -5,
    'Envoy': 0
  }

  base += classBonus[charClass] || 0

  // Level-based progression (simplified)
  // Actual game rules may be more complex
  base += (level - 1) * 4

  return Math.max(1, base) // Minimum 1 HP
}

/**
 * Calculate maximum MP based on character stats and class
 */
export function calculateMaxMP(intelligence, charClass, level = 1) {
  if (charClass === 'Mage') {
    return intelligence + 10 + (level - 1) * 3
  } else if (charClass === 'Envoy') {
    return Math.floor((intelligence + 10 + (level - 1) * 2) / 2)
  }

  return 0 // Warriors and Rogues don't get MP by default
}

/**
 * Calculate focus bonus for a stat
 * Focus (1) gives +2 at level 6+, Focus (2) gives +3/+4 at level 11+
 */
export function calculateFocusBonus(primaryFoci, secondaryFoci, level) {
  let bonus = 0

  // Primary focus bonus
  if (primaryFoci.length > 0 && level >= 6) {
    bonus += 2
  }

  // Secondary focus bonus
  if (secondaryFoci.length > 0 && level >= 11) {
    bonus += 2 // Simplified - actual rules may vary
  }

  return bonus
}

/**
 * Format foci for display (showing duplicates as counts)
 */
export function formatFoci(primaryFoci, secondaryFoci) {
  const allFoci = [...primaryFoci, ...secondaryFoci]
  const counted = {}

  allFoci.forEach(focus => {
    counted[focus] = (counted[focus] || 0) + 1
  })

  const formatted = Object.entries(counted).map(([name, count]) => {
    return count > 1 ? `${name} (${count})` : name
  })

  return formatted.join(', ')
}

/**
 * Calculate total currency in copper pieces
 */
export function calculateTotalCopper(gold, silver, copper) {
  return copper + (silver * 10) + (gold * 100)
}

/**
 * Convert total copper to normalized currency
 */
export function normalizeCurrency(totalCopper) {
  const gold = Math.floor(totalCopper / 100)
  const silver = Math.floor((totalCopper % 100) / 10)
  const copper = totalCopper % 10

  return { gold, silver, copper }
}

/**
 * Calculate attack roll bonus for a weapon
 */
export function calculateAttackBonus(stat, focusBonus = 0) {
  return stat + focusBonus
}

/**
 * Determine if a roll is a success
 */
export function isSuccess(total, targetNumber) {
  return total >= targetNumber
}

/**
 * Check if dice show a stunt (any duplicates)
 */
export function hasStunt(dice) {
  return dice.length !== new Set(dice).size
}

/**
 * Resolve class-based damage extras for a damage roll.
 *
 * Stat-comparison conditionals (Envoy COM>WIL, Rogue DEX>target) are
 * folded into a single `auto_apply_damage_extras` toggle on the character —
 * when on, they're assumed true. The level-16 gate and class/weapon rules
 * are applied here.
 *
 * @returns {{ bonusDice: number, stuntBonus: number, statBonus: number, label: string }}
 */
export function resolveDamageExtras({ character, weapon, weaponType, attackRoll }) {
  const out = { bonusDice: 0, stuntBonus: 0, statBonus: 0, label: '', bonusDiceLabel: '' }
  if (!character || !weapon) return out

  const labels = []
  // "Stunt die" in damage rules = the third die of the attack roll,
  // regardless of whether a stunt was actually generated.
  const stuntDie = attackRoll?.dice?.[2] || 0
  const charClass = character.char_class
  const level = character.level || 1
  const auto = character.auto_apply_damage_extras !== false
  const isArcaneBlast = weapon.Group === 'Arcane Blast' || weapon.Weapon === 'Arcane Blast'
  const isSpellWeapon = isArcaneBlast

  if (isArcaneBlast && weapon.DamageStat) {
    out.statBonus += character.stats?.[weapon.DamageStat] || 0
  }

  if (charClass === 'Rogue' && auto) {
    out.bonusDice += 1
    out.bonusDiceLabel = 'pinpoint'
    labels.push('Pinpoint +1d6')
    if (level >= 16 && stuntDie > 0) {
      out.stuntBonus += stuntDie
      labels.push(`Rogue stunt die +${stuntDie}`)
    }
  } else if (level >= 16 && stuntDie > 0) {
    if (charClass === 'Envoy' && auto) {
      out.stuntBonus += stuntDie
      labels.push(`Envoy stunt die +${stuntDie}`)
    } else if (charClass === 'Mage' && isArcaneBlast) {
      out.stuntBonus += stuntDie
      labels.push(`Mage Arcane Blast stunt die +${stuntDie}`)
    } else if (charClass === 'Warrior' && !isSpellWeapon) {
      out.stuntBonus += stuntDie
      labels.push(`Warrior stunt die +${stuntDie}`)
    }
  }

  out.label = labels.join(', ')
  return out
}
