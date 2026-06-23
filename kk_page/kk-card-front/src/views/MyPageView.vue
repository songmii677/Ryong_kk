<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useCompareStore } from '@/stores/compare'
import { useFavoriteStore } from '@/stores/favorite'
import kkImage from '@/assets/kk.jpg'

const router = useRouter()
const accountStore = useAccountStore()
const compareStore = useCompareStore()
const favoriteStore = useFavoriteStore()

const username = computed(() => {
  return (
    accountStore.user?.username ||
    accountStore.username ||
    localStorage.getItem('username') ||
    '룡크크러버'
  )
})

const userIntro = computed(() => {
  return '나에게 딱 맞는 카드 생활을 찾아가는 중이에요.'
})

const compareCount = computed(() => {
  return compareStore.count || 0
})

function goResult() {
  router.push({ name: 'result' })
}

function goCards() {
  router.push({ name: 'cards' })
}

function goGoldChart() {
  // 너희 router/index.js의 금은 그래프 path/name에 맞게 수정
  router.push('/gold-silver')
}

function goCommunity() {
  router.push({name:'myCommunity'})
}

function goProfileEdit() {
  router.push({name:'profileEdit'})
}

function goCardDetail(cardId) {
  router.push(`/cards/${cardId}`)
}

function goFavoriteCards() {
  router.push({ name: 'favorites' })
}

</script>

<template>
  <main class="mypage-page">
    <section class="mypage-container">
      <!-- <header class="mypage-title-card">
        마이페이지
      </header> -->

      <section class="mypage-profile-card">
        <div class="mypage-profile-image-box">
          <img
            :src="kkImage"
            alt="룡크크 프로필"
            class="mypage-profile-image"
          />
        </div>

        <div class="mypage-profile-info">
          <!-- <p class="mypage-profile-label">아이디</p> -->
          <h1>{{ username }}</h1>
          <p class="mypage-profile-intro">
            {{ userIntro }}
          </p>
        </div>
      </section>

      <section class="mypage-action-grid">
        <button
          type="button"
          class="mypage-action-card"
          @click="goResult"
        >
          <span class="mypage-action-icon">💳</span>
          <strong>나의 추천 결과</strong>
          <p>설문 기반 카드 추천 확인</p>
        </button>

        <button
            type="button"
            class="mypage-action-card"
            @click="goFavoriteCards"
            >
            <span class="mypage-action-icon">❤️</span>
            <strong>나의 관심카드</strong>
            <p>담긴 카드 {{ favoriteStore.count }}개</p>
        </button>

        <button
          type="button"
          class="mypage-action-card"
          @click="goGoldChart"
        >
          <span class="mypage-action-icon">📈</span>
          <strong>나의 금리 그래프</strong>
          <p>금·은 가격 변동 확인</p>
        </button>

        <button
          type="button"
          class="mypage-action-card"
          @click="goCommunity"
        >
          <span class="mypage-action-icon">💬</span>
          <strong>커뮤니티 관리</strong>
          <p>작성 글과 댓글 확인</p>
        </button>
      </section>

      <button
        type="button"
        class="mypage-edit-button"
        @click="goProfileEdit"
      >
        회원정보 수정
      </button>
    </section>
  </main>
</template>

<style scoped src="@/assets/styles/mypage.css"></style>