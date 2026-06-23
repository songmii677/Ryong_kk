<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import {
  getArticle,
  createComment,
  deleteArticle as deleteArticleApi,
  updateComment,
  deleteComment as deleteCommentApi,
  toggleArticleLike,
  toggleCommentLike,
} from '@/api/community'

import redHeart from '@/assets/red.png'
import whiteHeart from '@/assets/white.png'

const router = useRouter()
const route = useRoute()
const accountStore = useAccountStore()

const article = ref({})
const comments = ref([])
const commentInput = ref('')
const editingCommentId = ref(null)
const editText = ref('')

// 댓글 데이터의 좋아요 기본값 정리
const normalizeComments = (commentList = []) => {
  return commentList.map((comment) => ({
    ...comment,
    like_count: comment.like_count ?? 0,
    is_liked: comment.is_liked ?? false,
  }))
}

// 게시글 불러오기
onMounted(async () => {
  const res = await getArticle(route.params.id, accountStore.token)

  article.value = {
    ...res.data,
    like_count: res.data.like_count ?? 0,
    is_liked: res.data.is_liked ?? false,
  }

  comments.value = normalizeComments(res.data.comments)
})

// 작성자 체크
const isAuthor = computed(() => {
  return article.value.user === accountStore.username
})

// 댓글 작성
const submitComment = async () => {
  const content = commentInput.value.trim()

  if (!content) return

  await createComment(
    article.value.id,
    { content },
    accountStore.token,
  )

  commentInput.value = ''

  const res = await getArticle(route.params.id, accountStore.token)
  comments.value = normalizeComments(res.data.comments)
}

// 수정 페이지로 이동
const goEdit = () => {
  router.push(`/community/edit/${route.params.id}`)
}

// 게시글 삭제
const deleteArticle = async () => {
  const ok = confirm('정말 삭제하시겠습니까?')

  if (!ok) return

  await deleteArticleApi(
    route.params.id,
    accountStore.token,
  )

  router.push('/community')
}

// 댓글 수정 시작
const startEdit = (comment) => {
  editingCommentId.value = comment.id
  editText.value = comment.content
}

// 댓글 수정 취소
const cancelEdit = () => {
  editingCommentId.value = null
  editText.value = ''
}

// 댓글 수정 완료
const submitEdit = async (commentId) => {
  const content = editText.value.trim()

  if (!content) return

  await updateComment(
    commentId,
    { content },
    accountStore.token,
  )

  cancelEdit()

  const res = await getArticle(route.params.id, accountStore.token)
  comments.value = normalizeComments(res.data.comments)
}

// 댓글 삭제
const deleteComment = async (id) => {
  const ok = confirm('댓글을 삭제하시겠어요?')

  if (!ok) return

  await deleteCommentApi(
    id,
    accountStore.token,
  )

  const res = await getArticle(route.params.id, accountStore.token)
  comments.value = normalizeComments(res.data.comments)
}

// 게시글 좋아요
const toggleArticleLikeHandler = async () => {
  const res = await toggleArticleLike(
    article.value.id,
    accountStore.token,
  )

  article.value.like_count = res.data.like_count
  article.value.is_liked = res.data.liked
}

// 댓글 좋아요
const toggleCommentLikeHandler = async (comment) => {
  const res = await toggleCommentLike(
    comment.id,
    accountStore.token,
  )

  comment.like_count = res.data.like_count
  comment.is_liked = res.data.liked
}
</script>

