<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import ryongImage from '@/assets/kk.jpg'

const props = defineProps({
  done: {
    type: Boolean,
    default: false
  }
})

const progress = ref(0)
const messageIndex = ref(0)

const messages = [
  '설문 결과 분석 중..',
  '소비 성향 정리 중..',
  '후보 카드를 찾는 중..',
  'AI가 카드를 추천하는 중..',
]

let progressTimer = null
let messageTimer = null

const currentMessage = computed(() => {
  if (props.done) {
    return '추천 결과 정리 완료!'
  }

  return messages[messageIndex.value]
})

onMounted(() => {
  progressTimer = setInterval(() => {
    if (progress.value < 88) {
      progress.value += Math.floor(Math.random() * 3) + 1
    }
  }, 180)

  messageTimer = setInterval(() => {
    messageIndex.value =
      (messageIndex.value + 1) % messages.length
  }, 1200)
})

watch(
  () => props.done,
  (done) => {
    if (done) {
      progress.value = 100
    }
  }
)

onUnmounted(() => {
  clearInterval(progressTimer)
  clearInterval(messageTimer)
})
</script>

<template>
  <main class="loading-page">
    <section class="loading-card">
      <div class="speech-bubble">
        {{ currentMessage }}
      </div>

      <div class="ryong-area">
        <img
          :src="ryongImage"
          alt="룡크크 캐릭터"
          class="ryong-image"
        />
        <div class="ryong-shadow"></div>
      </div>

      <p class="loading-subtitle">
        룡크크가 딱 맞는 카드를 찾고 있어요
      </p>

      <h1 class="loading-percent">
        {{ progress }}%
      </h1>

      <div class="progress-track">
        <div
          class="progress-fill"
          :style="{ width: progress + '%' }"
        ></div>
      </div>

      <p class="loading-guide">
        잠시만 기다리면 AI 추천 결과가 도착해요.
      </p>
    </section>
  </main>
</template>

<style scoped>
.loading-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(72, 199, 142, 0.16), transparent 32%),
    linear-gradient(180deg, #f4fbff 0%, #f7fcff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  box-sizing: border-box;
}

.loading-card {
  width: 100%;
  max-width: 460px;
  min-height: 620px;
  padding: 52px 36px 44px;
  border-radius: 36px;
  background: #ffffff;
  box-shadow: 0 18px 44px rgba(74, 143, 180, 0.16);
  text-align: center;
  box-sizing: border-box;
}

.speech-bubble {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 54px;
  padding: 0 28px;
  border-radius: 999px;
  background: #c8ff8e;
  color: #2d9c2d;
  font-size: 19px;
  font-weight: 900;
  box-shadow: 0 10px 24px rgba(117, 219, 81, 0.2);
}

.speech-bubble::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -12px;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 14px solid #c8ff8e;
}

.ryong-area {
  margin: 76px auto 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ryong-image {
  width: 170px;
  height: 170px;
  object-fit: contain;
  animation: floatRyong 1.4s ease-in-out infinite;
}

.ryong-shadow {
  width: 96px;
  height: 18px;
  margin-top: 10px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.08);
  animation: shadowPulse 1.4s ease-in-out infinite;
}

.loading-subtitle {
  margin: 0 0 8px;
  color: #222;
  font-size: 20px;
  font-weight: 900;
}

.loading-percent {
  margin: 0 0 22px;
  color: #111;
  font-size: 42px;
  font-weight: 900;
  letter-spacing: -0.04em;
}

.progress-track {
  width: 100%;
  height: 8px;
  border-radius: 999px;
  background: #e7edf2;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #8ee95e, #48c78e);
  transition: width 0.2s ease;
}

.loading-guide {
  margin: 22px 0 0;
  color: #9aa3aa;
  font-size: 15px;
  font-weight: 700;
}

@keyframes floatRyong {
  0% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-14px);
  }

  100% {
    transform: translateY(0);
  }
}

@keyframes shadowPulse {
  0% {
    transform: scale(1);
    opacity: 0.08;
  }

  50% {
    transform: scale(0.82);
    opacity: 0.04;
  }

  100% {
    transform: scale(1);
    opacity: 0.08;
  }
}
</style>