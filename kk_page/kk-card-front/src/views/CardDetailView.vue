<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCardDetail } from '@/api/cards'

const route = useRoute()
const card = ref(null)

onMounted(async () => {
  try {
    const response = await getCardDetail(route.params.id)
    card.value = response.data
  } catch (error) {
    console.error('카드 상세 불러오기 실패:', error)
  }
})
</script>

<template>
  <main v-if="card" class="detail-page">
    <section class="top-section">
      <img
        v-if="card.image_url"
        :src="card.image_url"
        :alt="card.name"
        class="card-image"
      />

      <div>
        <p class="company">{{ card.company }}</p>
        <h1>{{ card.name }}</h1>
        <p>카드 유형: {{ card.card_type }}</p>
        <p>대상: {{ card.target }}</p>
      </div>
    </section>

    <section class="section">
      <h2>연회비</h2>

      <ul>
        <li v-for="(fee, brand) in card.annual_fee" :key="brand">
          {{ brand }}: {{ fee }}원
        </li>
      </ul>
    </section>

    <section class="section">
      <h2>혜택</h2>

      <div
        v-for="(items, category) in card.benefits"
        :key="category"
        class="benefit-box"
      >
        <h3>{{ category }}</h3>

        <ul v-if="items && items.length">
          <li v-for="item in items" :key="item">
            {{ item }}
          </li>
        </ul>

        <p v-else>해당 혜택 없음</p>
      </div>
    </section>

    <a
      v-if="card.detail_url"
      :href="card.detail_url"
      target="_blank"
      class="detail-link"
    >
      카드사 상세 페이지로 이동
    </a>
  </main>

  <main v-else class="detail-page">
    <p>카드 정보를 불러오는 중입니다.</p>
  </main>
</template>

<style scoped>
.detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}

.top-section {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-bottom: 40px;
}

.card-image {
  width: 160px;
  height: 220px;
  object-fit: contain;
}

.company {
  color: #777;
}

.section {
  margin-bottom: 32px;
}

.benefit-box {
  padding: 18px;
  margin-bottom: 16px;
  border-radius: 16px;
  background-color: #f7f7f7;
}

.detail-link {
  display: inline-block;
  margin-top: 20px;
  padding: 14px 24px;
  border-radius: 999px;
  background-color: #222;
  color: white;
  text-decoration: none;
}
</style>