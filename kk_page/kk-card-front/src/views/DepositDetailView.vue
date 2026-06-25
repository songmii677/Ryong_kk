<script setup>
import {
  onMounted,
  ref,
} from 'vue'
import {
  useRoute,
  useRouter,
} from 'vue-router'

import {
  getFinancialProductDetail,
  toggleFinancialFavorite,
} from '@/api/deposits'
import { useAccountStore } from '@/stores/accounts'


const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()

const product = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')


async function fetchProduct() {
  try {
    isLoading.value = true
    errorMessage.value = ''

    const response =
      await getFinancialProductDetail(
        route.params.id,
        accountStore.token,
      )

    product.value = response.data
  } catch (error) {
    console.error(
      '상품 상세 조회 실패:',
      error.response?.data || error,
    )

    errorMessage.value =
      '상품 정보를 불러오지 못했습니다.'
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


async function toggleFavorite() {
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
        product.value.id,
        accountStore.token,
      )

    product.value.is_favorite =
      response.data.is_favorite
  } catch (error) {
    console.error(
      '관심 상품 처리 실패:',
      error.response?.data || error,
    )
  }
}


onMounted(fetchProduct)
</script>


<template>
  <main class="deposit-page">
    <section class="deposit-detail-container">
      <button
        type="button"
        class="deposit-back-button"
        @click="router.push('/deposits')"
      >
        목록으로 돌아가기
      </button>

      <p
        v-if="isLoading"
        class="deposit-state-message"
      >
        상품 정보를 불러오는 중입니다.
      </p>

      <p
        v-else-if="errorMessage"
        class="deposit-state-message error"
      >
        {{ errorMessage }}
      </p>

      <article
        v-else-if="product"
        class="deposit-detail-card"
      >
        <div class="deposit-detail-heading">
          <div>
            <p class="deposit-detail-type">
              {{ product.product_type_name }}
            </p>

            <h1>
              {{ product.fin_prdt_nm }}
            </h1>

            <p class="deposit-detail-bank">
              {{ product.kor_co_nm }}
            </p>
          </div>

          <button
            type="button"
            class="deposit-detail-favorite"
            :class="{
              active: product.is_favorite,
            }"
            @click="toggleFavorite"
          >
            {{
              product.is_favorite
                ? '♥ 관심 상품'
                : '♡ 관심 상품'
            }}
          </button>
        </div>

        <dl class="deposit-info-list">
          <div>
            <dt>가입 대상</dt>
            <dd>
              {{ product.join_member || '-' }}
            </dd>
          </div>

          <div>
            <dt>가입 방법</dt>
            <dd>
              {{ product.join_way || '-' }}
            </dd>
          </div>

          <div>
            <dt>우대 조건</dt>
            <dd>
              {{ product.spcl_cnd || '-' }}
            </dd>
          </div>

          <div>
            <dt>만기 후 이자율</dt>
            <dd>
              {{ product.mtrt_int || '-' }}
            </dd>
          </div>

          <div>
            <dt>기타 유의사항</dt>
            <dd>
              {{ product.etc_note || '-' }}
            </dd>
          </div>
        </dl>

        <h2>기간별 금리</h2>

        <div class="deposit-table-wrap">
          <table class="deposit-table">
            <thead>
              <tr>
                <th>기간</th>
                <th>금리 유형</th>
                <th>적립 유형</th>
                <th>기본 금리</th>
                <th>최고 금리</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="option in product.options"
                :key="option.id"
              >
                <td>
                  {{ option.save_trm }}개월
                </td>

                <td>
                  {{
                    option.intr_rate_type_nm
                    || '-'
                  }}
                </td>

                <td>
                  {{
                    option.rsrv_type_nm
                    || '-'
                  }}
                </td>

                <td>
                  {{
                    formatRate(
                      option.intr_rate,
                    )
                  }}
                </td>

                <td>
                  {{
                    formatRate(
                      option.intr_rate2,
                    )
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>
    </section>
  </main>
</template>


<style
  scoped
  src="@/assets/styles/deposit.css"
></style>