<script setup>
import { useCompareStore } from '@/stores/compare'

const emit = defineEmits(['close'])

const compareStore = useCompareStore()

function formatAnnualFee(annualFee) {
  if (!annualFee) {
    return '-'
  }

  if (typeof annualFee === 'object') {
    return Object.entries(annualFee)
      .map(([key, value]) => {
        if (value === null || value === undefined || value === '') {
          return `${key}: -`
        }

        if (typeof value === 'number') {
          return `${key}: ${value.toLocaleString()}원`
        }

        return `${key}: ${value}`
      })
      .join('\n')
  }

  return String(annualFee)
}

function formatBenefits(benefits) {
  if (!benefits) {
    return ['-']
  }

  if (Array.isArray(benefits)) {
    return benefits.length ? benefits.slice(0, 6) : ['-']
  }

  if (typeof benefits === 'object') {
    const result = []

    Object.entries(benefits).forEach(([category, items]) => {
      if (Array.isArray(items)) {
        items.forEach((item) => {
          result.push(`${category}: ${item}`)
        })
      }
    })

    return result.length ? result.slice(0, 8) : ['-']
  }

  return [String(benefits)]
}
</script>

<template>
  <div class="compare-modal-backdrop">
    <div class="compare-modal">
      <div class="compare-modal-header">
        <h2>카드 비교하기</h2>

        <button
          type="button"
          class="compare-close-btn"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <div class="compare-table-wrap">
        <table class="compare-table">
          <tbody>
            <tr>
              <th>카드상품</th>

              <td
                v-for="card in compareStore.compareCards"
                :key="card.id"
              >
                <h3>{{ card.name }}</h3>
                <p>{{ card.company }}</p>
                <img :src="card.image_url" :alt="card.name" />
              </td>
            </tr>

            <tr>
              <th>카드유형</th>
              <td
                v-for="card in compareStore.compareCards"
                :key="card.id"
              >
                {{ card.card_type || '-' }}
              </td>
            </tr>

            <tr>
              <th>대상</th>
              <td
                v-for="card in compareStore.compareCards"
                :key="card.id"
              >
                {{ card.target || '-' }}
              </td>
            </tr>

            <tr>
              <th>연회비</th>
              <td
                v-for="card in compareStore.compareCards"
                :key="card.id"
                class="pre-line"
              >
                {{ formatAnnualFee(card.annual_fee) }}
              </td>
            </tr>

            <tr>
              <th>주요 혜택</th>
              <td
                v-for="card in compareStore.compareCards"
                :key="card.id"
              >
                <ul class="compare-benefit-list">
                  <li
                    v-for="benefit in formatBenefits(card.benefits)"
                    :key="benefit"
                  >
                    {{ benefit }}
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="compare-modal-actions">
        <button
          type="button"
          class="compare-clear-btn"
          @click="compareStore.clearCards"
        >
          비교함 비우기
        </button>
      </div>
    </div>
  </div>
</template>