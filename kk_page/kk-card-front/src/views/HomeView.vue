<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import banklocation from '@/assets/bank-icon.png'
import kkImage from '@/assets/kkk.png'
import chuImage from '@/assets/chu.png'
import playIcon from '@/assets/play-icon.png'
import goldbar from '@/assets/goldbar.png'
import deposit from '@/assets/deposit.png'

const router = useRouter()

const nickname = ref('')

function goSurvey() {
  // if (!nickname.value.trim()) {
  //   alert('닉네임을 입력해주세요!')
  //   return
  // }

  localStorage.setItem('nickname', nickname.value)
  router.push('/survey')
}

function goYoutube() {
  router.push({ name: 'youtube' })
}

function goBankMap() {
  router.push({ name: 'banklocation' })
}

function goPrice() {
  router.push({ name: 'price' })
}
function goDeposit() {
  router.push({ name: 'deposits' })
}
</script>


<template>
  <div class="home-page">
    <header class="top-bar">
      <!-- <button class="icon-btn">☰</button> -->
      <!-- <h1 class="logo">룡크크</h1> -->
    </header>

    <main class="home-main">
      <img
        :src="chuImage"
        alt="핏카츄 로고"
        class="outside-logo"
      />
      <section class="hero-card">
        <p class="badge">카드 추천 테스트</p>

        <div class="character-circle">
          <img :src="kkImage" alt="룡크크" class="dino-image" />
        </div>

        <h2>
          나에게 가장 잘 맞는<br />
          카드는 무엇일까?
        </h2>

        <p class="description">
          간단한 소비 성향 테스트로<br />
          나에게 딱 맞는 카드를 찾아보세요.
        </p>

        <!-- <input
          v-model="nickname"
          class="nickname-input"
          type="text"
          placeholder="닉네임을 입력해주세요"
        /> -->
        
        <button class="start-btn" @click="goSurvey">
          시작하기
        </button>

        <p class="count-text">
          지금까지 12,384명이 참여했어요
        </p>
      </section>

      <div class="feature-floating-menu">
        <!-- 유튜브 이동 버튼 -->
        <button class="feature-floating-btn" @click="goYoutube">
          <img
            :src="playIcon"
            alt="금융 콘텐츠 검색"
            class="feature-floating-icon youtube-icon"
          />
        </button>

        <!-- 카카오맵 이동 버튼 -->
        <button class="feature-floating-btn" @click="goBankMap">
          <img
            :src="banklocation"
            alt="은행 지도 검색"
            class="feature-floating-icon bank-icon"
          />
        </button>

        <!-- 금/은 이동 버튼 -->
        <button class="feature-floating-btn" @click="goPrice">
          <img
            :src="goldbar"
            alt="금/은 비교"
            class="feature-floating-icon bank-icon"
          />
        </button>

        <!-- 예적금 버튼 -->
        <button class="feature-floating-btn" @click="goDeposit">
          <img
            :src="deposit"
            alt="예적금 상품 조회"
            class="feature-floating-icon bank-icon"
          />
        </button>

      </div>

    </main>
  </div>
</template>

