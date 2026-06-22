<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCards } from '@/api/cards'

const router = useRouter()

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
  </main>
</template>


<style scoped>
/* =========================
   카드 목록 전체 페이지
========================= */

.card-list-page {
  min-height: calc(100vh - 70px);
  padding: 46px 32px 70px;
  background-color: #f4fbff;
  box-sizing: border-box;
}

.card-list-page > h1 {
  width: 100%;
  max-width: 820px;
  margin: 0 auto 24px;
  color: #222;
  font-size: 30px;
  font-weight: 900;
}


/* =========================
   카드 필터
========================= */

.card-filter-bar {
  display: grid;
  grid-template-columns:
    minmax(180px, 1fr)
    minmax(180px, 1fr)
    100px
    130px;
  align-items: end;
  gap: 14px;

  width: 100%;
  max-width: 820px;
  margin: 0 auto 28px;
  padding: 22px 24px;

  border: 1px solid #e4eee8;
  border-radius: 20px;
  background-color: #ffffff;
  box-shadow: 0 8px 24px rgba(45, 156, 122, 0.08);
  box-sizing: border-box;
}

.card-filter-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.card-filter-field label {
  color: #303833;
  font-size: 14px;
  font-weight: 800;
}

.card-filter-field select {
  width: 100%;
  height: 48px;
  padding: 0 40px 0 14px;

  border: 1px solid #dce8e1;
  border-radius: 12px;
  background-color: #ffffff;

  color: #303833;
  font-family: inherit;
  font-size: 14px;

  outline: none;
  cursor: pointer;
  box-sizing: border-box;

  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.card-filter-field select:hover {
  border-color: #b8d7c7;
}

.card-filter-field select:focus {
  border-color: #2d9c7a;
  box-shadow: 0 0 0 3px rgba(45, 156, 122, 0.12);
}

.card-filter-search-button,
.card-filter-reset-button {
  width: 100%;
  height: 48px;
  padding: 0 14px;
  border-radius: 12px;

  font-family: inherit;
  font-size: 14px;
  font-weight: 800;
  white-space: nowrap;

  cursor: pointer;
  box-sizing: border-box;
  transition: 0.2s;
}

.card-filter-search-button {
  border: 1px solid #2d9c7a;
  background-color: #2d9c7a;
  color: #ffffff;
}

.card-filter-search-button:hover {
  background-color: #238667;
  box-shadow: 0 6px 16px rgba(45, 156, 122, 0.2);
  transform: translateY(-1px);
}

.card-filter-reset-button {
  border: 1px solid #cfe1d7;
  background-color: #ffffff;
  color: #647069;
}

.card-filter-reset-button:hover {
  border-color: #2d9c7a;
  background-color: #eef9f3;
  color: #2d9c7a;
}


/* =========================
   카드 목록
========================= */

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;

  width: 100%;
  max-width: 820px;
  margin: 0 auto;
}

.card-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  min-height: 240px;
  padding: 24px 20px;

  border: 1px solid #edf1ef;
  border-radius: 18px;
  background-color: #ffffff;
  box-shadow: 0 8px 20px rgba(51, 77, 65, 0.08);

  cursor: pointer;
  box-sizing: border-box;

  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.card-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(45, 156, 122, 0.14);
}

.card-image-box {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 180px;
  height: 90px;
  margin-bottom: 16px;

  overflow: hidden;
  border-radius: 12px;
}

.card-image {
  display: block;
  width: 150px;
  height: 90px;
  object-fit: contain;
}

.card-info {
  width: 100%;
  text-align: center;
}

.card-info .company {
  margin: 0 0 7px;
  color: #737d77;
  font-size: 13px;
}

.card-info h2 {
  margin: 0;
  color: #181b19;
  font-size: 17px;
  font-weight: 800;
  line-height: 1.4;
  word-break: keep-all;
}

.card-info .type {
  margin: 8px 0 0;
  color: #737d77;
  font-size: 13px;
}

.empty-message {
  max-width: 820px;
  margin: 70px auto;
  color: #718078;
  text-align: center;
}


/* =========================
   반응형
========================= */

@media (max-width: 850px) {
  .card-filter-bar {
    grid-template-columns: 1fr 1fr;
  }

  .card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .card-list-page {
    padding: 32px 18px 50px;
  }

  .card-filter-bar {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
