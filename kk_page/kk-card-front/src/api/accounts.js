import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/accounts/'

// 회원 탈퇴
export function deleteAccount(token){

  return axios.delete(
    `${API_URL}delete/`,
    {
      headers:{
        Authorization:`Token ${token}`
      }
    }
  )
}

// 비밀번호 변경
export function changePassword(data, token){

  return axios.post(
    `${API_URL}password/change/`,
    data,
    {
      headers:{
        Authorization:`Token ${token}`
      }
    }
  )
}