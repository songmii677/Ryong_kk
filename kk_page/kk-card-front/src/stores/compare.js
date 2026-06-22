import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useCompareStore = defineStore('compare', () => {
  const savedCards = JSON.parse(localStorage.getItem('compareCards') || '[]')

  const compareCards = ref(savedCards)

  const count = computed(() => compareCards.value.length)

  const isCompared = function (cardId) {
    return compareCards.value.some((card) => String(card.id) === String(cardId))
  }

  const addCard = function (card) {
    if (isCompared(card.id)) {
      return {
        ok: false,
        message: '이미 비교함에 담긴 카드입니다.',
      }
    }

    if (compareCards.value.length >= 3) {
      return {
        ok: false,
        message: '비교함에는 최대 3개까지 담을 수 있습니다.',
      }
    }

    compareCards.value.push({
      id: card.id,
      company: card.company,
      name: card.name,
      card_type: card.card_type,
      target: card.target,
      annual_fee: card.annual_fee,
      benefits: card.benefits,
      image_url: card.image_url,
      detail_url: card.detail_url,
    })

    return {
      ok: true,
      message: '비교함에 담겼습니다.',
    }
  }

  const removeCard = function (cardId) {
    compareCards.value = compareCards.value.filter(
      (card) => String(card.id) !== String(cardId)
    )
  }

  const toggleCard = function (card) {
    if (isCompared(card.id)) {
      removeCard(card.id)

      return {
        ok: true,
        message: '비교함에서 제거했습니다.',
      }
    }

    return addCard(card)
  }

  const clearCards = function () {
    compareCards.value = []
  }

  watch(
    compareCards,
    (newValue) => {
      localStorage.setItem('compareCards', JSON.stringify(newValue))
    },
    { deep: true }
  )

  return {
    compareCards,
    count,
    isCompared,
    addCard,
    removeCard,
    toggleCard,
    clearCards,
  }
})