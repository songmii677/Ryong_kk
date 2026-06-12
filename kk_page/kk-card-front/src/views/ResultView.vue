<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendCards } from '@/api/cards'

const router = useRouter()

const selectedCategory = ref('')
const persona = ref({
  title: '',
  desc: ''
})
const recommendedCards = ref([])

// 카테고리 점수 계산 함수
function analyzeAnswers() {
  const answers =
    JSON.parse(
      localStorage.getItem('surveyAnswers')
    ) || []

  const categoryScore = {}

  let cardType = 'credit'

  answers.forEach(answer => {

    if (answer.key === 'card_type') {
      cardType = answer.value
    }

    if (answer.key === 'category') {
      categoryScore[answer.value] =
        (categoryScore[answer.value] || 0) + 1
    }
  })

  const topCategory =
    Object.entries(categoryScore)
      .sort((a, b) => b[1] - a[1])[0]?.[0]

  return {
    cardType,
    topCategory
  }
}

function getPersona(cardType, category) {

  if (
    cardType === 'check' &&
    category === '음식/카페'
  ) {
    return {
      title: '☕ 카페 러버',
      desc: '카페와 외식, 배달을 즐기는 소비형'
    }
  }

  if (
    cardType === 'check' &&
    category === '통신'
  ) {
    return {
      title: '💸 알뜰한 생활러',
      desc: '고정 지출을 아끼는 실속형'
    }
  }

  if (
    cardType === 'credit' &&
    category === '쇼핑/간편결제'
  ) {
    return {
      title: '🛍️ 혜택 사냥꾼',
      desc: '쇼핑 할인과 적립을 적극 활용하는 타입'
    }
  }

  if (
    cardType === 'credit' &&
    category === '여행'
  ) {
    return {
      title: '✈️ 여행 준비러',
      desc: '항공과 숙박 혜택을 중요하게 생각하는 타입'
    }
  }

  if (
    cardType === 'credit' &&
    category === '문화/생활'
  ) {
    return {
      title: '🎬 OTT 마스터',
      desc: '넷플릭스와 구독 서비스를 즐기는 타입'
    }
  }

  return {
    title: '🌱 사회초년생',
    desc: '실속 있는 소비를 추구하는 타입'
  }
}

onMounted(async () => {

  const result = analyzeAnswers()

  selectedCategory.value =
    result.topCategory

  persona.value =
    getPersona(
      result.cardType,
      result.topCategory
    )

  try {

    const response =
      await getRecommendCards(
        selectedCategory.value,
        3
      )

    const data =
      response?.data ?? response

    if (Array.isArray(data)) {
      recommendedCards.value = data
    } else if (Array.isArray(data.cards)) {
      recommendedCards.value = data.cards
    }

  } catch (error) {
    console.error(error)
  }
})

</script>

<template>
  <main class="result-page">
    <h1>당신은 {{ persona.title }} !</h1>
    <p><strong>{{ persona.desc }}</strong></p>

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