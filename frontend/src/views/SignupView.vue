<template>
  <div>
    <form @submit.prevent="signUp">
    <div>
        <h2>기본 정보</h2>
        <p>*필수 입력</p>

      <div>
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username" />
      </div>
      <div>
        <label for="email">이메일</label>
        <input type="email" id="email" v-model.trim="email" />
      </div>
      <div>
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1" />
      </div>
      <div>
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model.trim="password2" />
      </div>
      <h2>추가 정보</h2>
      <div>
        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" v-model.trim="nickname" />
      </div>
      <div>
        <label for="birth">생년월일</label>
        <input type="date" id="birth" v-model.trim="birth" />
      </div>
      <div>
        <label>성별</label>
        <label><input type="radio" value="M" v-model="gender" /> 남성</label>
        <label><input type="radio" value="F" v-model="gender" /> 여성</label>
      </div>
    </div>
    <button type="submit">회원가입</button>
    <div>
        <p>이미 회원이신가요?</p>
        <router-link to="/login">로그인</router-link>
    </div>
    </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from "@/stores/userStore.js";

const userStore = useUserStore();
const username = ref('');
const email = ref('')
const password1 = ref('');
const password2 = ref('');
const nickname = ref('');
const birth = ref('');
const gender = ref('');

const signUp = () => {
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
  })
}


</script>

<style scoped>

</style>