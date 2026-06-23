<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { deleteAccount as deleteAPI, changePassword as changePasswordAPI } from '@/api/accounts'

const router = useRouter()
const accountStore = useAccountStore()

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const passwordError = ref('')

// 비밀번호 변경
async function changePassword(){
  
  console.log('store token:', accountStore.token)
  console.log(
    'local token:',
    localStorage.getItem('token')
  )

  if(
    !currentPassword.value ||
    !newPassword.value ||
    !confirmPassword.value
  ){
    alert('모든 항목을 입력해주세요.')
    return
  }

  if(
    newPassword.value !== confirmPassword.value
  ){
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  try{

    await changePasswordAPI(
      {
        old_password: currentPassword.value,
        new_password1: newPassword.value,
        new_password2: confirmPassword.value
      },
      accountStore.token
    )

    alert('비밀번호가 변경되었습니다.')

    currentPassword.value=''
    newPassword.value=''
    confirmPassword.value=''

  }catch(err){

    console.log(err)

    console.log(err.response?.data)

    const message =
      Object.values(
        err.response?.data || {}
      )
      .flat()
      .join('\n')

    alert(message || '비밀번호 변경 실패')
  }
}

// 새 비번 확인
watch(
  [newPassword, confirmPassword],
  () => {

    if(
      confirmPassword.value &&
      newPassword.value !== confirmPassword.value
    ){
      passwordError.value =
      '비밀번호가 일치하지 않습니다.'
    }
    else{
      passwordError.value=''
    }

  }
)

// 계정 삭제(회원 탈퇴) 함수
async function deleteAccount(){

  const confirmDelete = confirm(
    '정말 회원 탈퇴하시겠습니까?\n탈퇴하면 되돌릴 수 없습니다.'
  )

  if(!confirmDelete) return

  try{

    await deleteAPI(
      accountStore.token
    )

    localStorage.clear()

    alert('회원 탈퇴가 완료되었습니다.')

    router.push('/')

  }catch(err){

    console.log(err)

    alert('회원 탈퇴 실패')
  }
}

</script>


<template>
<main class="mypage-page">

<section class="mypage-container">

<div class="profile-card">


<h1>
회원 정보 수정
</h1>

<p class="description">
비밀번호를 변경하거나 계정을 삭제할 수 있어요.
</p>

<form
class="password-form"
@submit.prevent="changePassword"
>

<div class="form-group">

<label>
현재 비밀번호
</label>

<input
type="password"
v-model="currentPassword"
placeholder="현재 비밀번호 입력"
/>

</div>


<div class="form-group">

<label>
새 비밀번호
</label>

<input
type="password"
v-model="newPassword"
placeholder="새 비밀번호 입력"
/>

</div>


<div class="form-group">

<label>
새 비밀번호 확인
</label>

<input
type="password"
v-model="confirmPassword"
placeholder="새 비밀번호 다시 입력"
/>

<p
v-if="passwordError"
class="password-error"
>
{{ passwordError }}
</p>


</div>

<button
type="submit"
class="save-btn"
>
비밀번호 변경
</button>

</form>

<!-- 회원 탈퇴 -->
<button
class="delete-btn"
@click="deleteAccount"
>
회원 탈퇴하기
</button>

<p class="description">
탈퇴 시 계정 데이터는 복구할 수 없어요.
</p>

</div>


</section>

</main>
</template>

<style scoped>

.mypage-page{
min-height:100vh;
padding:32px 20px;
background:#f7fcff;
}

.mypage-container{
max-width:430px;
margin:0 auto;
display:flex;
flex-direction:column;
gap:20px;
}

.profile-card,
.delete-card{
background:white;
padding:28px;
border-radius:28px;
box-shadow:0 10px 24px rgba(74,143,180,0.14);
}


h1{
margin:0;
font-size:23px;
color:#2d9c7a;
}

.description{
margin-top:12px;
margin-bottom:24px;
color:#666;
line-height:1.6;
}

.password-form{
display:flex;
flex-direction:column;
gap:18px;
}

.form-group{
display:flex;
flex-direction:column;
gap:8px;
}

.form-group label{
font-size:14px;
font-weight:700;
}

.form-group input{
height:54px;
border:2px solid #dcecf5;
border-radius:18px;
padding:0 16px;
font-size:15px;
outline:none;
}

.form-group input:focus{
border-color:#48c78e;
}

.save-btn{
height:56px;
border:none;
border-radius:999px;
background:#48c78e;
color:white;
font-size:17px;
font-weight:800;
cursor:pointer;
margin-top:10px;
}

.delete-card h3{
margin-top:0;
color:#d83b3b;
}

.delete-card p{
color:#666;
line-height:1.6;
margin-bottom:20px;
}

.delete-btn{
width:100%;
height:54px;
border:none;
border-radius:999px;
background:#ff5757;
color:white;
font-size:16px;
font-weight:800;
cursor:pointer;
margin-top:20px;
}

.delete-btn:hover{
opacity:.9;
}

.password-error{
font-size:14px;
color:#ff5757;
margin-top:6px;
font-weight:600;
}

</style>