<template>
  <div class="detail-page">
    <div class="thread-box">
      <!-- 게시글 -->
      <section class="article-box">
        <div class="article-top">
          <h2>{{ article.title }}</h2>
        </div>

        <!-- 게시글 작성자 -->
        <div class="author-row">
          <span class="author-label">작성자</span>
          <span class="author-divider">|</span>
          <span class="author-id">{{ article.user }}</span>
        </div>

        <!-- 게시글 수정·삭제 -->
        <div
          v-if="isAuthor"
          class="article-actions"
        >
          <button
            type="button"
            class="btn"
            @click="goEdit"
          >
            수정
          </button>

          <button
            type="button"
            class="btn delete"
            @click="deleteArticle"
          >
            삭제
          </button>
        </div>

        <!-- 게시글 내용 -->
        <p class="content">
          {{ article.content }}
        </p>

        <!-- 게시글 좋아요 -->
        <div class="article-bottom">
          <div class="like-box">
            <button
              type="button"
              class="like-button"
              :aria-label="article.is_liked ? '좋아요 취소' : '좋아요'"
              :aria-pressed="article.is_liked"
              @click="toggleArticleLikeHandler"
            >
              <img
                :src="article.is_liked ? redHeart : whiteHeart"
                alt=""
                class="like-heart-image"
                :class="{ 'is-unliked': !article.is_liked }"
              />
            </button>

            <span class="like-count">
              {{ article.like_count }}
            </span>
          </div>
        </div>
      </section>

      <!-- 댓글 영역 -->
      <section class="comment-box">
        <div class="comment-section-header">
          <h3>
            댓글
            <span>{{ comments.length }}</span>
          </h3>
        </div>

        <p
          v-if="comments.length === 0"
          class="empty"
        >
          아직 작성된 댓글이 없습니다.
        </p>

        <div
          v-for="(comment, index) in comments"
          :key="comment.id"
          class="comment"
          :class="{
            'is-last-comment': index === comments.length - 1,
          }"
        >
          <!-- 댓글 수정 상태 -->
          <div
            v-if="editingCommentId === comment.id"
            class="comment-edit-area"
          >
            <input
              v-model="editText"
              @keyup.enter="submitEdit(comment.id)"
            />

            <div class="comment-edit-buttons">
              <button
                type="button"
                @click="submitEdit(comment.id)"
              >
                저장
              </button>

              <button
                type="button"
                @click="cancelEdit"
              >
                취소
              </button>
            </div>
          </div>

          <!-- 댓글 일반 상태 -->
          <template v-else>
            <div class="comment-author-row">
              <span class="author-label">작성자</span>
              <span class="author-divider">|</span>
              <span class="author-id">{{ comment.user }}</span>
            </div>

            <p class="comment-content">
              {{ comment.content }}
            </p>
          </template>

          <div class="comment-footer">
            <!-- 댓글 작성자만 수정·삭제 가능 -->
            <div
              v-if="comment.user === accountStore.username"
              class="comment-owner-actions"
            >
              <button
                type="button"
                class="btn"
                @click="startEdit(comment)"
              >
                수정
              </button>

              <button
                type="button"
                class="btn delete"
                @click="deleteComment(comment.id)"
              >
                삭제
              </button>
            </div>

            <!-- 작성자가 아닐 때 좋아요를 오른쪽에 유지 -->
            <div
              v-else
              class="comment-action-spacer"
            ></div>

            <!-- 댓글 좋아요 -->
            <div class="like-box">
              <button
                type="button"
                class="like-button"
                :aria-label="comment.is_liked ? '좋아요 취소' : '좋아요'"
                :aria-pressed="comment.is_liked"
                @click="toggleCommentLikeHandler(comment)"
              >
                <img
                  :src="comment.is_liked ? redHeart : whiteHeart"
                  alt=""
                  class="like-heart-image"
                  :class="{ 'is-unliked': !comment.is_liked }"
                />
              </button>

              <span class="like-count">
                {{ comment.like_count }}
              </span>
            </div>
          </div>
        </div>

        <!-- 댓글 작성 -->
        <div class="comment-write">
          <input
            v-model="commentInput"
            placeholder="댓글을 입력하세요"
            @keyup.enter="submitComment"
          />

          <button
            type="button"
            @click="submitComment"
          >
            작성
          </button>
        </div>
      </section>
    </div>
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

.thread-box {
  overflow: hidden;
  border-radius: 18px;
  background-color: #ffffff;
  box-shadow: 0 8px 18px rgba(74, 143, 180, 0.12);
}

/* =========================
   게시글
========================= */

.article-box {
  padding: 22px;
  border-bottom: 1px solid #e5ece8;
  background-color: #ffffff;
}

