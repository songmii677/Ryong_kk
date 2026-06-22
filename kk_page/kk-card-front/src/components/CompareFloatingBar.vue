<script setup>
import { ref } from 'vue'
import { useCompareStore } from '@/stores/compare'
import CompareModal from '@/components/CompareModal.vue'

const compareStore = useCompareStore()
const isModalOpen = ref(false)
</script>

<template>
  <div v-if="compareStore.count > 0" class="compare-bottom-bar">
    <div class="compare-bar-inner">
      <div class="compare-title">
        카드비교
        <span>{{ compareStore.count }}</span>
      </div>

      <div class="compare-card-list">
        <div
          v-for="card in compareStore.compareCards"
          :key="card.id"
          class="compare-mini-card"
        >
          <img :src="card.image_url" :alt="card.name" />

          <p>{{ card.name }}</p>

          <button
            type="button"
            class="compare-remove-btn"
            @click="compareStore.removeCard(card.id)"
          >
            ×
          </button>
        </div>
      </div>

      <button
        type="button"
        class="compare-open-btn"
        @click="isModalOpen = true"
      >
        비교하기
      </button>
    </div>
  </div>

  <CompareModal
    v-if="isModalOpen"
    @close="isModalOpen = false"
  />
</template>