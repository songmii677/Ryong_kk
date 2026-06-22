<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const keyword = ref('')
const videos = ref([])
const isLoading = ref(false)
const searched = ref(false)
const errorMessage = ref('')

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

const searchVideos = async function () {
  if (!keyword.value.trim()) {
    alert('검색어를 입력해주세요.')
    return
  }

  isLoading.value = true
  searched.value = true
  errorMessage.value = ''
  videos.value = []

  try {
    const response = await axios({
      method: 'get',
      url: 'https://www.googleapis.com/youtube/v3/search',
      params: {
        key: API_KEY,
        part: 'snippet',
        q: keyword.value,
        type: 'video',
        maxResults: 12,
        order: 'relevance',
      },
    })

    videos.value = response.data.items
  } catch (error) {
    console.log('유튜브 검색 실패:', error)
    errorMessage.value = '영상을 불러오지 못했습니다. API 키 또는 요청 제한을 확인해주세요.'
  } finally {
    isLoading.value = false
  }
}

const goDetail = function (video) {
  router.push({
    name: 'youtube-detail',
    params: {
      videoId: video.id.videoId,
    },
    query: {
      title: video.snippet.title,
      channelTitle: video.snippet.channelTitle,
      publishedAt: video.snippet.publishedAt,
    },
  })
}
</script>

<template>
  <main class="youtube-page">
    <section class="hero-section">
      <p class="sub-title">RyongKK Financial Contents</p>
      <h1>룡크크 금융 콘텐츠 검색</h1>
      <p class="description">
        카드 추천, 혜택 비교, 재테크, 소비 습관과 관련된 유튜브 영상을 검색해보세요.
      </p>
    </section>

    <section class="search-section">
      <div class="search-box">
        <input
          v-model.trim="keyword"
          type="text"
          placeholder="예: 신용카드 추천, 체크카드 혜택, 사회초년생 재테크"
          @keyup.enter="searchVideos"
        />
        <button @click="searchVideos">검색</button>
      </div>

      <div class="quick-keywords">
        <button @click="keyword = '신용카드 추천'; searchVideos()">신용카드 추천</button>
        <button @click="keyword = '체크카드 혜택'; searchVideos()">체크카드 혜택</button>
        <button @click="keyword = '사회초년생 재테크'; searchVideos()">사회초년생 재테크</button>
        <button @click="keyword = '카드 포인트 활용'; searchVideos()">카드 포인트 활용</button>
      </div>
    </section>

    <section class="result-section">
      <div v-if="isLoading" class="message">
        영상을 검색하는 중입니다...
      </div>

      <div v-else-if="errorMessage" class="message error">
        {{ errorMessage }}
      </div>

      <div v-else-if="searched && videos.length === 0" class="message">
        검색 결과가 없습니다. 다른 키워드로 검색해보세요.
      </div>

      <div v-else class="video-grid">
        <article
          v-for="video in videos"
          :key="video.id.videoId"
          class="video-card"
          @click="goDetail(video)"
        >
          <img
            :src="video.snippet.thumbnails.medium.url"
            :alt="video.snippet.title"
            class="thumbnail"
          />

          <div class="video-info">
            <h3>{{ video.snippet.title }}</h3>
            <p class="channel">{{ video.snippet.channelTitle }}</p>
            <p class="date">
              {{ video.snippet.publishedAt.slice(0, 10) }}
            </p>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>
<style scoped>
.youtube-page {
  min-height: 100vh;
  padding: 40px 24px;
  background: linear-gradient(180deg, #dff5ff 0%, #f7fcff 100%);
  color: #1f2d2a;
}

.hero-section {
  max-width: 1000px;
  margin: 0 auto 32px;
  padding: 36px 32px;
  border-radius: 28px;
  background: linear-gradient(135deg, #b8f7a8, #48c78e);
  color: white;
  box-shadow: 0 12px 28px rgba(72, 199, 142, 0.28);
}

.sub-title {
  margin-bottom: 8px;
  font-weight: 700;
  letter-spacing: 0.08em;
  font-size: 14px;
}

.hero-section h1 {
  margin: 0 0 12px;
  font-size: 36px;
  font-weight: 800;
}

.description {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
}

.search-section {
  max-width: 1000px;
  margin: 0 auto 32px;
}

.search-box {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 20px;
  background: white;
  box-shadow: 0 8px 24px rgba(74, 143, 180, 0.12);
}

.search-box input {
  flex: 1;
  padding: 14px 18px;
  border: 1px solid #cdeee2;
  border-radius: 14px;
  font-size: 15px;
  outline: none;
}

.search-box input:focus {
  border-color: #48c78e;
  box-shadow: 0 0 0 3px rgba(72, 199, 142, 0.16);
}

.search-box button {
  padding: 0 28px;
  border: none;
  border-radius: 14px;
  background: #48c78e;
  color: white;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(72, 199, 142, 0.28);
}

.search-box button:hover {
  background: #2d9c7a;
}

.quick-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}

.quick-keywords button {
  padding: 10px 14px;
  border: 1px solid #b8efd8;
  border-radius: 999px;
  background: #ffffff;
  color: #2d9c7a;
  font-weight: 700;
  cursor: pointer;
}

.quick-keywords button:hover {
  background: #e5fff4;
  border-color: #48c78e;
}

.result-section {
  max-width: 1000px;
  margin: 0 auto;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.video-card {
  overflow: hidden;
  border-radius: 20px;
  background: white;
  box-shadow: 0 8px 24px rgba(74, 143, 180, 0.12);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.video-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 32px rgba(72, 199, 142, 0.22);
}

.thumbnail {
  width: 100%;
  height: 170px;
  object-fit: cover;
}

.video-info {
  padding: 16px;
}

.video-info h3 {
  display: -webkit-box;
  margin: 0 0 10px;
  font-size: 15px;
  line-height: 1.4;
  color: #1f2d2a;

  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;

  overflow: hidden;
}

.channel {
  margin: 0 0 6px;
  color: #2d9c7a;
  font-weight: 800;
  font-size: 14px;
}

.date {
  margin: 0;
  color: #7b8f88;
  font-size: 13px;
}

.message {
  padding: 40px 20px;
  text-align: center;
  border-radius: 20px;
  background: white;
  color: #4b635b;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(74, 143, 180, 0.1);
}

.error {
  color: #d93025;
}

@media (max-width: 900px) {
  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .youtube-page {
    padding: 24px 16px;
  }

  .hero-section h1 {
    font-size: 28px;
  }

  .search-box {
    flex-direction: column;
  }

  .search-box button {
    padding: 14px;
  }

  .video-grid {
    grid-template-columns: 1fr;
  }
}
</style>