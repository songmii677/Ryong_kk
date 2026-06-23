import axios from 'axios'

const API_URL =
  'http://127.0.0.1:8000/community/'

// 게시글 전체 조회
export function getArticles() {
  return axios.get(
    `${API_URL}articles/`
  )
}

// 게시글 상세 조회
export function getArticle(articleId) {
  return axios.get(
    `${API_URL}articles/${articleId}/`
  )
}

// 게시글 작성
export function createArticle(
  articleData,
  token
) {
  return axios.post(
    `${API_URL}articles/`,
    articleData,
    {
      headers: {
        Authorization:
          `Token ${token}`
      }
    }
  )
}

// 게시글 수정
export function updateArticle(
  articleId,
  articleData,
  token
) {
  return axios.put(
    `${API_URL}articles/${articleId}/`,
    articleData,
    {
      headers: {
        Authorization:
          `Token ${token}`
      }
    }
  )
}


// 게시글 삭제
export function deleteArticle(
  articleId,
  token
) {
  return axios.delete(
    `${API_URL}articles/${articleId}/`,
    {
      headers: {
        Authorization:
          `Token ${token}`
      }
    }
  )
}

// 내가 작성한 글/댓글
export function getMyCommunity(token) {
  return axios.get(
    `${API_URL}my/`,
    {
      headers: {
        Authorization: `Token ${token}`
      }
    }
  )
}

// 게시글 좋아요
export function toggleArticleLike(articleId, token) {
  return axios.post(
    `${API_URL}articles/${articleId}/like/`,
    {},
    {
      headers: {
        Authorization: `Token ${token}`
      }
    }
  )
}


// 댓글 작성
export function createComment(
  articleId,
  commentData,
  token
) {
  return axios.post(
    `${API_URL}articles/${articleId}/comments/`,
    commentData,
    {
      headers: {
        Authorization:
          `Token ${token}`
      }
    }
  )
}

// 댓글 삭제
export function deleteComment(
  commentId,
  token
) {
  return axios.delete(
    `${API_URL}comments/${commentId}/`,
    {
      headers: {
        Authorization:
          `Token ${token}`
      }
    }
  )
}

//댓글 수정
export const updateComment = (id, data, token) => {
  return axios.put(
    `${API_URL}comments/${id}/`,
    data,
    {
      headers: {
        Authorization: `Token ${token}`
      }
    }
  )
}

// 댓글 좋아요
export function toggleCommentLike(commentId, token) {
  return axios.post(
    `${API_URL}comments/${commentId}/like/`,
    {},
    {
      headers: {
        Authorization: `Token ${token}`
      }
    }
  )
}