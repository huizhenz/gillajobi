<template>
  <div>
    <form @submit.prevent="logIn">
      <div>
        <label for="id">아이디</label>
        <input type="text" id="id" v-model.trim="username" />
      </div>
      <div>
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model.trim="password" />
      </div>
      <button type="submit">로그인</button>
      <div>
        <p>아직 회원이 아니세요?</p>
        <router-link to="/signup">회원가입</router-link>

      </div>

    </form>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import {useUserStore} from "@/stores/userStore.js";

const userStore = useUserStore();
const username = ref('');
const password = ref('');

const logIn = () => {
  const payload = {
    username: username.value,
    password: password.value
  }
  userStore.logIn(payload);
}

</script>

<style scoped>

</style>