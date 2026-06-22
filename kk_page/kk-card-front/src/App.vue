<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAccountStore } from './stores/accounts';

const router = useRouter()
const accountStore = useAccountStore()

const handleLogout = async () => {
  await accountStore.logout()
  alert('로그아웃 되었습니다.')
  router.push('/')
}
</script>

<template>
  <div>
    <nav class="nav">
      <RouterLink to="/">홈</RouterLink>
      <RouterLink to="/cards">전체 카드</RouterLink>
      <RouterLink to="/result">추천 결과</RouterLink>

      <div class="nav-right">
        <template v-if="accountStore.isLogin">
          <RouterLink to="/mypage">마이페이지</RouterLink>
          <button class="nav-link-button" @click="handleLogout">로그아웃</button>
          <RouterLink to="/community">커뮤니티</RouterLink>
        </template>
        <template v-else>
          <RouterLink to="/signup">회원가입</RouterLink>
          <RouterLink to="/login">로그인</RouterLink>
        </template>
      </div>
      </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 22px;
  padding: 20px 32px;
  border-bottom: 1px solid #e5eee8;
  background-color: #ffffff;
}

.nav a,
.nav-link-button {
  color: #222;
  font-size: 16px;
  font-weight: 700;
  text-decoration: none;
}

.nav-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 22px;
}

.nav a.router-link-active {
  color: #139b67;
}

.nav-link-button {
  padding: 0;
  border: none;
  background: none;
  font-family: inherit;
  cursor: pointer;
}

.nav a:hover,
.nav-link-button:hover {
  color: #139b67;
}
</style>