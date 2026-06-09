import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import CardListView from '@/views/CardListView.vue'
import CardDetailView from '@/views/CardDetailView.vue'
import ResultView from '@/views/ResultView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/cards',
      name: 'cards',
      component: CardListView,
    },
    {
      path: '/cards/:id',
      name: 'card-detail',
      component: CardDetailView,
    },
    {
      path: '/result',
      name: 'result',
      component: ResultView,
    },
  ],
})

export default router