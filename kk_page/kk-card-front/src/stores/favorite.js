import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

export const useFavoriteStore = defineStore('favorite', () => {
  const savedCards = JSON.parse(localStorage.getItem('favoriteCards') || '[]')

  const favoriteCards = ref(savedCards)

  const count = computed(() => favoriteCards.value.length)

  const isFavorite = function (cardId) {
    return favoriteCards.value.some((card) => String(card.id) === String(cardId))
  }

  const addCard = function (card) {
    if (isFavorite(card.id)) {
      return {
        ok: false,
        message: '이미 관심카드에 담긴 카드입니다.',
      }
    }

    favoriteCards.value.push({
      id: card.id,
      company: card.company,
      name: card.name,
      card_type: card.card_type,
      target: card.target,
      annual_fee: card.annual_fee,
      benefits: card.benefits,
      image_url: card.image_url,
      detail_url: card.detail_url,
      savedAt: Date.now(),
    })

    return {
      ok: true,
      message: '관심카드에 추가되었습니다.',
    }
  }

  const removeCard = function (cardId) {
    favoriteCards.value = favoriteCards.value.filter(
      (card) => String(card.id) !== String(cardId)
    )
  }

  const toggleCard = function (card) {
    if (isFavorite(card.id)) {
      removeCard(card.id)

      return {
        ok: true,
        message: '관심카드에서 삭제되었습니다.',
      }
    }

    return addCard(card)
  }

  watch(
    favoriteCards,
    (newValue) => {
      localStorage.setItem('favoriteCards', JSON.stringify(newValue))
    },
    { deep: true }
  )

  return {
    favoriteCards,
    count,
    isFavorite,
    addCard,
    removeCard,
    toggleCard,
  }
})