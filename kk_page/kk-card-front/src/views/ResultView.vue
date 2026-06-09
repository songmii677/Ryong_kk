<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendCards } from '@/api/cards'

const router = useRouter()

const selectedCategory = ref('쇼핑/간편결제')
const recommendedCards = ref([])

onMounted(async () => {
  try {
    const response = await getRecommendCards(selectedCategory.value, 3)

    console.log('추천 API 원본 응답:', response)

    const data = response?.data ?? response

    console.log('추천 API 실제 데이터:', data)

    if (Array.isArray(data)) {
      recommendedCards.value = data
    } else if (Array.isArray(data.cards)) {
      recommendedCards.value = data.cards
    } else if (Array.isArray(data.results)) {
      recommendedCards.value = data.results
    } else if (Array.isArray(data.data)) {
      recommendedCards.value = data.data
    } else {
      recommendedCards.value = []
    }

    console.log('화면에 표시할 카드:', recommendedCards.value)
  } catch (error) {
    console.error('추천 카드 불러오기 실패:', error)
  }
})

function goDetail(cardId) {
  router.push(`/cards/${cardId}`)
}
</script>

<template>
  <main class="result-page">
    <h1>당신에게 추천하는 카드</h1>

    <p class="desc">
      선택한 소비 성향:
      <strong>{{ selectedCategory }}</strong>
    </p>

    <p v-if="recommendedCards.length === 0">
      추천 카드가 없습니다. API 응답 또는 카드 데이터를 확인해주세요.
    </p>

    <section v-else class="recommend-list">
      <article
        v-for="card in recommendedCards"
        :key="card.id"
        class="recommend-card"
        @click="goDetail(card.id)"
      >
        <img
          v-if="card.image_url"
          :src="card.image_url"
          :alt="card.name"
          class="card-image"
        />

        <div>
          <p class="company">{{ card.company }}</p>
          <h2>{{ card.name }}</h2>

          <ul v-if="card.benefits && card.benefits[selectedCategory]">
            <li
              v-for="benefit in card.benefits[selectedCategory]"
              :key="benefit"
            >
              {{ benefit }}
            </li>
          </ul>
        </div>
      </article>
    </section>

    <button @click="router.push('/cards')" class="more-button">
      다른 카드 더보기
    </button>
  </main>
</template>

<style scoped>
.result-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}

.desc {
  margin-bottom: 28px;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.recommend-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  border-radius: 20px;
  background-color: #ffffff;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  cursor: pointer;
}

.card-image {
  width: 120px;
  height: 170px;
  object-fit: contain;
}

.company {
  color: #777;
}

.more-button {
  margin-top: 28px;
  padding: 14px 24px;
  border: none;
  border-radius: 999px;
  background-color: #222;
  color: white;
  cursor: pointer;
}
</style>