<script setup>
import { useUserStore } from '@/stores/userStore';

const userstore = useUserStore();
const logOut = function () {
    userstore.logOut();
}
</script>

<template>
  <div class="nav-wrap">
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/" class="nav-logo">
          <img src="@/assets/LOGO.png" alt="LogoImg" class="logo-img">
        </router-link>
        <router-link to="/jobs" class="nav-link">채용공고</router-link>
        <router-link to="/certification" class="nav-link">자격증</router-link>
        <router-link to="/bootcamp" class="nav-link">부트캠프</router-link>
        <router-link to="/competition" class="nav-link">공모전</router-link>
        <router-link to="/community" class="nav-link">커뮤니티</router-link>
      </div>

      <div class="nav-right">
        <div v-if="userstore.isLogin" class="nav-right-auth">
          <router-link to="/calendar" class="btn-calendar">캘린더</router-link>
          <router-link v-if="userstore.username" :to="{ name: 'ProfileView', params: { username: userstore.username } }" class="nav-username">{{ userstore.username }}님</router-link>
          <form @submit.prevent="logOut" class="logout-form">
            <input type="submit" value="로그아웃" class="btn-logout">
          </form>
        </div>
        <div v-else class="nav-right-guest">
          <router-link to="/login" class="nav-link">로그인</router-link>
          <router-link to="/signup" class="btn-signup">회원가입</router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<style lang="scss" scoped>
$primary: #2ab59e;

.nav-wrap {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  border-bottom: 1px solid #eee;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.navbar {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-logo {
  display: flex;
  align-items: center;
  margin-right: 8px;
  text-decoration: none;
}

.logo-img {
  height: 28px;
  width: auto;
}

.nav-link {
  font-size: 0.92rem;
  color: #444;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;

  &:hover,
  &.router-link-active {
    color: $primary;
  }
}

.nav-right {
  display: flex;
  align-items: center;
}

.nav-right-auth,
.nav-right-guest {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-calendar {
  background: $primary;
  color: white;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 7px 18px;
  border-radius: 20px;
  transition: background 0.2s;

  &:hover {
    background: #239e8a;
  }
}

.nav-username {
  font-size: 0.9rem;
  color: #333;
  text-decoration: none;
  font-weight: 600;

  &:hover {
    color: $primary;
  }
}

.nav-link-sm {
  font-size: 0.82rem;
  color: #999;
  text-decoration: none;

  &:hover {
    color: $primary;
  }
}

.logout-form {
  margin: 0;
}

.btn-logout {
  background: none;
  border: none;
  font-size: 0.85rem;
  color: #aaa;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;

  &:hover {
    color: #555;
  }
}

.btn-signup {
  background: $primary;
  color: white;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 7px 18px;
  border-radius: 20px;
  transition: background 0.2s;

  &:hover {
    background: #239e8a;
  }
}
</style>
