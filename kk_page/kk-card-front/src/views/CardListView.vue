<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCards } from '@/api/cards'

const router = useRouter()
const cards = ref([])

onMounted(async () => {
  try {
    const response = await getCards()
    cards.value = response.data
  } catch (error) {
    console.error('카드 목록 불러오기 실패:', error)
  }
})

function goDetail(cardId) {
  router.push(`/cards/${cardId}`)
}
</script>

<template>
  <main class="card-list-page">
    <h1>전체 카드 보기</h1>

    <section class="card-grid">
      <article
        v-for="card in cards"
        :key="card.id"
        class="card-item"
        @click="goDetail(card.id)"
      >
        <img
          v-if="card.image_url"
          :src="card.image_url"
          :alt="card.name"
          class="card-image"
        />

        <div class="card-info">
          <p class="company">{{ card.company }}</p>
          <h2>{{ card.name }}</h2>
          <p class="type">{{ card.card_type }}</p>
        </div>
      </article>
    </section>
  </main>
</template>

<style scoped>
.card-list-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 20px;
}

.card-list-page h1 {
  margin-bottom: 24px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.card-item {
  padding: 24px;
  border-radius: 18px;
  background-color: #ffffff;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  text-align: center;
}

.card-item:hover {
  transform: translateY(-4px);
  transition: 0.2s;
}

.card-image {
  width: 120px;
  height: 170px;
  object-fit: contain;
  margin-bottom: 16px;
}

.company {
  color: #777;
  font-size: 14px;
}

.card-info h2 {
  font-size: 18px;
  margin: 8px 0;
}

.type {
  color: #555;
  font-size: 14px;
}
</style>