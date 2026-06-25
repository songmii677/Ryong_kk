<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'
import { useRouter } from 'vue-router'

import {
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from 'chart.js'

import {
  getFinancialFavorites,
} from '@/api/deposits'
import { useAccountStore } from '@/stores/accounts'

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
)

const router = useRouter()
const accountStore = useAccountStore()

const favoriteProducts = ref([])
const selectedTerm = ref('12')

const isLoading = ref(false)
const errorMessage = ref('')

const chartCanvas = ref(null)
let chartInstance = null

const terms = [6, 12, 24, 36]

// 선택한 기간의 금리 정보가 있는 관심 상품만 추출
const chartProducts = computed(() => {
  return favoriteProducts.value
    .filter((product) => {
      return Boolean(
        product.rates?.[selectedTerm.value],
      )
    })
    .map((product) => {
      const rate =
        product.rates[selectedTerm.value]

      return {
        id: product.id,
        bankName: product.kor_co_nm,
        productName: product.fin_prdt_nm,
        productType: product.product_type,
        basicRate: rate.basic,
        maxRate:
          rate.max
          ?? rate.basic,
      }
    })
})

async function fetchFavoriteProducts() {
  try {
    isLoading.value = true
    errorMessage.value = ''

    const response =
      await getFinancialFavorites(
        accountStore.token,
      )

    favoriteProducts.value =
      Array.isArray(response.data)
        ? response.data
        : []

    await drawChart()
  } catch (error) {
    console.error(
      '관심 상품 조회 실패:',
      error.response?.data || error,
    )

    errorMessage.value =
      '관심 상품을 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}

function formatRate(value) {
  if (
    value === null
    || value === undefined
  ) {
    return '-'
  }

  return `${Number(value).toFixed(2)}%`
}

async function drawChart() {
  await nextTick()

  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }

  if (
    !chartCanvas.value
    || chartProducts.value.length === 0
  ) {
    return
  }

  const labels = chartProducts.value.map(
    (product) => {
      return (
        `${product.bankName} · `
        + product.productName
      )
    },
  )

  const basicRates = chartProducts.value.map(
    (product) => {
      return product.basicRate ?? 0
    },
  )

  const maxRates = chartProducts.value.map(
    (product) => {
      return product.maxRate ?? 0
    },
  )

  chartInstance = new Chart(
    chartCanvas.value,
    {
      type: 'bar',

      data: {
        labels,

        datasets: [
          {
            label: '기본 금리',
            data: basicRates,
            backgroundColor:
              'rgba(114, 201, 235, 0.75)',
            borderColor: '#72c9eb',
            borderWidth: 1,
            borderRadius: 7,
          },
          {
            label: '최고 금리',
            data: maxRates,
            backgroundColor:
              'rgba(72, 199, 142, 0.78)',
            borderColor: '#48c78e',
            borderWidth: 1,
            borderRadius: 7,
          },
        ],
      },

      options: {
        // 상품명이 길기 때문에 가로 막대그래프로 표시
        indexAxis: 'y',

        responsive: true,
        maintainAspectRatio: false,

        plugins: {
          legend: {
            display: true,
            position: 'top',
          },

          title: {
            display: true,
            text:
              `${selectedTerm.value}개월 `
              + '관심 상품 금리 비교',
            color: '#202522',

            font: {
              size: 17,
              weight: 'bold',
            },
          },

          tooltip: {
            callbacks: {
              label(context) {
                return (
                  `${context.dataset.label}: `
                  + `${Number(
                    context.raw,
                  ).toFixed(2)}%`
                )
              },
            },
          },
        },

        scales: {
          x: {
            beginAtZero: true,

            title: {
              display: true,
              text: '금리 (%)',
            },

            ticks: {
              callback(value) {
                return `${value}%`
              },
            },
          },

          y: {
            ticks: {
              autoSkip: false,
            },
          },
        },
      },
    },
  )
}

function goToProductDetail(productId) {
  router.push(`/deposits/${productId}`)
}

// 기간을 변경하면 그래프 다시 생성
watch(selectedTerm, async () => {
  await drawChart()
})

onMounted(fetchFavoriteProducts)

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
})
</script>

