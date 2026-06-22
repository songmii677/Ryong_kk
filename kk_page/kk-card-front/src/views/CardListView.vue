<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCards } from '@/api/cards'
import { useCompareStore } from '@/stores/compare'
import CompareFloatingBar from '@/components/CompareFloatingBar.vue'


const router = useRouter()
const compareStore = useCompareStore()

const cards = ref([])
const isLoading = ref(false)

const selectedCardType = ref('')
const selectedCompany = ref('')

const cardTypeOptions = [
  {
    label: '신용카드',
    value: 'credit',
  },
  {
    label: '체크카드',
    value: 'check',
  },
]

const companyOptions = [
  {
    label: '삼성카드',
    value: '삼성',
  },
  {
    label: '하나카드',
    value: '하나',
  },
  {
    label: '국민카드',
    value: '국민',
  },
  {
    label: '신한카드',
    value: '신한카드',
  },
  {
    label: '우리카드',
    value: '우리카드',
  },
]

async function fetchCards() {
  isLoading.value = true

  try {
    const params = {}

    if (selectedCardType.value) {
      params.card_type = selectedCardType.value
    }

    if (selectedCompany.value) {
      params.company = selectedCompany.value
    }

    console.log('필터 요청값:', params)

    const response = await getCards(params)

    cards.value = response.data.results ?? response.data
  } catch (error) {
    console.error('카드 목록 불러오기 실패:', error)
    console.error('백엔드 응답:', error.response?.data)

    cards.value = []
  } finally {
    isLoading.value = false
  }
}

function applyFilters() {
  fetchCards()
}

async function resetFilters() {
  selectedCardType.value = ''
  selectedCompany.value = ''

  await fetchCards()
}

function goDetail(cardId) {
  router.push(`/cards/${cardId}`)
}

onMounted(fetchCards)

function toggleCompare(card) {
  const result = compareStore.toggleCard(card)

  if (!result.ok) {
    alert(result.message)
  }
}


</script>


<template>
  <main class="card-list-page">
    <h1>전체 카드 보기</h1>

    <!-- 필터 영역 -->
<form
  class="card-filter-bar"
  @submit.prevent="applyFilters"
>
  <div class="card-filter-field">
    <label for="card-type">카드 종류</label>

    <select
      id="card-type"
      v-model="selectedCardType"
    >
      <option value="">전체</option>

      <option
        v-for="option in cardTypeOptions"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>

  <div class="card-filter-field">
    <label for="company">카드사</label>

    <select
      id="company"
      v-model="selectedCompany"
    >
      <option value="">전체</option>

      <option
        v-for="option in companyOptions"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
  </div>

  <button
    type="submit"
    class="card-filter-search-button"
  >
    검색
  </button>

  <button
    type="button"
    class="card-filter-reset-button"
    @click="resetFilters"
  >
    필터 초기화
  </button>
</form>

    <!-- 로딩 중 -->
    <p
      v-if="isLoading"
      class="empty-message"
    >
      카드를 불러오는 중입니다.
    </p>

    <!-- 검색 결과 없음 -->
    <p
      v-else-if="cards.length === 0"
      class="empty-message"
    >
      조건에 맞는 카드가 없습니다.
    </p>

    <!-- 카드 목록 -->
    <section
      v-else
      class="card-grid"
    >
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

            <button
              type="button"
              class="card-compare-btn"
              :class="{ active: compareStore.isCompared(card.id) }"
              @click.stop="toggleCompare(card)"
            >
              <template v-if="compareStore.isCompared(card.id)">
                    <span class="compare-plus-icon">✓</span>
                    <!-- <span class="compare-label">담김</span> -->
              </template>

              <template v-else>
                <span class="compare-plus-icon">+</span>
                <span class="compare-label">비교함에 담기</span>
              </template>
            </button>
        </div>

        <div class="card-info">
          <p class="company">
            {{ card.company }}
          </p>

          <h2>{{ card.name }}</h2>

          <p class="type">
            {{
              card.card_type === 'credit'
                ? '신용카드'
                : card.card_type === 'check'
                  ? '체크카드'
                  : card.card_type
            }}
          </p>
        </div>
      </article>
    </section>
    <CompareFloatingBar />
  </main>
</template>


<style scoped src="@/assets/styles/card-list.css"></style>
