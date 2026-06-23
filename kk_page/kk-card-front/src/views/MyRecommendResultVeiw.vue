<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

// Django에서 받아온 저장 결과 목록
const results = ref([])

// 로딩 상태
const isLoading = ref(false)

// 저장 결과 불러오기
const getMyResults = async () => {
  try {
    isLoading.value = true

    const response = await axios.get(
      'http://127.0.0.1:8000/api/cards/results/',
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )

    console.log('저장된 추천 결과:', response.data)

    results.value = response.data
  } catch (error) {
    console.error(
      '추천 결과 조회 실패:',
      error.response?.data || error,
    )
  } finally {
    isLoading.value = false
  }
}

// 마이페이지가 열릴 때 GET 요청
onMounted(() => {
  getMyResults()
})

function handleCardImageLoad(event) {
  const image = event.currentTarget
  const isPortrait = image.naturalHeight > image.naturalWidth

  image.classList.toggle('is-portrait', isPortrait)
}
</script>


<template>
  <main class="myrecommend-page">
    <!-- 페이지 제목 -->
    <header class="page-header">
      <h1>
        {{ accountStore.username }}님의 카드 추천 결과
      </h1>
    </header>

    <!-- 로딩 중 -->
    <p
      v-if="isLoading"
      class="state-message"
    >
      추천 결과를 불러오는 중입니다.
    </p>

    <!-- 저장된 결과 없음 -->
    <p
      v-else-if="results.length === 0"
      class="state-message"
    >
      저장된 추천 결과가 없습니다.
    </p>

    <!-- 저장된 추천 결과 -->
    <section
      v-else
      class="result-list"
    >
      <article
        v-for="result in results"
        :key="result.id"
        class="result-box"
      >
        <div class="result-row">
          <!-- 왼쪽: 설문 결과 -->
          <div class="persona-area">
            <p class="persona-label">
              나의 추천 결과
            </p>

            <h2 class="persona-title">
              {{ result.persona_title }}
            </h2>

            <p class="persona-description">
              {{ result.persona_description }}
            </p>
          </div>

          <!-- 오른쪽: 추천 카드 3개 -->
          <div class="recommended-card-list">
            <div
              v-for="card in (result.recommended_cards || []).slice(0, 3)"
              :key="card.id"
              class="recommended-card"
            >
            <RouterLink
              :to="`/cards/${card.id}`"
              class="card-detail-link"
              :aria-label="`${card.name}상세 페이지로 이동`"
              >
                <div class="card-image-box">
                  <img
                    v-if="card.image_url"
                    :src="card.image_url"
                    :alt="card.name"
                    class="card-image"
                    @load="handleCardImageLoad"
                  />

                  <span
                    v-else
                    class="image-placeholder"
                  >
                    이미지 없음
                  </span>
                </div>
            </RouterLink>

              <p class="card-company">
                {{ card.company }}카드
              </p>

              <h3 class="card-name">
                {{ card.name }}
              </h3>
            </div>
          </div>
        </div>
      </article>
    </section>
  </main>
</template>

<style scoped src="@/assets/styles/myrecommend.css"></style>