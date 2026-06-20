import { defineStore } from 'pinia'
import { ref } from 'vue'

const MAX_ENTRIES = 10

/**
 * Session-only log of recent dice rolls (attack/damage/spell/ability).
 * Newest first. Capped at MAX_ENTRIES.
 *
 * Entry shape:
 *   { id, ts, title, kind, dice: [{ value, variant }], lines: string[],
 *     totalLabel, totalValue, totalClass?, stuntPoints? }
 *   variant ∈ 'normal' | 'stunt' | 'bonus'
 *   kind   ∈ 'attack' | 'damage' | 'spell' | 'check'
 *   totalClass ∈ 'success' | 'danger' (used for spell pass/fail tinting)
 */
export const useRollHistoryStore = defineStore('rollHistory', () => {
  const entries = ref([])

  function add(entry) {
    const stamped = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      ts: Date.now(),
      ...entry
    }
    entries.value.unshift(stamped)
    if (entries.value.length > MAX_ENTRIES) {
      entries.value.length = MAX_ENTRIES
    }
  }

  function clear() {
    entries.value = []
  }

  return { entries, add, clear }
})

/**
 * Tag each die with a variant. Stunt die (the 3rd die of a 3d6 check, when
 * the first two match) renders red. Bonus dice (e.g. Rogue Pinpoint) render
 * green and are appended after the regular dice.
 */
export function diceWithVariants(dice, { hasStunt = false, bonusDice = [] } = {}) {
  const out = dice.map((value, i) => ({
    value,
    variant: hasStunt && i === 2 ? 'stunt' : 'normal'
  }))
  for (const value of bonusDice) {
    out.push({ value, variant: 'bonus' })
  }
  return out
}
