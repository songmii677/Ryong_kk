<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { getArticle, createComment, deleteArticle as deleteArticleApi } from '@/api/community'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const article = ref({})
const comments = ref([])
const commentInput = ref('')

// 게시글 불러오기
onMounted(async () => {
  const res = await getArticle(route.params.id)

  article.value = res.data
  comments.value = res.data.comments || []
})

// 작성자 체크
const isAuthor = computed(() => {
  return article.value.user === accountStore.username
})

// 댓글 작성
const submitComment = async () => {
  if (!commentInput.value) return
  await createComment(
    article.value.id,
    { content: commentInput.value },
    accountStore.token
  )
  commentInput.value = ''
  const res = await getArticle(route.params.id)
  comments.value = res.data.comments || []
}

// 수정 페이지로 이동
const goEdit = () => {
  router.push(`/community/edit/${route.params.id}`)
}

// 게시글 삭제
const deleteArticle = async () => {
  const ok = confirm('정말 삭제하시겠습니까?')
  if (!ok) return

  await deleteArticleApi(route.params.id, accountStore.token)

  // 삭제 후 목록으로 이동
  router.push('/community')
}

</script>

<template>
  <div class="detail-page">

    <!-- 게시글 -->
    <section class="article-box">
      <div class="article-header">
        <h2>{{ article.title }}</h2>
        <p class="writer">{{ article.user }}</p>
        <!-- 작성자만 수정/삭제 -->
        <div v-if="isAuthor" class="btn-group">
          <button class="btn" @click="goEdit">수정</button>
          <button class="btn delete" @click="deleteArticle">삭제</button>
        </div>
      </div>

      <p class="content">
        {{ article.content }}
      </p>

    </section>

    <!-- 댓글 영역 -->
    <section class="comment-box">
      <div v-if="comments.length === 0" class="empty">
        댓글이 없습니다
      </div>

      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment"
      >
        <p class="comment-content">
          {{ comment.content }}
        </p>

        <p class="comment-user">
          {{ comment.user }}
        </p>
      </div>

      <hr />

      <!-- 댓글 작성 -->
      <div class="comment-write">
        <input
          v-model="commentInput"
          placeholder="댓글을 입력하세요"
        />

        <button @click="submitComment">
          작성
        </button>
      </div>

    </section>

  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  max-width: 430px;
  margin: 0 auto;
  padding: 24px;
  background: #f7fcff;
}

/* ===== 게시글 카드 ===== */
.article-box {
  background: white;
  padding: 22px;
  border-radius: 18px;

  box-shadow: 0 8px 18px rgba(74, 143, 180, 0.12);
  margin-bottom: 18px;
}

/* 제목 + 유저 영역 */
.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.article-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: #222;
}

/* 작성자 */
.writer {
  font-size: 13px;
  color: #777;
  margin-top: 6px;
}

.btn-group {
  margin-top: 8px;
  display: flex;
  gap: 12px;
}


.btn {
  padding: 0;
  border: none;
  background: none;

  font-size: 13px;
  color: #888;

  cursor: pointer;
  transition: 0.2s;
}

.btn:hover {
  color: #48c78e;
  text-decoration: underline;
}

.btn.delete:hover {
  color: #ff5c5c;
}

/* ===== 내용 ===== */
.content {
  margin-top: 14px;
  font-size: 15px;
  line-height: 1.7;
  color: #444;
}

/* ===== 댓글 박스 ===== */
.comment-box {
  background: white;
  padding: 20px;
  border-radius: 18px;

  box-shadow: 0 8px 18px rgba(74, 143, 180, 0.12);
}

.comment-box h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 800;
  text-align: center;
}

/* 댓글 없음 */
.empty {
  color: #999;
  padding: 12px 0;
  text-align: center;
}

/* 댓글 */
.comment {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.comment:last-child {
  border-bottom: none;
}

.comment-content {
  font-size: 14px;
  font-weight: 600;
}

.comment-user {
  font-size: 12px;
  color: #888;
}

/* ===== 댓글 입력 ===== */
.comment-write {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}

.comment-write input {
  flex: 1;
  padding: 10px 12px;

  border: 1px solid #ddd;
  border-radius: 12px;

  outline: none;
}

.comment-write input:focus {
  border-color: #48c78e;
}

.comment-write button {
  padding: 10px 14px;

  border: none;
  border-radius: 12px;

  background: #48c78e;
  color: white;

  font-weight: 700;
  cursor: pointer;
}

.comment-write button:hover {
  opacity: 0.9;
}
</style>