<template>
  <div class="signup-page">
    <form class="signup-form" @submit.prevent="signUp">

      <div class="section">
        <div class="section-header">
          <h2 class="section-title">기본 정보</h2>
          <p class="required-note">*필수 입력</p>
        </div>

        <div class="field">
          <label for="username" class="sr-only">아이디</label>
          <input class="form-input" type="text" id="username" v-model.trim="username" placeholder="아이디" />
          <p v-for="msg in errors.username" :key="msg" class="error">{{ msg }}</p>
        </div>
        <div class="field">
          <label for="email" class="sr-only">이메일</label>
          <input class="form-input" type="email" id="email" v-model.trim="email" placeholder="이메일" />
          <p v-for="msg in errors.email" :key="msg" class="error">{{ msg }}</p>
        </div>
        <div class="field">
          <label for="password1" class="sr-only">비밀번호</label>
          <input class="form-input" type="password" id="password1" v-model.trim="password1" placeholder="비밀번호 (8~16자의 영문, 숫자, 특수기호)" />
          <p v-for="msg in errors.password1" :key="msg" class="error">{{ msg }}</p>
        </div>
        <div class="field">
          <label for="password2" class="sr-only">비밀번호 확인</label>
          <input class="form-input" type="password" id="password2" v-model.trim="password2" placeholder="비밀번호 확인" />
          <p v-for="msg in errors.password2" :key="msg" class="error">{{ msg }}</p>
        </div>
      </div>

      <div class="section">
        <div class="section-header">
          <h2 class="section-title">추가 정보</h2>
        </div>

        <div class="field">
          <label for="nickname" class="sr-only">닉네임</label>
          <input class="form-input" type="text" id="nickname" v-model.trim="nickname" placeholder="닉네임" />
          <p v-for="msg in errors.nickname" :key="msg" class="error">{{ msg }}</p>
          <p>회원가입 이후 수정 불가능</p>
        </div>
        <div class="field">
          <label for="birth" class="field-label">생년월일</label>
          <input class="form-input" :class="{ 'has-value': birth }" type="date" id="birth" v-model.trim="birth" />
        </div>
        <div class="field gender-field">
          <span class="field-label">성별</span>
          <div class="gender-options">
            <label class="gender-option"><input type="radio" value="M" v-model="gender" /> 남성</label>
            <label class="gender-option"><input type="radio" value="F" v-model="gender" /> 여성</label>
          </div>
          <p v-for="msg in errors.gender" :key="msg" class="error">{{ msg }}</p>
        </div>
      </div>

      <button class="signup-btn" type="submit">회원가입</button>
      <div class="login-link">
        <p>이미 회원이신가요?</p>
        <router-link :to="{ name: 'LoginView' }">로그인</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useUserStore } from "@/stores/userStore.js";

const userStore = useUserStore();
const username = ref('');
const email = ref('')
const password1 = ref('');
const password2 = ref('');
const nickname = ref('');
const birth = ref('');
const gender = ref('');
const errors = ref({});

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

watch(username, (val) => {
  errors.value.username = val ? [] : ['아이디를 입력해주세요.']
})

watch(email, (val) => {
  if (!val) errors.value.email = ['이메일을 입력해주세요.']
  else if (!emailRegex.test(val)) errors.value.email = ['올바른 이메일 형식이 아닙니다.']
  else errors.value.email = []
})

watch(password1, (val) => {
  if (!val) errors.value.password1 = ['비밀번호를 입력해주세요.']
  else if (val.length < 8) errors.value.password1 = ['비밀번호는 최소 8자 이상이어야 합니다.']
  else errors.value.password1 = []
  if (password2.value) {
    errors.value.password2 = val === password2.value ? [] : ['비밀번호가 일치하지 않습니다.']
  }
})

watch(password2, (val) => {
  if (!val) errors.value.password2 = ['비밀번호 확인을 입력해주세요.']
  else errors.value.password2 = val === password1.value ? [] : ['비밀번호가 일치하지 않습니다.']
})

watch(nickname, (val) => {
  errors.value.nickname = val ? [] : ['닉네임을 입력해주세요.']
})

const signUp = () => {
  const clientErrors = {}
  if (!username.value) clientErrors.username = ['아이디를 입력해주세요.']
  if (!email.value) clientErrors.email = ['이메일을 입력해주세요.']
  else if (!emailRegex.test(email.value)) clientErrors.email = ['올바른 이메일 형식이 아닙니다.']
  if (!password1.value) clientErrors.password1 = ['비밀번호를 입력해주세요.']
  if (!password2.value) clientErrors.password2 = ['비밀번호 확인을 입력해주세요.']
  else if (password1.value !== password2.value) clientErrors.password2 = ['비밀번호가 일치하지 않습니다.']
  if (!nickname.value) clientErrors.nickname = ['닉네임을 입력해주세요.']
  if (!gender.value) clientErrors.gender = ['성별을 선택해주세요.']
  if (Object.keys(clientErrors).length > 0) {
    errors.value = clientErrors
    return
  }
  errors.value = {}
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    birth: birth.value,
    gender: gender.value
  }
  userStore.signUp(payload).then(() => {
    username.value = ''
    email.value = ''
    password1.value = ''
    password2.value = ''
    nickname.value = ''
    birth.value = ''
    gender.value = ''
  }).catch((error) => {
    if (error.response?.data) {
      errors.value = error.response.data
    }
  })
}


</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.signup-page {
  display: flex;
  justify-content: center;
  padding-top: 10vh;
  padding-bottom: 10vh;
}

.signup-form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

.section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a1a1a;
}

.required-note {
  font-size: 0.8rem;
  color: $teal;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-label {
  font-size: 0.90rem;
  color: #666;
  font-weight: 500;
}

.form-input {
  padding: 14px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 0.9rem;
  outline: none;
  background: #fafafa;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;

  &::placeholder {
    color: #bbb;
  }

  &:focus {
    border-color: $teal;
    background: white;
  }
}

.gender-field {
  flex-direction: row;
  align-items: center;
  gap: 16px;
}

.gender-options {
  display: flex;
  gap: 16px;
}

.gender-option {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #444;
  cursor: pointer;

  input[type="radio"] {
    accent-color: $teal;
    width: 16px;
    height: 16px;
  }
}

.signup-btn {
  padding: 16px;
  background: $teal;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: #239e8a;
  }
}

.login-link {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #888;
  margin-top: -16px;

  a {
    color: $teal;
    font-weight: 600;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.error {
  color: #e53935;
  font-size: 0.82rem;
  padding-left: 2px;
}
</style>