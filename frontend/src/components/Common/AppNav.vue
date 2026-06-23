<script setup>
import { useUserStore } from '@/stores/userStore';

const userstore = useUserStore();
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
            <router-link to="/profile">00님</router-link>
        </div>
        <div v-else>
            <router-link to="/login">로그인</router-link>
            <router-link to="/signup">회원가입</router-link>
        </div>
    </nav>
  </div>
</template>
