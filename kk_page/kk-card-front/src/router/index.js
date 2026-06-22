import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import CardListView from '@/views/CardListView.vue'
import CardDetailView from '@/views/CardDetailView.vue'
import ResultView from '@/views/ResultView.vue'
import SurveyView from '@/views/SurveyView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'

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
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('@/views/MyPageView.vue'),
      meta: { requiresAuth: true},
    },
    {
      path:'/community',
      name:'community',
      component:()=>import(
        '@/views/CommunityView.vue'
      )
    },

    {
      path:'/community/create',
      name:'communityCreate',
      component:()=>import(
        '@/views/CommunityCreateView.vue'
      )
    },

    {
      path:'/community/:id',
      name:'communityDetail',
      component:()=>import(
        '@/views/CommunityDetailView.vue'
      )
    },
    {
      path: '/community/edit/:id',
      name: 'CommunityUpdateView',
      component: () => import('@/views/CommunityUpdateView.vue')
    },
  ],
})

export default router