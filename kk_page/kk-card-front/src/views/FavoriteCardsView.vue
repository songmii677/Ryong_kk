<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useFavoriteStore } from '@/stores/favorite'
import deleteIcon from '@/assets/delete-icon.png'
import kkImage from '@/assets/kk.jpg'

const router = useRouter()
const accountStore = useAccountStore()
const favoriteStore = useFavoriteStore()

const username = computed(() => {
  return (
    accountStore.user?.username ||
    accountStore.username ||
    localStorage.getItem('username') ||
    '룡크크러버'
  )
})

const sortedFavoriteCards = computed(() => {
  return favoriteStore.favoriteCards
    .map((card, index) => ({
      ...card,
      orderIndex: card.savedAt || index,
    }))
    .sort((a, b) => b.orderIndex - a.orderIndex)
})

function goCardDetail(cardId) {
  router.push(`/cards/${cardId}`)
}

function removeFavorite(cardId) {
  favoriteStore.removeCard(cardId)
}

</script>

<template>
  <main class="favorite-page">
    <section class="favorite-container">
      <header class="favorite-title-card">
        <h1>{{ username }}의 관심카드</h1>
      </header>

      <div class="favorite-top-row">
        <p class="favorite-count">
          총 {{ favoriteStore.count }}개의 관심카드가 있어요.
        </p>
      </div>

      <section
        v-if="sortedFavoriteCards.length > 0"
        class="favorite-card-grid"
      >
        <article
          v-for="card in sortedFavoriteCards"
          :key="card.id"
          class="favorite-card"
        >
          <button
            type="button"
            class="favorite-remove-x"
            @click="removeFavorite(card.id)"
            >
                <img
                :src="deleteIcon"
                alt="관심카드 삭제"
                />
            </button>

          <div class="favorite-card-image-box">
            <img
              :src="card.image_url"
              :alt="card.name"
              class="favorite-card-image"
            />
          </div>

          <div class="favorite-card-info">
            <p>{{ card.company }}</p>
            <h2>{{ card.name }}</h2>
          </div>


            <button
              type="button"
              class="favorite-detail-button"
              @click="goCardDetail(card.id)"
            >
              자세히 살펴보기
            </button>

        </article>
      </section>

        <section
        v-else
        class="favorite-empty-card"
        >

        <p>
            마음에 드는 카드를 하트로 저장하면<br />
            이곳에서 한눈에 확인할 수 있어요.
        </p>

        <button
            type="button"
            class="favorite-empty-button"
            @click="router.push('/cards')"
        >
            카드 둘러보러 가기
        </button>
        </section>
    </section>
  </main>
</template>

<style scoped src="@/assets/styles/favorite-cards.css"></style>