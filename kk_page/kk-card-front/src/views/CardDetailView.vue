<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCardDetail } from '@/api/cards'
import { useCompareStore } from '@/stores/compare'
import CompareFloatingBar from '@/components/CompareFloatingBar.vue'
import { useFavoriteStore } from '@/stores/favorite'

const route = useRoute()
const router = useRouter()
const compareStore = useCompareStore()
const favoriteStore = useFavoriteStore()

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

function toggleCompare() {
  if (!card.value) {
    return
  }

  const result = compareStore.toggleCard(card.value)

  if (!result.ok) {
    alert(result.message)
  }
}

function toggleFavorite() {
  if (!card.value) {
    return
  }

  const result = favoriteStore.toggleCard(card.value)

  if (result.ok) {
    console.log(result.message)
  }
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

            <button
              type="button"
              class="detail-compare-btn"
              :class="{ active: compareStore.isCompared(card.id) }"
              @click.stop="toggleCompare"
            >
              <template v-if="compareStore.isCompared(card.id)">
                <span class="detail-compare-icon">✓</span>
                <span>비교함 담김</span>
              </template>

              <template v-else>
                <span class="detail-compare-icon">+</span>
                <span>비교함에 담기</span>
              </template>
            </button>

            <button
              v-if="card"
              type="button"
              class="detail-favorite-circle-btn"
              :class="{ active: favoriteStore.isFavorite(card.id) }"
              @click.stop="toggleFavorite"
            >
              <span class="detail-heart-icon">
                {{ favoriteStore.isFavorite(card.id) ? '♥' : '♡' }}
              </span>

            </button>
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
    <CompareFloatingBar />
  </main>
</template>

<style scoped src="@/assets/styles/card-detail.css"></style>