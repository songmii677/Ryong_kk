<script setup>
import {
  computed,
  onMounted,
  ref,
  watch,
} from 'vue'
import { useRouter } from 'vue-router'

import {
  getFinancialProducts,
  toggleFinancialFavorite,
} from '@/api/deposits'
import { useAccountStore } from '@/stores/accounts'


const router = useRouter()
const accountStore = useAccountStore()

const products = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

const selectedType = ref('deposit')
const selectedBank = ref('')
const selectedTerm = ref('')
const keyword = ref('')

const terms = [6, 12, 24, 36]


async function fetchProducts() {
  try {
    isLoading.value = true
    errorMessage.value = ''

    const response = await getFinancialProducts(
      accountStore.token,
    )

    products.value = response.data
  } catch (error) {
    console.error(
      '예적금 목록 조회 실패:',
      error.response?.data || error,
    )

    errorMessage.value =
      '예적금 상품을 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
}


const typeProducts = computed(() => {
  return products.value.filter(
    (product) => {
      return (
        product.product_type
        === selectedType.value
      )
    },
  )
})


const bankOptions = computed(() => {
  const bankNames = typeProducts.value.map(
    (product) => product.kor_co_nm,
  )

  return [...new Set(bankNames)].sort(
    (a, b) => a.localeCompare(b, 'ko'),
  )
})


const filteredProducts = computed(() => {
  const normalizedKeyword = keyword.value
    .trim()
    .toLowerCase()

  return typeProducts.value.filter(
    (product) => {
      const matchesBank =
        !selectedBank.value
        || product.kor_co_nm
          === selectedBank.value

      const matchesTerm =
        !selectedTerm.value
        || Boolean(
          product.rates[
            String(selectedTerm.value)
          ],
        )

      const matchesKeyword =
        !normalizedKeyword
        || product.fin_prdt_nm
          .toLowerCase()
          .includes(normalizedKeyword)
        || product.kor_co_nm
          .toLowerCase()
          .includes(normalizedKeyword)

      return (
        matchesBank
        && matchesTerm
        && matchesKeyword
      )
    },
  )
})


function formatRate(product, term) {
  const rate = product.rates[String(term)]

  if (!rate) {
    return '-'
  }

  const value =
    rate.max !== null
      ? rate.max
      : rate.basic

  if (
    value === null
    || value === undefined
  ) {
    return '-'
  }

  return `${Number(value).toFixed(2)}%`
}


function goToDetail(productId) {
  router.push(`/deposits/${productId}`)
}


async function toggleFavorite(product) {
  if (!accountStore.token) {
    alert(
      '로그인하시면 관심 상품으로 '
      + '등록할 수 있습니다.',
    )
    return
  }

  try {
    const response =
      await toggleFinancialFavorite(
        product.id,
        accountStore.token,
      )

    product.is_favorite =
      response.data.is_favorite
  } catch (error) {
    console.error(
      '관심 상품 처리 실패:',
      error.response?.data || error,
    )

    if (error.response?.status === 401) {
      alert(
        '로그인하시면 관심 상품으로 '
        + '등록할 수 있습니다.',
      )
      return
    }

    alert(
      '관심 상품을 처리하지 못했습니다.',
    )
  }
}


function resetFilters() {
  selectedBank.value = ''
  selectedTerm.value = ''
  keyword.value = ''
}


watch(selectedType, () => {
  selectedBank.value = ''
  selectedTerm.value = ''
})


onMounted(fetchProducts)
</script>


<template>
  <main class="deposit-page">
    <section class="deposit-container">
      <header class="deposit-title-card">
        <h1>예적금 금리 비교</h1>

        <p>
          은행별 예금과 적금 금리를
          비교해 보세요.
        </p>
      </header>

      <div class="deposit-content">
        <aside class="deposit-filter-panel">
          <h2>검색 조건</h2>

          <div class="deposit-type-tabs">
            <button
              type="button"
              :class="{
                active:
                  selectedType === 'deposit',
              }"
              @click="selectedType = 'deposit'"
            >
              정기예금
            </button>

            <button
              type="button"
              :class="{
                active:
                  selectedType === 'saving',
              }"
              @click="selectedType = 'saving'"
            >
              정기적금
            </button>
          </div>

          <label class="deposit-filter-field">
            <span>은행 선택</span>

            <select v-model="selectedBank">
              <option value="">
                전체 은행
              </option>

              <option
                v-for="bank in bankOptions"
                :key="bank"
                :value="bank"
              >
                {{ bank }}
              </option>
            </select>
          </label>

          <label class="deposit-filter-field">
            <span>저축 기간</span>

            <select v-model="selectedTerm">
              <option value="">
                전체 기간
              </option>

              <option
                v-for="term in terms"
                :key="term"
                :value="term"
              >
                {{ term }}개월
              </option>
            </select>
          </label>

          <label class="deposit-filter-field">
            <span>상품 검색</span>

            <input
              v-model="keyword"
              type="search"
              placeholder="상품명 또는 은행명"
            />
          </label>

          <button
            type="button"
            class="deposit-reset-button"
            @click="resetFilters"
          >
            조건 초기화
          </button>
        </aside>

        <section class="deposit-table-section">
          <div class="deposit-table-top">
            <div>
              <h2>
                {{
                  selectedType === 'deposit'
                    ? '정기예금'
                    : '정기적금'
                }}
              </h2>

              <p>
                총
                {{ filteredProducts.length }}개 상품
              </p>
            </div>
          </div>

          <p
            v-if="isLoading"
            class="deposit-state-message"
          >
            상품을 불러오는 중입니다.
          </p>

          <p
            v-else-if="errorMessage"
            class="deposit-state-message error"
          >
            {{ errorMessage }}
          </p>

          <p
            v-else-if="
              filteredProducts.length === 0
            "
            class="deposit-state-message"
          >
            조건에 맞는 상품이 없습니다.
          </p>

          <div
            v-else
            class="deposit-table-wrap"
          >
            <table class="deposit-table">
              <thead>
                <tr>
                  <th>공시월</th>
                  <th>금융회사명</th>
                  <th>상품명</th>

                  <th
                    v-for="term in terms"
                    :key="term"
                  >
                    {{ term }}개월
                  </th>

                  <th>관심</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="product in filteredProducts"
                  :key="product.id"
                  @click="goToDetail(product.id)"
                >
                  <td>
                    {{ product.dcls_month || '-' }}
                  </td>

                  <td class="bank-name">
                    {{ product.kor_co_nm }}
                  </td>

                  <td class="product-name">
                    {{ product.fin_prdt_nm }}
                  </td>

                  <td
                    v-for="term in terms"
                    :key="term"
                    class="rate-cell"
                  >
                    {{ formatRate(product, term) }}
                  </td>

                  <td>
                    <button
                      type="button"
                      class="deposit-favorite-button"
                      :class="{
                        active:
                          product.is_favorite,
                      }"
                      @click.stop="
                        toggleFavorite(product)
                      "
                    >
                      {{
                        product.is_favorite
                          ? '♥'
                          : '♡'
                      }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>


<style
  scoped
  src="@/assets/styles/deposit.css"
></style>