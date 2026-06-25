<script setup>
import { computed, ref, unref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCardDetail } from '@/api/cards'
import { useCompareStore } from '@/stores/compare'
import CompareFloatingBar from '@/components/CompareFloatingBar.vue'
import { useFavoriteStore } from '@/stores/favorite'

// 아이콘 이미지 불러오기
import otherIcon from '@/assets/category-icons/other.png'
import foodIcon from '@/assets/category-icons/food.png'
import carIcon from '@/assets/category-icons/car.png'
import cultureIcon from '@/assets/category-icons/culture.png'
import eduIcon from '@/assets/category-icons/edu.png'
import phoneIcon from '@/assets/category-icons/phone.png'
import shoppingIcon from '@/assets/category-icons/shopping.png'
import travelIcon from '@/assets/category-icons/travel.png'

const categoryIconMap = {
  '기타':otherIcon,
  '음식/카페':foodIcon,
  '주유/교통':carIcon,
  '쇼핑/간편결제':shoppingIcon,
  '여행':travelIcon,
  '교육/건강':eduIcon,
  '통신':phoneIcon,
  '문화/생활':cultureIcon,

}
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

const benefitCategories = computed(() => {
  const benefits = unref(card)?.benefits ?? {}

  return Object.entries(benefits)
    .filter(([, items]) => {
      return Array.isArray(items) && items.length > 0
    })
    .map(([category, items]) => {
      return {
        category,
        items,
        icon: categoryIconMap[category] || otherIcon,
      }
    })
    .sort((a, b) => {
      if (a.category === '기타') return -1
      if (b.category === '기타') return 1
      return 0
    })
})

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
        <div class="card-left-area">
          <div class="card-detail-image-box">
            <img
              v-if="card.image_url"
              :src="card.image_url"
              :alt="card.name"
              class="card-detail-image"
              @load="handleCardDetailImageLoad"
            />
          </div>
          
          <div v-if="card.card_type !== 'check'" class="card-fee-row">
          [연회비]
          <template
            v-for="([brand, fee], index) in Object.entries(card.annual_fee)
              .filter(([brand, fee]) => fee)"
            :key="brand"
          >
            <span>
              {{ brand }} {{ fee }}원
            </span>

            <span
              v-if="index !== Object.entries(card.annual_fee)
                .filter(([brand, fee]) => fee).length - 1"
            >
              |
            </span>
          </template>
          </div>
        </div>

          <!-- 오른쪽 -->
          <div class="card-detail-summary">
            <p class="card-detail-company">
              {{ card.company }}
            </p>

            <h1>{{ card.name }}</h1>

            <p>
              {{
                card.card_type === 'credit'
                  ? '신용카드'
                  : card.card_type === 'check'
                    ? '체크카드'
                    : card.card_type
              }}
            </p>
            <p v-if="card.target !== '일반'" >
              {{ card.target }} 대상 카드
            </p>
          </div>

            <div class="detail-action-area">
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
                type="button"
                class="detail-favorite-circle-btn"
                :class="{ active: favoriteStore.isFavorite(card.id) }"
                @click.stop="toggleFavorite"
              >
                <span class="detail-heart-icon">
                  {{ favoriteStore.isFavorite(card.id) ? '❤️' : '🤍' }}
                </span>
              </button>
            </div>
        </section>

        <section
          v-if="benefitCategories.length > 0"
          class="card-detail-section card-benefit-section"
        > <div class="title-section">
            <h2>카테고리별 혜택</h2>
          </div>

          <div class="card-benefit-list">
            <article
              v-for="item in benefitCategories"
              :key="item.category"
              class="card-benefit-row"
            >
              <!-- 왼쪽: 카테고리 아이콘 -->
              <div class="card-benefit-icon-box">
                <img
                  :src="item.icon"
                  :alt="`${item.category} 아이콘`"
                  class="card-benefit-icon"
                />
              </div>

              <!-- 가운데: 카테고리명 -->
              <div class="card-benefit-category-box">
                <h3>{{ item.category }}</h3>
              </div>

              <!-- 오른쪽: 혜택 내용 -->
              <div class="card-benefit-content-box">
                <ul>
                  <li
                    v-for="benefit in item.items"
                    :key="benefit"
                  >
                    {{ benefit }}
                  </li>
                </ul>
              </div>
            </article>
          </div>
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

        <p class="card-notice">
        * 본 카드의 혜택 서비스 내용은 카드사 사정에 따라 사전 고지 후 변경 또는 중단될 수 있습니다.<br />
        * 카드 신청 전 반드시 상품설명서와 약관을 읽어 보시기 바랍니다.
        </p>

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