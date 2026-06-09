<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <nav class="nav">
      <RouterLink to="/">홈</RouterLink>
      <RouterLink to="/cards">전체 카드</RouterLink>
      <RouterLink to="/result">추천 결과</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<style scoped>
.nav {
  display: flex;
  gap: 20px;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.nav a {
  text-decoration: none;
  color: #222;
  font-weight: 600;
}
</style>