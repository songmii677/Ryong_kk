<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts';

const router = useRouter()
const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

const login = async () => {
    if (!username.value.trim() || !password.value.trim()) {
        alert('아이디와 비밀번호를 입력해주세요.')
        return
    }
    const payload = {
        username: username.value,
        password: password.value
    }
    try {
        await accountStore.login(payload)
        alert('로그인 되었습니다.')
        router.push('/')
    } catch (error) {
        console.error('로그인 실패:', error)
        alert('아이디 또는 비밀번호를 확인해주세요')
    }
}
</script>


<template>
  <main class="login-page">
    <section class="login-card">
      <p class="badge">룡크크 로그인</p>

      <h1>로그인</h1>

      <p class="description">
        로그인하면 관심 카드와 추천 결과를 저장할 수 있어요.
      </p>

      <form class="login-form" @submit.prevent="login">
        <div class="form-group">
          <label for="username">아이디</label>
          <input
            type="text"
            id="username"
            v-model.trim="username"
            placeholder="아이디를 입력해주세요"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            type="password"
            id="password"
            v-model.trim="password"
            placeholder="비밀번호를 입력해주세요"
          />
        </div>

        <button type="submit" class="login-button">
          로그인
        </button>
      </form>

      <p class="signup-text">
        아직 계정이 없나요?
        <RouterLink to="/signup">회원가입하기</RouterLink>
      </p>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background-color: #f7fbf6;
}

.login-card {
  width: 100%;
  max-width: 430px;
  padding: 36px 32px;
  border-radius: 28px;
  background-color: #ffffff;
  box-shadow: 0 10px 28px rgba(47, 158, 109, 0.12);
  text-align: center;
}

.badge {
  display: inline-block;
  margin-bottom: 14px;
  padding: 7px 14px;
  border-radius: 999px;
  background-color: #e2f7ea;
  color: #139b67;
  font-size: 13px;
  font-weight: 700;
}

.login-card h1 {
  margin: 0;
  font-size: 28px;
  color: #222;
}

.description {
  margin: 14px 0 28px;
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #333;
  font-size: 14px;
  font-weight: 700;
}

.form-group input {
  padding: 14px 15px;
  border: 1px solid #dfe8e2;
  border-radius: 14px;
  font-size: 15px;
  outline: none;
}

.form-group input:focus {
  border-color: #139b67;
  box-shadow: 0 0 0 3px rgba(19, 155, 103, 0.12);
}

.login-button {
  margin-top: 8px;
  padding: 15px;
  border: none;
  border-radius: 999px;
  background-color: #139b67;
  color: white;
  font-size: 16px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.2s;
}

.login-button:hover {
  background-color: #0f8056;
  transform: translateY(-2px);
}

.signup-text {
  margin-top: 22px;
  color: #666;
  font-size: 14px;
}

.signup-text a {
  margin-left: 6px;
  color: #139b67;
  font-weight: 700;
  text-decoration: none;
}
</style>