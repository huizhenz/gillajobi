<template>
  <div class="login-page">
    <form class="login-form" @submit.prevent="logIn">
      <img src="@/assets/logo.png" alt="길라잡이 로고" class="login-logo" />
      <div class="input-group">
        <label for="id" class="sr-only">아이디</label>
        <input class="login-input" type="text" id="id" v-model.trim="username" placeholder="아이디" />
      </div>
      <div class="input-group">
        <label for="password" class="sr-only">비밀번호</label>
        <input class="login-input" type="password" id="password" v-model.trim="password" placeholder="비밀번호" />
      </div>
      <p v-if="errors.non_field_errors?.length" class="error">아이디 또는 비밀번호가 잘못되었습니다.</p>
      <button class="login-btn" type="submit">로그인</button>
      <div class="signup-link">
        <p>아직 회원이 아니세요?</p>
        <router-link :to="{ name: 'SignupView' }">회원가입</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from "@/stores/userStore.js";

const userStore = useUserStore();
const username = ref('');
const password = ref('');
const errors = ref({});

const logIn = () => {
  errors.value = {}
  const payload = {
    username: username.value,
    password: password.value
  }
  userStore.logIn(payload).catch((error) => {
    if (error.response?.data) {
      errors.value = error.response.data
    }
  })
}
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20%;
}

.login-form {
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 24px;
  box-sizing: border-box;
}

.login-logo {
  max-width: 100%;
  margin: 0 auto 40px;
  display: block;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
}

.input-group {
  display: flex;
  flex-direction: column;
}

.login-input {
  padding: 18px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  font-size: 0.95rem;
  outline: none;
  background: #fafafa;
  transition: border-color 0.2s;

  &::placeholder {
    color: #bbb;
  }

  &:focus {
    border-color: $teal;
    background: white;
  }
}

.login-btn {
  margin-top: 4px;
  padding: 18px;
  background: $teal;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: #239e8a;
  }
}

.signup-link {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  font-size: 0.9rem;
  color: #888;

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
  margin: 0;
  padding-left: 4px;
}
</style>