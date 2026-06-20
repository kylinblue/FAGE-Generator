/**
 * Display-ordering helpers for the character-sheet tables.
 *
 * These keep related rows visually grouped instead of in raw
 * selection/CSV order:
 *   - Talents / Specializations -> grouped by title, Novice -> Expert -> Master
 *   - Spells                    -> grouped by arcana
 *   - Stunts                    -> grouped by type (Combat / Social / Magic ...)
 */

/**
 * Sort rank for a talent/specialization/spell degree.
 * Accepts the long form ('Novice'/'Expert'/'Master') or the numeric
 * degree (1/2/3). Unknown values sort last.
 */
export function degreeRank(degree) {
  switch (String(degree)) {
    case 'Novice':
    case '1':
      return 1
    case 'Expert':
    case '2':
      return 2
    case 'Master':
    case '3':
      return 3
    default:
      return 99
  }
}

/**
 * Stable group-by for table display.
 *
 * Rows sharing the same key are kept together; groups appear in the order
 * their key was first seen (so it tracks selection/CSV order rather than
 * imposing an alphabetical one), and rows within a group are ordered by
 * rankFn, falling back to their original relative order on ties.
 *
 * @param {Array} items                  rows to order (not mutated)
 * @param {(item:any)=>string} keyFn      group key (e.g. talent title, arcana)
 * @param {(item:any)=>number} [rankFn]   intra-group order (e.g. degree)
 * @returns {Array} a new, ordered array
 */
export function groupBy(items, keyFn, rankFn = () => 0) {
  const firstSeen = new Map()
  items.forEach((item, i) => {
    const key = keyFn(item)
    if (!firstSeen.has(key)) firstSeen.set(key, i)
  })

  return items
    .map((item, i) => ({ item, i }))
    .sort((a, b) => {
      const groupDiff = firstSeen.get(keyFn(a.item)) - firstSeen.get(keyFn(b.item))
      if (groupDiff !== 0) return groupDiff
      const rankDiff = rankFn(a.item) - rankFn(b.item)
      if (rankDiff !== 0) return rankDiff
      return a.i - b.i // preserve original order on ties
    })
    .map(({ item }) => item)
}
