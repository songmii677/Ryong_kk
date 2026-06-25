import axios from 'axios'


const BASE_URL =
  'http://127.0.0.1:8000/api/deposits'


function getAuthHeaders(token) {
  if (!token) {
    return {}
  }

  return {
    Authorization: `Token ${token}`,
  }
}


export function getFinancialProducts(token) {
  return axios.get(
    `${BASE_URL}/`,
    {
      headers: getAuthHeaders(token),
    },
  )
}


export function getFinancialProductDetail(
  productId,
  token,
) {
  return axios.get(
    `${BASE_URL}/${productId}/`,
    {
      headers: getAuthHeaders(token),
    },
  )
}


export function toggleFinancialFavorite(
  productId,
  token,
) {
  return axios.post(
    `${BASE_URL}/${productId}/favorite/`,
    {},
    {
      headers: getAuthHeaders(token),
    },
  )
}


export function getFinancialFavorites(token) {
  return axios.get(
    `${BASE_URL}/favorites/`,
    {
      headers: getAuthHeaders(token),
    },
  )
}