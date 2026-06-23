<script setup>
import { useUserStore } from '@/stores/userStore';

const userstore = useUserStore();
const logOut = function () {
    userstore.logOut();
}
</script>

<template>
  <div>
    <nav>
        <div>
            <router-link to="/">
                <img src="@/assets/LOGO.png" alt="LogoImg">
            </router-link>
            <router-link to="/jobs">채용공고</router-link>
            <router-link to="/certification">자격증</router-link>
            <router-link to="/bootcamp">부트캠프</router-link>
            <router-link to="/competition">공모전</router-link>
            <router-link to="/community">커뮤니티</router-link>
        </div>
        <div v-if="userstore.isLogin">
            <router-link to="/calendar">캘린더</router-link>
            <router-link v-if="userstore.username" :to="{ name: 'ProfileView', params: { username: userstore.username } }">{{ userstore.username }}님의 프로필</router-link>
        </div>
        <div v-else>
            <router-link to="/login">로그인</router-link>
            <router-link to="/signup">회원가입</router-link>
        </div>
        <div v-if="userstore.isLogin">
            <form @submit.prevent="logOut">
                <input type="submit" value="로그아웃">
            </form>
        </div>

    </nav>
  </div>
</template>
