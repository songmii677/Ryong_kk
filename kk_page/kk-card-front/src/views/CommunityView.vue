<script setup>
import { ref,onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles } from '@/api/community'

const router = useRouter()

const articles = ref([])

onMounted(async()=>{

  const response =
    await getArticles()

  articles.value =
    response.data
})

function goDetail(id){

  router.push(
    `/community/${id}`
  )
}
</script>

<template>
<div class="community-page">

<div class="community-header">

<div>
<h1>커뮤니티</h1>
</div>

<button class="write-btn" @click="router.push('/community/create')">글쓰기</button>

</div>


<div
v-if="articles.length===0"
class="empty-card"
>

아직 작성된 글이 없어요

</div>


<div v-else class="article-list">

<div v-for="article in articles" :key="article.id"
  class="article-card"
  @click="goDetail(article.id)"
>
<h3 class="title">
{{ article.title }}
</h3>

<p class="writer">
{{ article.user }}
</p>

</div>

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
justify-content:space-between;
align-items:flex-start;
margin-bottom:28px;
}

.community-header h1{
margin:0;
font-size:30px;
}

.community-header p{
margin-top:8px;
font-size:14px;
color:#666;
line-height:1.5;
}

.write-btn{
  min-width: 90px;
  height: 40px;
  padding: 0 22px;

  border: none;
  border-radius: 14px;

  background: #48c78e;
  color: white;

  font-size: 15px;
  font-weight: 700;
  line-height: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  white-space: nowrap;
  cursor: pointer;

  box-shadow:
  0 6px 14px rgba(72,199,142,.25);
}

.write-btn:hover{
  opacity:.95;
}

.article-list{
display:flex;
flex-direction:column;
gap:18px;
}

.article-list{
display:flex;
flex-direction:column;
gap:12px;
}

.article-card{

background:white;
padding:18px 22px;
border-radius:18px;

display:flex;
justify-content:space-between;
align-items:center;

cursor:pointer;

box-shadow:
0 8px 18px
rgba(74,143,180,.12);

transition:.2s;
}

.article-card:hover{
transform:translateY(-2px);
}

.title{
margin:0;
font-size:16px;
font-weight:700;
}

.writer{
margin:0;
font-size:14px;
color:#777;
}

.article-card:hover{

transform:translateY(-4px);

}

.article-card h3{
margin:0;
font-size:18px;
}

.content{
margin-top:12px;
font-size:14px;
line-height:1.6;
color:#666;

display:-webkit-box;
-webkit-line-clamp:2;
-webkit-box-orient:vertical;
overflow:hidden;
}

.bottom{

margin-top:16px;
padding-top:12px;
border-top:1px solid #eee;

font-size:13px;
color:#999;
}

.empty-card{

background:white;
padding:40px;
border-radius:24px;

text-align:center;

box-shadow:
0 10px 24px
rgba(74,143,180,.14);

color:#777;
}

</style>