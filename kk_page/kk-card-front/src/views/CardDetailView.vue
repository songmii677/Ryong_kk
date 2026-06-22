<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCardDetail } from '@/api/cards'

const route = useRoute()
const router = useRouter()

const card = ref(null)

async function fetchCardDetail() {
  try {
    const response = await getCardDetail(route.params.id)
    card.value = response?.data ?? response
  } catch (error) {
    console.error('카드 상세 조회 실패:', error)
  }
}

function goBackToList() {
  router.push({
    path: '/cards',
    query: {
      ...route.query,
    },
  })
}

function handleCardDetailImageLoad(event) {
  const image = event.currentTarget
  const isPortrait = image.naturalHeight > image.naturalWidth
  image.classList.toggle('is-portrait', isPortrait)
}

onMounted(fetchCardDetail)
</script>


<template>
  <main class="card-detail-page">
    <div class="card-detail-container">
      <div class="card-detail-return-area">
        <button
          type="button"
          class="card-detail-return-button"
          @click="goBackToList"
        >
          목록으로 돌아가기
        </button>
      </div>

      <template v-if="card">
        <section class="card-detail-top-section">
          <div class="card-detail-image-box">
            <img
              v-if="card.image_url"
              :src="card.image_url"
              :alt="card.name"
              class="card-detail-image"
              @load="handleCardDetailImageLoad"
            />
          </div>

          <div class="card-detail-summary">
            <p class="card-detail-company">
              {{ card.company }}
            </p>

            <h1>{{ card.name }}</h1>

            <p>
              카드 유형:
              {{
                card.card_type === 'credit'
                  ? '신용카드'
                  : card.card_type === 'check'
                    ? '체크카드'
                    : card.card_type
              }}
            </p>

            <p>대상: {{ card.target }}</p>
          </div>
        </section>

        <section class="card-detail-section">
          <h2>연회비</h2>

          <ul class="card-detail-fee-list">
            <template
              v-for="(fee, brand) in card.annual_fee"
              :key="brand"
            >
              <li v-if="fee">
                <span>{{ brand }}</span>
                <strong>{{ fee }}원</strong>
              </li>
            </template>
          </ul>
        </section>

        <section class="card-detail-section">
          <h2>혜택</h2>

          <template
            v-for="(items, category) in card.benefits"
            :key="category"
          >
            <div
              v-if="items && items.length"
              class="card-detail-benefit-box"
            >
              <h3>{{ category }}</h3>

              <ul>
                <li
                  v-for="item in items"
                  :key="item"
                >
                  {{ item }}
                </li>
              </ul>
            </div>
          </template>
        </section>

        <a
          v-if="card.detail_url"
          :href="card.detail_url"
          target="_blank"
          rel="noopener noreferrer"
          class="card-detail-link"
        >
          카드 신청하기
        </a>
      </template>

      <p
        v-else
        class="card-detail-loading"
      >
        카드 정보를 불러오는 중입니다.
      </p>
    </div>
  </main>
</template>

<style scoped>
.card-detail-page {
  min-height: calc(100vh - 70px);
  padding: 40px 32px 70px;
  background-color: #f4fbff;
  box-sizing: border-box;
}

.card-detail-container {
  width: 100%;
  max-width: 920px;
  margin: 0 auto;
}

.card-detail-return-area {
  margin-bottom: 18px;
}

.card-detail-return-button {
  appearance: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;

  height: 46px;
  padding: 0 18px;

  border: 1px solid #cfe1d7;
  border-radius: 12px;
  background-color: #ffffff;

  color: #2d9c7a;
  font-family: inherit;
  font-size: 14px;
  font-weight: 800;

  box-shadow: 0 6px 16px rgba(45, 156, 122, 0.08);
  cursor: pointer;

  transition:
    border-color 0.2s,
    background-color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;
}

.card-detail-return-button:hover {
  border-color: #2d9c7a;
  background-color: #eef9f3;
  box-shadow: 0 8px 20px rgba(45, 156, 122, 0.14);
  transform: translateY(-1px);
}

.card-detail-top-section {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  align-items: center;
  gap: 42px;

  padding: 36px;
  border: 1px solid #e4eee8;
  border-radius: 24px;
  background-color: #ffffff;
  box-shadow: 0 10px 28px rgba(45, 156, 122, 0.1);
}

.card-detail-image-box {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 190px;

  border-radius: 18px;
  background-color: transparent;
  overflow: hidden;
}

.card-detail-image {
  display: block;
  width: 88%;
  height: 88%;
  object-fit: contain;
  max-width: none;
  max-height: none;
  transform-origin: center;
}

.card-detail-image.is-portrait {
  width: 100%;
  height: 150%;
  transform: rotate(270deg);
}

.card-detail-summary {
  min-width: 0;
}

.card-detail-company {
  margin: 0 0 8px;
  color: #2d9c7a;
  font-size: 14px;
  font-weight: 800;
}

.card-detail-summary h1 {
  margin: 0 0 22px;
  color: #181b19;
  font-size: 30px;
  line-height: 1.35;
  word-break: keep-all;
}

.card-detail-summary p {
  margin: 8px 0;
  color: #647069;
  font-size: 15px;
}

.card-detail-section {
  margin-top: 22px;
  padding: 30px 34px;

  border: 1px solid #e4eee8;
  border-radius: 22px;
  background-color: #ffffff;
  box-shadow: 0 8px 22px rgba(45, 156, 122, 0.07);
}

.card-detail-section h2 {
  margin: 0 0 20px;
  color: #202522;
  font-size: 21px;
  font-weight: 900;
}

.card-detail-fee-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.card-detail-fee-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 14px 0;
  border-bottom: 1px solid #edf2ef;

  color: #59635d;
  font-size: 14px;
}

.card-detail-fee-list li:last-child {
  border-bottom: none;
}

.card-detail-fee-list strong {
  color: #2d9c7a;
}

.card-detail-benefit-box {
  padding: 20px 0;
  border-bottom: 1px solid #edf2ef;
}

.card-detail-benefit-box:last-child {
  border-bottom: none;
}

.card-detail-benefit-box h3 {
  margin: 0 0 12px;
  color: #2d9c7a;
  font-size: 16px;
  font-weight: 900;
}

.card-detail-benefit-box ul {
  margin: 0;
  padding-left: 20px;
}

.card-detail-benefit-box li {
  margin: 8px 0;
  color: #59635d;
  font-size: 14px;
  line-height: 1.6;
}

.card-detail-link {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 52px;
  margin-top: 24px;

  border-radius: 12px;
  background-color: #2d9c7a;

  color: #ffffff;
  font-size: 15px;
  font-weight: 800;
  text-decoration: none;

  box-shadow: 0 8px 18px rgba(45, 156, 122, 0.2);
  transition:
    background-color 0.2s,
    transform 0.2s;
}

.card-detail-link:hover {
  background-color: #238667;
  transform: translateY(-1px);
}

.card-detail-loading {
  padding: 70px 20px;
  color: #718078;
  text-align: center;
}

@media (max-width: 720px) {
  .card-detail-page {
    padding: 28px 18px 50px;
  }

  .card-detail-top-section {
    grid-template-columns: 1fr;
    gap: 24px;
    padding: 24px;
  }

  .card-detail-image-box {
    max-width: 320px;
    margin: 0 auto;
  }

  .card-detail-section {
    padding: 24px 22px;
  }

  .card-detail-summary h1 {
    font-size: 25px;
  }
}

</style>