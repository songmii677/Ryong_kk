import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import CardListView from '@/views/CardListView.vue'
import CardDetailView from '@/views/CardDetailView.vue'
import ResultView from '@/views/ResultView.vue'
import SurveyView from '@/views/SurveyView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import BankLocationView from '@/views/BankLocationView.vue'
import YoutubeSearchView from '@/views/YoutubeSearchView.vue'
import YoutubeDetailView from '@/views/YoutubeDetailView.vue'
import GoldSilverChartView from '@/views/GoldSilverChartView.vue'
import ProfileEditView from '@/views/ProfileEditView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CommunityUpdateView from '@/views/CommunityUpdateView.vue'
import CommunityDetailView from '@/views/CommunityDetailView.vue'
import CommunityCreateView from '@/views/CommunityCreateView.vue'
import MyPageView from '@/views/MyPageView.vue'
import MyCommunityView from '@/views/MyCommunityView.vue'
import MyRecommendResultVeiw from '@/views/MyRecommendResultVeiw.vue'

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
      component: MyPageView
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('@/views/FavoriteCardsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path:'/community',
      name:'community',
      component: CommunityView
    },

    {
      path:'/community/create',
      name:'communityCreate',
      component: CommunityCreateView
    },

    {
      path:'/community/:id',
      name:'communityDetail',
      component: CommunityDetailView
    },
    {
      path: '/community/edit/:id',
      name: 'CommunityUpdateView',
      component: CommunityUpdateView
    },
    {
      path: '/banklocation',
      name: 'banklocation',
      component: BankLocationView
      // component: () => import('@/views/BankLocationView.vue'),
      // meta: { requiresAuth: true},
    },
    {
      path: '/youtube',
      name: 'youtube',
      component: YoutubeSearchView,
    },
    {
      path: '/youtube/:videoId',
      name: 'youtube-detail',
      component: YoutubeDetailView,
      props: true,
    },
    {
    path: '/price',
    name: 'price',
    component: GoldSilverChartView
    },
    {
    path:'/profile-edit',
    name:'profileEdit',
    component: ProfileEditView 
    },
    {
    path:'/my-community',
    name:'myCommunity',
    component: MyCommunityView
    },
    {
    path:'/myrecommendresult',
    name:'myrecommendresult',
    component: MyRecommendResultVeiw
    }
  ],
})

export default router
