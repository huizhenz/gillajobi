<template>
  <div>
    <form @submit.prevent="signUp">
    <div>
        <h2>기본 정보</h2>
        <p>*필수 입력</p>

      <div>
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username" />
        <p v-for="msg in errors.username" :key="msg" class="error">{{ msg }}</p>
      </div>
      <div>
        <label for="email">이메일</label>
        <input type="email" id="email" v-model.trim="email" />
        <p v-for="msg in errors.email" :key="msg" class="error">{{ msg }}</p>
      </div>
      <div>
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model.trim="password1" />
        <p v-for="msg in errors.password1" :key="msg" class="error">{{ msg }}</p>
      </div>
      <div>
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model.trim="password2" />
        <p v-for="msg in errors.password2" :key="msg" class="error">{{ msg }}</p>
      </div>
      <h2>추가 정보</h2>
      <div>
        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" v-model.trim="nickname" />
        <p v-for="msg in errors.nickname" :key="msg" class="error">{{ msg }}</p>
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

<style scoped>
.error {
  color: red;
  font-size: 0.8rem;
  margin: 2px 0 0;
}
</style>