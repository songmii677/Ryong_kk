import axios from 'axios'

const API_URL =
'http://127.0.0.1:8000/accounts/'

export function deleteAccount(token){
  return axios.delete(
    `${API_URL}delete-account/`,
    {
      headers:{
        Authorization:
        `Token ${token}`
      }
    }
  )
}