<template>
  <main class="rate-chart-page">
    <section class="rate-chart-container">
      <!-- <button
        type="button"
        class="rate-chart-back-button"
        @click="router.push('/mypage')"
      >
        ← 마이페이지로 돌아가기
      </button> -->

      <header class="rate-chart-heading">
        <h1>나의 금리 그래프</h1>

        <p>
          관심 등록한 예·적금 상품의
          기본금리와 최고금리를 비교합니다.
        </p>
      </header>

      <p
        v-if="isLoading"
        class="rate-chart-state"
      >
        관심 상품을 불러오는 중입니다.
      </p>

      <p
        v-else-if="errorMessage"
        class="rate-chart-state error"
      >
        {{ errorMessage }}
      </p>

      <template v-else>
        <section class="rate-chart-card">
          <div class="rate-chart-card-title">
            <div>
              <h2>관심 금융상품</h2>

              <p>
                총
                {{ favoriteProducts.length }}개 상품
              </p>
            </div>
          </div>

          <p
            v-if="favoriteProducts.length === 0"
            class="rate-chart-empty"
          >
            관심 등록한 예·적금 상품이 없습니다.
          </p>

          <div
            v-else
            class="rate-product-list"
          >
            <button
              v-for="product in favoriteProducts"
              :key="product.id"
              type="button"
              class="rate-product-item"
              @click="goToProductDetail(product.id)"
            >
              <span>{{ product.kor_co_nm }}</span>

              <strong>{{ product.fin_prdt_nm }}</strong>

              <small>
                {{
                  product.product_type === 'deposit'
                    ? '정기예금'
                    : '정기적금'
                }}
              </small>
            </button>
          </div>
        </section>

        <section
          v-if="favoriteProducts.length > 0"
          class="rate-chart-card"
        >
          <div class="rate-chart-card-title chart-title">
            <div>
              <h2>금리 비교</h2>
              <p>비교할 저축 기간을 선택하세요.</p>
            </div>

            <div class="rate-term-buttons">
              <button
                v-for="term in terms"
                :key="term"
                type="button"
                :class="{
                  active:
                    selectedTerm === String(term),
                }"
                @click="selectedTerm = String(term)"
              >
                {{ term }}개월
              </button>
            </div>
          </div>

          <p
            v-if="chartProducts.length === 0"
            class="rate-chart-empty"
          >
            관심 상품 중
            {{ selectedTerm }}개월 금리 정보가 있는
            상품이 없습니다.
          </p>

          <div
            v-else
            class="rate-chart-canvas-box"
            :style="{
              height:
                `${Math.max(
                  340,
                  chartProducts.length * 75,
                )}px`,
            }"
          >
            <canvas ref="chartCanvas"></canvas>
          </div>

          <div
            v-if="chartProducts.length > 0"
            class="rate-chart-summary"
          >
            <article
              v-for="product in chartProducts"
              :key="product.id"
            >
              <div>
                <span>{{ product.bankName }}</span>
                <strong>
                  {{ product.productName }}
                </strong>
              </div>

              <p>
                기본
                <b>
                  {{
                    formatRate(
                      product.basicRate,
                    )
                  }}
                </b>

                · 최고
                <b>
                  {{
                    formatRate(
                      product.maxRate,
                    )
                  }}
                </b>
              </p>
            </article>
          </div>
        </section>
      </template>
    </section>
  </main>
</template>

<style scoped>
.rate-chart-container {
  width: 100%;
  max-width: 1060px;
  margin: 0 auto;
}

.rate-chart-card {
  width: 100%;
  margin-bottom: 24px;
  padding: 30px;

  border: 1px solid #dce9e3;
  border-radius: 24px;
  background-color: #ffffff;

  box-shadow: 0 8px 24px rgba(45, 156, 122, 0.08);
  box-sizing: border-box;
}


/* =========================
   카드 상단 제목 영역
========================= */

.rate-chart-card-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  width: 100%;
  margin-bottom: 24px;
}

.rate-chart-card-title > div:first-child {
  min-width: 0;
}

.rate-chart-card-title h2 {
  margin: 0 0 7px;

  color: #202522;
  font-size: 22px;
  font-weight: 900;
  line-height: 1.3;
}

