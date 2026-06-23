<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAiRecommendCards } from '@/api/cards'
import LoadingScreen from '@/components/LoadingScreen.vue'

const router = useRouter()

const selectedCategory = ref('')
const persona = ref({
  title: '',
  desc: ''
})
const recommendedCards = ref([])
const aiSummary = ref(null)

const isLoading = ref(true)
const loadingDone = ref(false)
const errorMessage = ref('')

const showAiSummary = ref(true)
const toggleAiSummary = () => {
  showAiSummary.value = !showAiSummary.value
}

onMounted(async () => {
  const answers =
    JSON.parse(localStorage.getItem('surveyAnswers')) || []

  if (answers.length === 0) {
    errorMessage.value = '설문 결과가 없습니다. 다시 테스트를 진행해주세요.'
    loadingDone.value = true

    setTimeout(() => {
      isLoading.value = false
    }, 600)
    return
  }

  try {
    const response = await getAiRecommendCards({
      answers
    })

    console.log('AI 추천 응답:', response.data)

    recommendedCards.value = response.data.cards
    persona.value = response.data.persona
    selectedCategory.value = response.data.selected_category
    aiSummary.value = response.data.ai_summary
  } catch (error) {
    console.error('AI 추천 API 오류:', error)
    errorMessage.value = 'AI 추천 결과를 불러오는 중 오류가 발생했습니다.'
  } finally {
    loadingDone.value = true

    setTimeout(() => {
      isLoading.value = false
    }, 700)
  }
})

const goDetail = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const handleCardimageLoad = (event) => {
  const image = event.currentTarget
  const isPortrait = image.naturalHeight > image.naturalWidth

  image.classList.toggle('is-portrait-card', isPortrait)
  image.classList.toggle('is-landscape-card', !isPortrait)
}
</script>

<template>
  <LoadingScreen v-if="isLoading" :done="loadingDone"/>

  <main v-else class="result-page">
    <section class="result-container">

      <p
        v-if="errorMessage"
        class="empty-message"
      >
        {{ errorMessage }}
      </p>

      <template v-else>
        <section class="result-top">
          <div class="persona-box">
            <h1 class="type-title">
              {{ persona.title }}
            </h1>

            <p class="type-desc">
              {{ persona.desc }}
            </p>
          </div>

          <div class="ai-box">
            <button class="ai-button"
             @click="toggleAiSummary">
              {{ showAiSummary ? '닫기' : 'AI 추천' }}
            </button>

            <p class="ai-caption">
              AI로 똑똑하게<br />
              추천받았어요
            </p>
          </div>
        </section>

        <p class="result-message">
          당신의 소비성향에 맞는 Top3 카드를 보여드립니다.
        </p>

        <section
          v-if="showAiSummary && aiSummary"
          class="ai-summary-section"
        >
          <div class="ai-summary-header">
            <span class="ai-summary-badge">AI 분석</span>
          </div>

          <div class="ai-summary-grid two-columns">
            <article class="ai-summary-card">
              <h4>유형 분석</h4>
              <p>
                {{ aiSummary.type_reason }}
              </p>
            </article>

            <article class="ai-summary-card">
              <h4>추천 이유</h4>
              <p>
                {{ aiSummary.recommend_reason }}
              </p>
            </article>
          </div>
        </section>

        <section
          v-if="recommendedCards.length"
          class="recommend-list"
        >
          <article
            v-for="card in recommendedCards"
            :key="card.id"
            class="recommend-card"
            @click="goDetail(card.id)"
          >
            <div class="card-image-area">
              <img
                v-if="card.image_url"
                :src="card.image_url"
                :alt="card.name"
                class="card-image"
                @load="handleCardimageLoad"
              />

              <span
                v-else
                class="image-placeholder"
              >
                카드
              </span>
            </div>

            <div class="card-info-area">
              <p class="company">
                <span class="card-type-text">
                  {{ card.card_type === 'credit' ? '신용' : '체크' }}
                </span>

                <span class="company-divider"> | </span>

                <span class="company-name-text">
                  {{ card.company }}카드
                </span>
              </p>

              <h2 class="card-name">
                {{ card.name }}
              </h2>

              <ul
                v-if="card.benefits && card.benefits[selectedCategory]"
                class="benefit-list"
              >
                <li
                  v-for="benefit in card.benefits[selectedCategory].slice(0, 3)"
                  :key="benefit"
                >
                  {{ benefit }}
                </li>
              </ul>

              <p
                v-else
                class="reason"
              >
                선택한 소비 성향과 잘 맞는 카드입니다.
              </p>
            </div>
          </article>
        </section>

        <p
          v-else
          class="empty-message"
        >
          추천 카드가 없습니다.
        </p>

        <div class="more-card-row">
          <button
            @click="router.push('/cards')"
            class="more-button"
          >
            다른 카드 더보기
          </button>
        </div>

        <div class="bottom-actions">
          <button
            @click="router.push('/')"
            class="sub-button"
          >
            테스트 다시하기
          </button>

          <button
            @click="router.push('/')"
            class="sub-button"
          >
            결과 저장하기
          </button>
        </div>
      </template>
    </section>
  </main>
</template>


<style scoped src="@/assets/styles/result.css"></style>