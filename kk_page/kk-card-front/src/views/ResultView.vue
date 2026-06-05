<template>
  <div class="result-page">
    <header class="result-header">
      <p class="badge">추천 결과</p>

      <h2>
        {{ nickname }}님은<br />
        "{{ resultTitle }}"이에요!
      </h2>

      <p class="description">
        설문 답변과 카드 혜택을 비교해서<br />
        가장 잘 맞는 국민카드를 추천했어요.
      </p>
    </header>

    <main class="card-list">
      <article
        v-for="card in visibleCards"
        :key="card.name"
        class="recommend-card"
      >
        <div class="card-image-box">
          <img
            :src="card.image_url"
            :alt="card.name"
            class="card-image"
          />
        </div>

        <div class="card-info">
          <p class="company">
            {{ card.company }}카드 · {{ getCardTypeText(card.card_type) }}
          </p>

          <h3>{{ card.name }}</h3>

          <p class="annual-fee">
            연회비 {{ getAnnualFeeText(card.annual_fee) }}
          </p>

          <div class="benefit-list">
            <span
              v-for="benefit in getMainBenefits(card)"
              :key="benefit"
            >
              {{ benefit }}
            </span>
          </div>

          <p class="reason">
            {{ getRecommendReason(card) }}
          </p>

          <button class="detail-btn" @click="goCardDetail(card.name)">
            카드 자세히 보기
          </button>
        </div>
      </article>
    </main>

    <button
      v-if="!showMore && recommendedCards.length > 3"
      class="more-btn"
      @click="showMore = true"
    >
      추천 카드 더보기
    </button>

    <button class="restart-btn" @click="restart">
      다시 테스트하기
    </button>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import kbCards from '../data/kb.json'

const router = useRouter()

const showMore = ref(false)

const nickname = localStorage.getItem('nickname') || '고객'
const answers = JSON.parse(localStorage.getItem('surveyAnswers')) || []

const selectedCardType = computed(() => {
  return answers.find((answer) => answer.key === 'card_type')?.value
})

const selectedCategories = computed(() => {
  return answers
    .filter((answer) => answer.key === 'category')
    .map((answer) => answer.value)
})

const selectedBenefitKeyword = computed(() => {
  return answers.find((answer) => answer.key === 'benefit_keyword')?.value
})

const selectedFee = computed(() => {
  return answers.find((answer) => answer.key === 'fee')?.value
})

const selectedSimpleType = computed(() => {
  return answers.find((answer) => answer.key === 'simple')?.value
})

const selectedSpendType = computed(() => {
  return answers.find((answer) => answer.key === 'type')?.value
})

const resultTitle = computed(() => {
  const categories = selectedCategories.value

  if (categories.includes('음식/카페') && categories.includes('문화/생활')) {
    return '카페와 콘텐츠를 즐기는 데일리 소비형'
  }

  if (categories.includes('쇼핑/간편결제')) {
    return '온라인 쇼핑 혜택을 챙기는 알뜰 소비형'
  }

  if (categories.includes('주유/교통')) {
    return '교통비를 아끼는 생활 절약형'
  }

  if (categories.includes('여행')) {
    return '해외와 여행 혜택을 챙기는 여행 준비형'
  }

  if (categories.includes('통신')) {
    return '통신비와 구독비를 줄이는 고정비 절약형'
  }

  if (categories.includes('교육/건강')) {
    return '건강과 자기관리를 챙기는 꼼꼼 소비형'
  }

  return '일상 혜택을 골고루 챙기는 실속형'
})

const recommendedCards = computed(() => {
  return kbCards
    .map((card) => {
      const score = calculateScore(card)

      return {
        ...card,
        score
      }
    })
    .filter((card) => card.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
})

const visibleCards = computed(() => {
  if (showMore.value) {
    return recommendedCards.value
  }

  return recommendedCards.value.slice(0, 3)
})

function calculateScore(card) {
  let score = 0

  if (selectedCardType.value && card.card_type === selectedCardType.value) {
    score += 4
  }

  selectedCategories.value.forEach((category) => {
    const categoryBenefits = card.benefits?.[category] || []

    if (categoryBenefits.length > 0) {
      score += 3
    }
  })

  const allBenefitText = getAllBenefitText(card)

  if (
    selectedBenefitKeyword.value &&
    allBenefitText.includes(selectedBenefitKeyword.value)
  ) {
    score += 2
  }

  if (selectedFee.value === 'free' && getMinAnnualFee(card.annual_fee) === 0) {
    score += 3
  }

  if (selectedSimpleType.value === 'simple') {
    if (
      allBenefitText.includes('전 가맹점') ||
      allBenefitText.includes('모든 가맹점') ||
      allBenefitText.includes('기본')
    ) {
      score += 1
    }
  }

  if (selectedSimpleType.value === 'premium') {
    if (
      allBenefitText.includes('최대') ||
      allBenefitText.includes('50%') ||
      allBenefitText.includes('30%')
    ) {
      score += 1
    }
  }

  if (selectedSpendType.value === 'daily') {
    if (
      card.benefits?.['음식/카페']?.length > 0 ||
      card.benefits?.['쇼핑/간편결제']?.length > 0 ||
      card.benefits?.['문화/생활']?.length > 0
    ) {
      score += 1
    }
  }

  if (selectedSpendType.value === 'big_spender') {
    if (card.card_type === 'credit') {
      score += 1
    }
  }

  return score
}

function getAllBenefits(card) {
  return Object.values(card.benefits || {}).flat()
}

function getAllBenefitText(card) {
  return getAllBenefits(card).join(' ')
}

function getMainBenefits(card) {
  const benefits = []

  selectedCategories.value.forEach((category) => {
    const categoryBenefits = card.benefits?.[category] || []
    benefits.push(...categoryBenefits)
  })

  if (benefits.length === 0) {
    benefits.push(...getAllBenefits(card))
  }

  return [...new Set(benefits)].slice(0, 3)
}

function getRecommendReason(card) {
  const matchedCategories = selectedCategories.value.filter((category) => {
    return card.benefits?.[category]?.length > 0
  })

  if (matchedCategories.length > 0) {
    return `${matchedCategories.join(', ')} 영역 혜택이 있어 추천해요.`
  }

  return '설문 답변과 카드 혜택 조건이 잘 맞아 추천해요.'
}

function getAnnualFeeText(annualFee) {
  const minFee = getMinAnnualFee(annualFee)

  if (minFee === null) {
    return '정보 없음'
  }

  if (minFee === 0) {
    return '없음'
  }

  return `${minFee.toLocaleString()}원부터`
}

function getMinAnnualFee(annualFee) {
  const fees = Object.values(annualFee || {}).filter((fee) => {
    return fee !== null && fee !== undefined
  })

  if (fees.length === 0) {
    return null
  }

  return Math.min(...fees)
}

function getCardTypeText(cardType) {
  if (cardType === 'check') {
    return '체크카드'
  }

  if (cardType === 'credit') {
    return '신용카드'
  }

  return cardType
}

function goCardDetail(cardName) {
  router.push(`/cards/${encodeURIComponent(cardName)}`)
}

function restart() {
  localStorage.removeItem('surveyAnswers')
  router.push('/')
}
</script>