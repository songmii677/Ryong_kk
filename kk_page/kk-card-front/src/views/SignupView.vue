<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const accountStore = useAccountStore()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const passwordError = ref('')

function validatePassword() {
  const password = password1.value
  const userId = username.value.trim()

  const hasLetter = /[A-Za-z]/.test(password)
  const hasNumber = /[0-9]/.test(password)
  const hasSpecial = /[!@#$%^&*(),.?":{}|<>_\-+=\/\\[\]]/.test(password)

  if (password.length < 8) {
    passwordError.value = '비밀번호는 8자 이상이어야 합니다.'
    return false
  }

  if (!hasLetter || !hasNumber || !hasSpecial) {
    passwordError.value = '비밀번호는 영문, 숫자, 특수문자를 모두 포함해야 합니다.'
    return false
  }

  if (
    password.includes('1234') ||
    password.includes('0000') ||
    password.includes('1111') ||
    password.toLowerCase().includes('password') ||
    password.toLowerCase().includes('qwer') ||
    password.toLowerCase().includes('abcd')
  ) {
    passwordError.value = '1234, password, qwer처럼 쉽게 추측 가능한 비밀번호는 사용할 수 없습니다.'
    return false
  }

  if (/(.)\1{3,}/.test(password)) {
    passwordError.value = '같은 문자가 4번 이상 반복되는 비밀번호는 사용할 수 없습니다.'
    return false
  }

  if (userId.length >= 3 && password.toLowerCase().includes(userId.toLowerCase())) {
    passwordError.value = '아이디와 너무 비슷한 비밀번호는 사용할 수 없습니다.'
    return false
  }

  if (password1.value !== password2.value) {
    passwordError.value = '비밀번호가 일치하지 않습니다.'
    return false
  }

  passwordError.value = ''
  return true
}

function getErrorMessage(errorData) {
  if (!errorData) {
    return '회원가입에 실패했습니다. 입력 정보를 확인해주세요.'
  }

  if (typeof errorData === 'string') {
    return errorData
  }

  if (Array.isArray(errorData)) {
    return errorData.join('\n')
  }

  if (typeof errorData === 'object') {
    return Object.values(errorData).flat().join('\n')
  }

  return '회원가입에 실패했습니다. 입력 정보를 확인해주세요.'
}

const signup = async () => {
  if (!username.value.trim()) {
    alert('아이디를 입력해주세요.')
    return
  }

  if (!password1.value || !password2.value) {
    passwordError.value = '비밀번호를 입력해주세요.'
    return
  }

  if (!validatePassword()) {
    return
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }

  try {
    await accountStore.signup(payload)
    alert('회원가입이 완료되었습니다.')
    router.push('/')
  } catch (error) {
    console.error('회원가입 실패:', error)

    const message = getErrorMessage(error.response?.data)
    passwordError.value = message
  }
}
</script>

<template>
  <main class="signup-page">
    <section class="signup-card">
      <!-- <p class="badge">룡크크 시작하기</p> -->

      <h1>회원가입</h1>

      <p class="description">
        계정을 만들면 관심 카드와 추천 결과를 저장할 수 있어요.
      </p>

      <form class="signup-form" @submit.prevent="signup">
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
          <label for="password1">비밀번호</label>
          <input
            type="password"
            id="password1"
            v-model="password1"
            placeholder="비밀번호를 입력해주세요"
          />

          <ul class="password-guide">
            <li>비밀번호는 8자 이상이어야 합니다.</li>
            <li>영문, 숫자, 특수문자를 모두 포함해야 합니다.</li>
            <li>1234, password, qwer처럼 쉬운 비밀번호는 사용할 수 없습니다.</li>
            <li>아이디와 너무 비슷한 비밀번호는 사용할 수 없습니다.</li>
          </ul>
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input
            type="password"
            id="password2"
            v-model="password2"
            placeholder="비밀번호를 다시 입력해주세요"
          />

          <p v-if="passwordError" class="password-error">
            {{ passwordError }}
          </p>
        </div>

        <button type="submit" class="signup-button">
          회원가입
        </button>
      </form>

      <p class="login-text">
        이미 계정이 있나요?
        <RouterLink to="/login">로그인하기</RouterLink>
      </p>
    </section>
  </main>
</template>

<style scoped>
.signup-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background-color: #f7fbf6;
}

.signup-card {
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

.signup-card h1 {
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

.signup-form {
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

.password-guide {
  margin: 4px 0 0;
  padding: 12px 14px 12px 28px;
  border-radius: 14px;
  background: #e5fff4;
  color: #3f6257;
  font-size: 12px;
  line-height: 1.6;
}

.password-guide li {
  margin-bottom: 3px;
}

.password-error {
  margin: 4px 0 0;
  padding: 10px 12px;
  border-radius: 12px;
  background: #fff0f0;
  color: #d93025;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.5;
  white-space: pre-line;
}

.signup-button {
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

.signup-button:hover {
  background-color: #0f8056;
  transform: translateY(-2px);
}

.login-text {
  margin-top: 22px;
  color: #666;
  font-size: 14px;
}

.login-text a {
  margin-left: 6px;
  color: #139b67;
  font-weight: 700;
  text-decoration: none;
}
</style>