<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCards } from '@/api/cards'

const router = useRouter()
const cards = ref([])

onMounted(async () => {
  try {
    const response = await getCards()

    // axios response 형태와 data만 반환하는 형태 둘 다 대응
    cards.value = response?.data ?? response
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
        <div class="card-image-box">
          <img
            v-if="card.image_url"
            :src="card.image_url"
            :alt="card.name"
            class="card-image"
          />
        </div>

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
  font-size: 28px;
  font-weight: 700;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.card-item {
  min-height: 310px;
  padding: 30px 24px 28px;
  border-radius: 22px;
  background-color: #ffffff;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
  cursor: pointer;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  text-align: center;
  overflow: hidden;
  transition: 0.2s;
}

.card-item:hover {
  transform: translateY(-4px);
}

.card-image-box {
  width: 280px;
  height: 75px;
  margin-bottom: 24px;

  display: flex;
  align-items: center;
  justify-content: center;

  overflow: hidden;
  border-radius: 14px;
  background-color: transparent;
}

.card-image {
  width: 280px;
  height: 175px;
  object-fit: contain;
  object-position: center;

  transform: scale(1.9);
  transform-origin: center;
  display: block;
}

.card-info {
  width: 100%;
}

.company {
  color: #777;
  font-size: 14px;
  margin-bottom: 8px;
}

.card-info h2 {
  font-size: 18px;
  margin: 8px 0;
  color: #111;
  font-weight: 600;
  line-height: 1.4;
}

.type {
  color: #555;
  font-size: 14px;
  margin-top: 8px;
}

@media (max-width: 900px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .card-grid {
    grid-template-columns: 1fr;
  }

  .card-item {
    min-height: 290px;
  }

  .card-image-box {
    width: 260px;
    height: 160px;
  }
}
</style>