<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAccountStore } from './stores/accounts'
import kkImage from '@/assets/kk.jpg'

const router = useRouter()
const accountStore = useAccountStore()

const showLoginGuide = ref(false)

const handleLogout = async () => {
  await accountStore.logout()
  alert('로그아웃 되었습니다.')
  router.push('/')
}

function goResult() {
  if (!accountStore.isLogin) {
    showLoginGuide.value = true
    return
  }

  router.push('/result')
}

function goSignup() {
  showLoginGuide.value = false
  router.push('/signup')
}

function goLogin() {
  showLoginGuide.value = false
  router.push('/login')
}
</script>

<template>
  <div>
    <nav class="nav">
      <RouterLink to="/">홈</RouterLink>
      <RouterLink to="/cards">전체 카드</RouterLink>

      <!-- 비로그인 상태면 모달 안내, 로그인 상태면 추천 결과 이동 -->
      <button class="nav-link-button" @click="goResult">
        추천 결과
      </button>

      <div class="nav-right">
        <template v-if="accountStore.isLogin">
          <RouterLink to="/mypage">마이페이지</RouterLink>
          <button class="nav-link-button" @click="handleLogout">
            로그아웃
          </button>
          <RouterLink to="/community">커뮤니티</RouterLink>
        </template>

        <template v-else>
          <RouterLink to="/signup">회원가입</RouterLink>
          <RouterLink to="/login">로그인</RouterLink>
        </template>
      </div>
    </nav>

    <RouterView />

    <!-- 추천 결과 비로그인 안내 모달 -->
    <div
      v-if="showLoginGuide"
      class="login-guide-backdrop"
      @click.self="showLoginGuide = false"
    >
      <div class="login-guide-modal">
        <button
          type="button"
          class="login-guide-close"
          @click="showLoginGuide = false"
        >
          ×
        </button>

        <div class="login-guide-icon">
          <img :src="kkImage" alt="룡크크"
          class="login-guide-kk">
        </div>

        <h2>
          룡크크에 가입하고<br />
          나만의 카드 추천 결과를<br />
          저장하세요!
        </h2>

        <p>
          로그인하면 추천 결과를 다시 확인하고,<br />
          나에게 맞는 카드 정보를 저장할 수 있어요.
        </p>

        <div class="login-guide-actions">
          <button
            type="button"
            class="signup-guide-btn"
            @click="goSignup"
          >
            회원가입 하기
          </button>

          <button
            type="button"
            class="login-guide-btn"
            @click="goLogin"
          >
            로그인 하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="@/assets/styles/app.css"></style>