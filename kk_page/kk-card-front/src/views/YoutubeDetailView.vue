<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const videoId = computed(() => route.params.videoId)
const title = computed(() => route.query.title || '영상 제목 정보 없음')
const channelTitle = computed(() => route.query.channelTitle || '채널 정보 없음')
const publishedAt = computed(() => {
  if (!route.query.publishedAt) {
    return '업로드 날짜 정보 없음'
  }
  return String(route.query.publishedAt).slice(0, 10)
})

const videoUrl = computed(() => {
  return `https://www.youtube.com/embed/${videoId.value}`
})
</script>

<template>
  <main class="detail-page">
    <section class="detail-header">
      <button class="back-button" @click="router.back()">
        ← 검색 결과로 돌아가기
      </button>

      <p class="sub-title">FitCH Video Detail</p>
      <h1>핏카츄 금융 영상 상세</h1>
    </section>

    <section class="video-section">
      <div class="iframe-wrapper">
        <iframe
          :src="videoUrl"
          title="YouTube video player"
          frameborder="0"
          allowfullscreen
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        ></iframe>
      </div>

      <div class="video-meta">
        <h2>{{ title }}</h2>

        <div class="meta-list">
          <p>
            <span>채널명</span>
            {{ channelTitle }}
          </p>
          <p>
            <span>업로드 날짜</span>
            {{ publishedAt }}
          </p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  padding: 40px 24px;
  background: linear-gradient(180deg, #dff5ff 0%, #f7fcff 100%);
  color: #1f2d2a;
}

.detail-header {
  max-width: 1000px;
  margin: 0 auto 28px;
}

.back-button {
  margin-bottom: 24px;
  padding: 10px 16px;
  border: 1px solid #b8efd8;
  border-radius: 999px;
  background: white;
  color: #2d9c7a;
  font-weight: 700;
  cursor: pointer;
}

.back-button:hover {
  background: #e5fff4;
  border-color: #48c78e;
}

.sub-title {
  margin: 0 0 8px;
  color: #2d9c7a;
  font-weight: 800;
  letter-spacing: 0.08em;
  font-size: 14px;
}

.detail-header h1 {
  margin: 0;
  font-size: 34px;
  font-weight: 800;
  color: #1f2d2a;
}

.video-section {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
  border-radius: 28px;
  background: white;
  box-shadow: 0 12px 28px rgba(74, 143, 180, 0.12);
}

.iframe-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  overflow: hidden;
  border-radius: 22px;
  background: #111;
}

.iframe-wrapper iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.video-meta {
  padding: 24px 4px 4px;
}

.video-meta h2 {
  margin: 0 0 18px;
  font-size: 24px;
  line-height: 1.5;
  color: #1f2d2a;
}

.meta-list {
  display: grid;
  gap: 10px;
}

.meta-list p {
  margin: 0;
  padding: 14px 16px;
  border-radius: 16px;
  background: #e5fff4;
  color: #4b635b;
}

.meta-list span {
  display: inline-block;
  min-width: 100px;
  color: #2d9c7a;
  font-weight: 800;
}

@media (max-width: 640px) {
  .detail-page {
    padding: 24px 16px;
  }

  .detail-header h1 {
    font-size: 28px;
  }

  .video-section {
    padding: 16px;
  }

  .video-meta h2 {
    font-size: 20px;
  }
}
</style>