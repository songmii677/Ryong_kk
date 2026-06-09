<template>
  <div class="survey-page">
    <header class="survey-header">
      <button class="back-btn" @click="goBack">‹</button>

      <div class="progress-wrap">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
    </header>

    <main class="survey-main">
      <p class="question-count">
        {{ currentIndex + 1 }} / {{ questions.length }}
      </p>

      <h2 class="question-title">
        {{ currentQuestion.question }}
      </h2>

      <div class="option-list">
        <button
          v-for="option in currentQuestion.options"
          :key="option.text"
          class="option-btn"
          @click="selectOption(option.value)"
        >
          {{ option.text }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { questions } from '../data/questions.js'

const router = useRouter()

const currentIndex = ref(0)
const answers = ref([])

const currentQuestion = computed(() => {
  return questions[currentIndex.value]
})

const progress = computed(() => {
  return ((currentIndex.value + 1) / questions.length) * 100
})

function selectOption(value) {
  answers.value.push(value)

  if (currentIndex.value < questions.length - 1) {
    currentIndex.value += 1
  } else {
    localStorage.setItem('surveyAnswers', JSON.stringify(answers.value))
    router.push('/result')
  }
}

function goBack() {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1
    answers.value.pop()
  } else {
    router.push('/')
  }
}
</script>