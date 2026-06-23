<script setup>
import { ref, onMounted, unref } from 'vue'
import { useRouter } from 'vue-router'
import { getRecommendCards } from '@/api/cards'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()
const isSaving = ref(false)

const selectedCategory = ref('')
const persona = ref({
  title: '',
  desc: ''
})
const recommendedCards = ref([])

function analyzeAnswers() {
  const answers =
    JSON.parse(localStorage.getItem('surveyAnswers')) || []

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
  if (cardType === 'check' && category === '음식/카페') {
    return {
      title: '☕ 카페 러버',
      desc: '카페와 외식, 배달을 즐기는 소비형'
    }
  }

  if (cardType === 'check' && category === '통신') {
    return {
      title: '💸 알뜰한 생활러',
      desc: '고정 지출을 아끼는 실속형'
    }
  }

  if (cardType === 'credit' && category === '쇼핑/간편결제') {
    return {
      title: '🛍️ 혜택 사냥꾼',
      desc: '쇼핑 할인과 적립을 적극 활용하는 타입'
    }
  }

  if (cardType === 'credit' && category === '여행') {
    return {
      title: '✈️ 여행 준비러',
      desc: '항공과 숙박 혜택을 중요하게 생각하는 타입'
    }
  }

  if (cardType === 'credit' && category === '문화/생활') {
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

  selectedCategory.value = result.topCategory

  persona.value =
    getPersona(result.cardType, result.topCategory)

  try {
    const response =
      await getRecommendCards(selectedCategory.value, 3)

    const data = response?.data ?? response

    if (Array.isArray(data)) {
      recommendedCards.value = data
    } else if (Array.isArray(data.cards)) {
      recommendedCards.value = data.cards
    }
  } catch (error) {
    console.error(error)
  }
})

const handleCardimageLoad = (event) => {
  const image = event.currentTarget
  const isPortrait = image.naturalHeight > image.naturalWidth
  image.classList.toggle('is-portrait-card', isPortrait)
  image.classList.toggle('is-landscape-card', !isPortrait)
}

const saveResult = async () => {
  const personaData = unref(persona)
  const cardData = unref(recommendedCards) || []
  if (!accountStore.token) {
    alert('로그인 후 결과를 저장할 수 있습니다.')
     return
  }
  if (!personaData?.title || !personaData?.desc) {
    alert('추천 결과 정보를 찾을 수 없습니다.')
    return
  }
  const requestData = {
    persona_title: personaData.title,
    personda_description: personaData.desc,
    card_ids: cardData
      .slice(0,3)
      .map((card) => card.id),
  }
  try {
    isSaving.value = true
    await axios.post(
      'http://127.0.0.1:8000/api/cards/results/',
      requestData,
      {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      },
    )
    alert('검사 결과가 저장되었습니다.')
    router.push('/myrecommendresult')
  } catch (error) {
    console.error(
      '추천 결과 저장 실패:',
      error.response?.data || error,
    )
    alert ('검사 결과를 저장하지 못했습니다.')
  } finally {
    isSaving.value = false
  }
}

const goDetail = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const getCardBenefits = (card) => {
  if (!card.benefits || !selectedCategory.value) {
    return []
  }
  const benefits = card.benefits[selectedCategory.value]

  if (!Array.isArray(benefits)) {
    return []
  }

  return benefits.slice(0, 2)
}

const getCardTypeText = (cardType) => {
  if (cardType === 'credit') {
    return '신용'
  }

  if (cardType === 'check') {
    return '체크'
  }

  return cardType || '카드'
}
</script>

<template>
  <main class="result-page">
    <section class="result-container">

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
          <button class="ai-button">
            AI
          </button>

          <p class="ai-caption">
            AI로 똑똑하게 <br/>
            내 카드를 추천받자
          </p>
        </div>
      </section>


      <p class="result-message">
            당신의 소비성향에 맞는 Top3 카드를 보여드립니다.
      </p>
      
      <p
        v-if="recommendedCards.length === 0"
        class="empty-message"
      >
        추천 카드가 없습니다. API 응답 또는 카드 데이터를 확인해주세요.
      </p>

      <section
        v-else
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

            <p v-else class="reason">
              선택한 소비 성향과 잘 맞는 카드입니다.
            </p>
          </div>
        </article>
      </section>

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
    </section>    
      <p class="card-notice">
      * 본 서비스는 카드 추천을 제공하는 플랫폼이며, 모든 선택과 이용에 대한 최종 책임은 사용자에게 있습니다. <br />
      * 본 카드의 혜택 서비스 내용은 카드사 사정에 따라 사전 고지 후 변경 또는 중단될 수 있습니다.<br />
      * 카드 신청 전 반드시 상품설명서와 약관을 읽어 보시기 바랍니다.
      </p>
  </main>

</template>

<style scoped src="@/assets/styles/result.css"></style>