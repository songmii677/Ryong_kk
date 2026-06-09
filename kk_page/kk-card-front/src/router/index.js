import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import CardListView from '@/views/CardListView.vue'
import CardDetailView from '@/views/CardDetailView.vue'
import ResultView from '@/views/ResultView.vue'
import SurveyView from '@/views/SurveyView.vue'

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
    {
      path: '/survey',
      name: 'survey',
      component: SurveyView,
    }
  ],
})

export default router