.rate-chart-card-title p {
  margin: 0;

  color: #758079;
  font-size: 14px;
  line-height: 1.5;
}


/* =========================
   관심 상품 목록
========================= */

.rate-product-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.rate-product-item {
  appearance: none;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: 6px;

  width: 100%;
  min-width: 0;
  min-height: 100px;
  padding: 18px 20px;

  border: 1px solid #dce9e3;
  border-radius: 16px;
  background-color: #f8fcfa;

  font-family: inherit;
  text-align: left;

  box-sizing: border-box;
  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.rate-product-item:hover {
  border-color: #48c78e;
  background-color: #f1fff8;
  box-shadow: 0 7px 18px rgba(45, 156, 122, 0.1);
  transform: translateY(-2px);
}

.rate-product-item span {
  color: #2d9c7a;
  font-size: 13px;
  font-weight: 900;
}

.rate-product-item strong {
  display: block;

  max-width: 100%;

  color: #202522;
  font-size: 16px;
  font-weight: 900;
  line-height: 1.4;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rate-product-item small {
  color: #758079;
  font-size: 13px;
}


/* =========================
   기간 선택 버튼
========================= */

.chart-title {
  align-items: center;
}

.rate-term-buttons {
  display: flex;
  flex-shrink: 0;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 9px;
}

.rate-term-buttons button {
  appearance: none;

  min-width: 62px;
  height: 38px;
  padding: 0 15px;

  border: 1px solid #d3e5dc;
  border-radius: 999px;
  background-color: #ffffff;

  color: #59635d;
  font-family: inherit;
  font-size: 13px;
  font-weight: 800;

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.rate-term-buttons button:hover {
  border-color: #2d9c7a;
  color: #2d9c7a;
  transform: translateY(-1px);
}

.rate-term-buttons button.active {
  border-color: #2d9c7a;
  background-color: #2d9c7a;
  color: #ffffff;
}


/* =========================
   차트 영역
========================= */

.rate-chart-canvas-box {
  position: relative;

  width: 100%;
  max-width: 880px;
  min-height: 350px;
  margin: 0 auto 26px;

  box-sizing: border-box;
}

.rate-chart-canvas-box canvas {
  display: block;

  width: 100% !important;
  height: 100% !important;
}


/* =========================
   차트 하단 금리 목록
========================= */

.rate-chart-summary {
  display: flex;
  flex-direction: column;
  gap: 10px;

  width: 100%;
  margin-top: 8px;
}

.rate-chart-summary article {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 24px;

  min-height: 68px;
  padding: 14px 18px;

  border-radius: 14px;
  background-color: #f6fbf8;

  box-sizing: border-box;
}

.rate-chart-summary article > div {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 5px;
}

.rate-chart-summary span {
  color: #2d9c7a;
  font-size: 13px;
  font-weight: 900;
}

.rate-chart-summary strong {
  display: block;

  max-width: 100%;

  color: #303732;
  font-size: 15px;
  font-weight: 900;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rate-chart-summary p {
  display: flex;
  align-items: center;
  gap: 5px;

  margin: 0;

  color: #647069;
  font-size: 13px;
  white-space: nowrap;
}

.rate-chart-summary b {
  color: #2d9c7a;
  font-size: 14px;
  font-weight: 900;
}


/* =========================
   빈 화면 문구
========================= */

.rate-chart-empty {
  padding: 70px 20px;

  color: #78847d;
  font-size: 14px;
  text-align: center;
}


/* =========================
   반응형
========================= */

@media (max-width: 760px) {
  .rate-chart-card {
    padding: 24px 20px;
  }

  .rate-chart-card-title {
    align-items: flex-start;
    flex-direction: column;
    gap: 17px;
  }

  .rate-term-buttons {
    justify-content: flex-start;
    width: 100%;
  }

  .rate-product-list {
    grid-template-columns: 1fr;
  }

  .rate-chart-canvas-box {
    max-width: none;
    min-height: 320px;
  }

  .rate-chart-summary article {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .rate-chart-summary p {
    white-space: normal;
  }
}

@media (max-width: 480px) {
  .rate-term-buttons {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }

  .rate-term-buttons button {
    width: 100%;
  }
}
</style>

