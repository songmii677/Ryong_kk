<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { createArticle } from '@/api/community'

const router = useRouter()
const accountStore = useAccountStore()

const title = ref('')
const content = ref('')

const submitArticle = async () => {
  try {
    const articleData = {
      title: title.value,
      content: content.value
    }
    await createArticle(articleData, accountStore.token)
    alert('게시글 작성 완료!')
    router.push('/community')
  } catch (error) {
    console.error(error)
    alert('작성 실패')
  }
}
</script>

<template>
<div class="community-page">

<div class="community-header">

<button
class="back-btn"
@click="router.back()"
>
‹
</button>

<h2>글쓰기</h2>

</div>

<div class="write-card">

<input
v-model="title"
type="text"
placeholder="제목을 입력하세요"
class="title-input"
/>

<textarea
v-model="content"
placeholder="내용을 입력하세요"
class="content-input"
/>

<button
class="submit-btn"
@click="submitArticle"
>
작성하기
</button>

</div>

</div>
</template>

<style scoped>

.community-page{
min-height:100vh;
max-width:430px;
margin:0 auto;
padding:24px;
background:#f7fcff;
}

.community-header{
display:flex;
align-items:center;
gap:16px;
margin-bottom:24px;
}

.community-header h2{
margin:0;
font-size:28px;
}

.write-card{
background:white;
padding:24px;
border-radius:28px;
box-shadow:0 10px 24px rgba(74,143,180,.14);
display:flex;
flex-direction:column;
gap:18px;
}

.title-input{
height:56px;
border:2px solid #dcecf5;
border-radius:18px;
padding:0 18px;
font-size:16px;
outline:none;
}

.title-input:focus{
border-color:#48c78e;
}

.content-input{
min-height:240px;
resize:none;
border:2px solid #dcecf5;
border-radius:18px;
padding:18px;
font-size:15px;
outline:none;
font-family:inherit;
}

.content-input:focus{
border-color:#48c78e;
}

.submit-btn{
height:56px;
border:none;
border-radius:999px;
background:#48c78e;
color:white;
font-size:18px;
font-weight:900;
cursor:pointer;
margin-top:10px;
box-shadow:0 8px 18px rgba(72,199,142,.35);
}

</style>
