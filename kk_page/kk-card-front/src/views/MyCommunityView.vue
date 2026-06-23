<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { getMyCommunity } from '@/api/community'

const router = useRouter()
const accountStore = useAccountStore()

const articles = ref([])
const comments = ref([])

const username = computed(() => {
  return (
    accountStore.user?.username ||
    accountStore.username ||
    localStorage.getItem('username')
  )
})

onMounted(async () => {
  try {
    const res = await getMyCommunity(
      accountStore.token
    )

    articles.value = res.data.articles.sort(
      (a,b)=> b.id - a.id
    )

    comments.value = res.data.comments.sort(
      (a,b)=> b.id - a.id
    )

  } catch(err){
    console.log(err)
  }
})


function goArticle(id){
  router.push(`/community/${id}`)
}
</script>

<template>
<main class="mypage-page">

<section class="mypage-container">

<div class="mypage-profile-card"></div>


<!-- 작성 글 -->

<section class="activity-card">

<h2>
{{ username }}님이 작성한 글
</h2>

<div
v-if="articles.length"
>

<div
v-for="article in articles"
:key="article.id"
class="activity-item"
@click="goArticle(article.id)"
>

<p class="activity-title">
{{ article.title }}
</p>

</div>

</div>

<p
v-else
class="empty-text"
>
작성한 글이 없습니다.
</p>

</section>



<!-- 작성 댓글 -->

<!-- 작성 댓글 -->
<section class="activity-card">

<h2>
{{ username }}님이 작성한 댓글
</h2>

<div v-if="comments.length">

<div
v-for="comment in comments"
:key="comment.id"
class="comment-wrap"
>

<!-- 게시글 제목만 박스 -->
<div
class="activity-item"
@click="goArticle(comment.article_id)"
>

<p class="comment-article">
{{ comment.article_title }}
</p>

</div>

<!-- 댓글 내용 -->
<p class="comment-content">
ㄴ {{ comment.content }}
</p>

</div>

</div>

<p
v-else
class="empty-text"
>
작성한 댓글이 없습니다.
</p>

</section>

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

.activity-card{
background:white;
padding:22px;
border-radius:26px;
box-shadow:0 10px 24px rgba(74,143,180,0.14);
}

.activity-card h2{
font-size:18px;
margin-bottom:18px;
color:#2d9c7a;
}

.activity-item{
padding:14px;
margin-bottom:12px;
border-radius:16px;
background:#f7fcff;
cursor:pointer;
transition:.2s;
}

.activity-item:hover{
background:#f0fff8;
transform:translateY(-2px);
}

.activity-title{
font-size:14px;
font-weight:800;
color:#666;
margin:0;
}

.comment-article{
font-size:14px;
font-weight:800;
color:#2d9c7a;
margin-bottom:8px;
}

.comment-content{
font-size:14px;
color:#666;
margin:0;
}

.empty-text{
text-align:center;
color:#888;
padding:20px;
}

.comment-wrap{
margin-bottom:18px;
}

.comment-article{
font-size:14px;
font-weight:800;
color:#2d9c7a;
margin:0;
}

.comment-content{
padding-left:14px;
margin-top:8px;
font-size:14px;
color:#666;
line-height:1.5;
}

</style>