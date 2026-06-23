import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/cards/'

export function getCards(params = {}) {
  return axios.get(API_URL, {params})
}

export function getCardDetail(cardId) {
  return axios.get(`${API_URL}${cardId}/`)
}

export function getRecommendCards(category, limit = 3) {
  return axios.get(`${API_URL}recommend/`, {
    params: {
      category,
      limit,
    },
  })
}

export const getAiRecommendCards = function (payload) {
  return axios.post('http://127.0.0.1:8000/api/cards/ai-recommend/', payload)
}