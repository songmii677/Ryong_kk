import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/cards/'

export function getCards() {
  return axios.get(API_URL)
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