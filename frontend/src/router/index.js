import { createRouter, createWebHistory } from 'vue-router'
import MainTab from '../views/MainTab.vue'
import MagicTab from '../views/MagicTab.vue'
import InventoryTab from '../views/InventoryTab.vue'
import LevelUpTab from '../views/LevelUpTab.vue'

const routes = [
  {
    path: '/',
    redirect: '/main'
  },
  {
    path: '/main',
    name: 'Main',
    component: MainTab,
    meta: { title: 'Character Sheet' }
  },
  {
    path: '/magic',
    name: 'Magic',
    component: MagicTab,
    meta: { title: 'Magic & Spells' }
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: InventoryTab,
    meta: { title: 'Inventory & Extras' }
  },
  {
    path: '/levelup',
    name: 'LevelUp',
    component: LevelUpTab,
    meta: { title: 'Level-Up Progression' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Update document title on route change
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'FAGE Character Generator'
  next()
})

export default router