.article-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.article-top h2 {
  margin: 0;
  color: #222;
  font-size: 20px;
  font-weight: 800;
  line-height: 1.4;
}

/* 작성자 표시 */
.author-row,
.comment-author-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  color: #7a8680;
  font-size: 12px;
}

.author-label {
  color: #8a948f;
  font-weight: 600;
}

.author-divider {
  color: #c3cbc7;
}

.author-id {
  color: #66716c;
}

/* 수정·삭제 */
.article-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn {
  padding: 0;
  border: none;
  background: none;
  color: #888;
  font-family: inherit;
  font-size: 13px;
  cursor: pointer;
  transition:
    color 0.2s,
    text-decoration-color 0.2s;
}

.btn:hover {
  color: #48c78e;
  text-decoration: underline;
}

.btn.delete:hover {
  color: #ff5c5c;
}

/* 게시글 내용 */
.content {
  margin-top: 14px;
  color: #444;
  font-size: 15px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 게시글 좋아요 위치 */
.article-bottom {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

/* =========================
   좋아요
========================= */

.like-box {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.like-button {
  all: unset;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 22px;
  height: 22px;

  cursor: pointer;
  box-sizing: border-box;
  transition: transform 0.2s;
}

.like-button:hover {
  transform: scale(1.08);
}

.like-button:focus-visible {
  border-radius: 5px;
  outline: 2px solid rgba(45, 156, 122, 0.25);
  outline-offset: 2px;
}

/* 좋아요 후 빨간색 하트 */
.like-heart-image {
  display: block;
  width: 18px;
  height: 18px;
  object-fit: contain;
}

/* 좋아요 전 흰색 하트만 조금 작게 */
.like-heart-image.is-unliked {
  width: 15px;
  height: 15px;
}

.like-count {
  min-width: 12px;
  color: #647069;
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
}

/* =========================
   댓글
========================= */

.comment-box {
  padding: 20px 22px 22px;
  background-color: #ffffff;
}

.comment-section-header {
  margin-bottom: 4px;
  padding-bottom: 14px;
  border-bottom: 1px solid #e8efeb;
}

.comment-section-header h3 {
  margin: 0;
  color: #222;
  font-size: 16px;
  font-weight: 800;
  text-align: left;
}

.comment-section-header h3 span {
  margin-left: 4px;
  color: #2d9c7a;
  font-size: 14px;
}

.empty {
  margin: 0;
  padding: 24px 0;
  color: #999;
  text-align: center;
}

/* 댓글 한 개 */
.comment {
  display: block;
  padding: 16px 0;
  border-bottom: 1px solid #edf2ef;
}

.comment.is-last-comment {
  border-bottom: none;
}

.comment-content {
  margin: 10px 0 12px;
  color: #303833;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 댓글 하단 */
.comment-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.comment-owner-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-action-spacer {
  flex: 1;
}

/* 댓글 수정 */
.comment-edit-area {
  margin-bottom: 12px;
}

.comment-edit-area input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-family: inherit;
  outline: none;
  box-sizing: border-box;
}

.comment-edit-area input:focus {
  border-color: #48c78e;
}

.comment-edit-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.comment-edit-buttons button {
  padding: 7px 11px;
  border: 1px solid #dce8e1;
  border-radius: 9px;
  background-color: #ffffff;
  color: #647069;
  font-family: inherit;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.comment-edit-buttons button:first-child {
  border-color: #48c78e;
  background-color: #48c78e;
  color: #ffffff;
}

/* =========================
   댓글 입력
========================= */

.comment-write {
  display: flex;
  gap: 10px;

  margin-top: 4px;
  padding-top: 16px;

  /* 마지막 댓글의 선은 없애고 이 선 하나만 표시 */
  border-top: 1px solid #e8efeb;
}

.comment-write input {
  flex: 1;
  min-width: 0;
  padding: 10px 12px;

  border: 1px solid #ddd;
  border-radius: 12px;

  font-family: inherit;
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

  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
}

.comment-write button:hover {
  opacity: 0.9;
}
</style>