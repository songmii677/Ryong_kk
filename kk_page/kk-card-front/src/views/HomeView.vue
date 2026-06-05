<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const nickname = ref('')

function goSurvey() {
  if (!nickname.value.trim()) {
    alert('닉네임을 입력해주세요!')
    return
  }

  localStorage.setItem('nickname', nickname.value)
  router.push('/survey')
}
</script>


<template>
  <div class="home-page">
    <header class="top-bar">
      <button class="icon-btn">☰</button>
      <h1 class="logo">룡크크</h1>
      <button class="login-btn">로그인</button>
    </header>

    <main class="home-main">
      <section class="hero-card">
        <p class="badge">카드 추천 테스트</p>

        <div class="character-circle">
          <div class="dino">🦖</div>
        </div>

        <h2>
          나에게 가장 잘 맞는<br />
          카드는 뭘까?
        </h2>

        <p class="description">
          간단한 소비 성향 테스트로<br />
          나에게 딱 맞는 카드를 찾아보세요.
        </p>

        <input
          v-model="nickname"
          class="nickname-input"
          type="text"
          placeholder="닉네임을 입력해주세요"
        />
        
        <button class="start-btn" @click="goSurvey">
          크크
        </button>

        <p class="count-text">
          지금까지 12,384명이 참여했어요
        </p>
      </section>
    </main>
  </div>
</template>

