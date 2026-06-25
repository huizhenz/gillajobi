<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';

const userstore = useUserStore();
const router = useRouter();
const menuOpen = ref(false);

const logOut = function () {
    userstore.logOut();
    menuOpen.value = false;
}

router.afterEach(() => {
    menuOpen.value = false;
})
</script>

<template>
  <div class="nav-wrap">
    <nav class="navbar">
      <div class="nav-left">
        <router-link :to="{ name: 'MainView' }" class="nav-logo">
          <img src="@/assets/LOGO.png" alt="LogoImg" class="logo-img">
        </router-link>
        <router-link :to="{ name: 'JobView' }" class="nav-link desktop-only">채용공고</router-link>
        <router-link :to="{ name: 'CertificationView' }" class="nav-link desktop-only">자격증</router-link>
        <router-link :to="{ name: 'BootcampView' }" class="nav-link desktop-only">부트캠프</router-link>
        <router-link :to="{ name: 'CompetitionView' }" class="nav-link desktop-only">공모전</router-link>
        <router-link :to="{ name: 'CommunityView' }" class="nav-link desktop-only">커뮤니티</router-link>
      </div>

      <div class="nav-right">
        <!-- 데스크탑 -->
        <div v-if="userstore.isLogin" class="nav-right-auth desktop-only">
          <router-link :to="{ name: 'CalendarView' }" class="btn-calendar">캘린더</router-link>
          <router-link v-if="userstore.username" :to="{ name: 'ProfileView', params: { username: userstore.username } }" class="nav-username">{{ userstore.nickname }}님</router-link>
          <form @submit.prevent="logOut" class="logout-form">
            <input type="submit" value="로그아웃" class="btn-logout">
          </form>
        </div>
        <div v-else class="nav-right-guest desktop-only">
          <router-link :to="{ name: 'LoginView' }" class="nav-link">로그인</router-link>
          <router-link :to="{ name: 'SignupView' }" class="btn-signup">회원가입</router-link>
        </div>

        <!-- 햄버거 버튼 -->
        <button class="hamburger mobile-only" @click="menuOpen = !menuOpen" aria-label="메뉴 열기">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <!-- 모바일 드롭다운 메뉴 -->
    <div class="mobile-menu mobile-only" :class="{ open: menuOpen }">
      <router-link :to="{ name: 'JobView' }" class="mobile-link">채용공고</router-link>
      <router-link :to="{ name: 'CertificationView' }" class="mobile-link">자격증</router-link>
      <router-link :to="{ name: 'BootcampView' }" class="mobile-link">부트캠프</router-link>
      <router-link :to="{ name: 'CompetitionView' }" class="mobile-link">공모전</router-link>
      <router-link :to="{ name: 'CommunityView' }" class="mobile-link">커뮤니티</router-link>

      <hr class="mobile-divider" />

      <template v-if="userstore.isLogin">
        <router-link :to="{ name: 'CalendarView' }" class="mobile-link">캘린더</router-link>
        <router-link v-if="userstore.username" :to="{ name: 'ProfileView', params: { username: userstore.username } }" class="mobile-link">{{ userstore.nickname }}님</router-link>
        <button class="mobile-link mobile-logout" @click="logOut">로그아웃</button>
      </template>
      <template v-else>
        <router-link :to="{ name: 'LoginView' }" class="mobile-link">로그인</router-link>
        <router-link :to="{ name: 'SignupView' }" class="mobile-link">회원가입</router-link>
      </template>
    </div>
  </div>
</template>

<style lang="scss" scoped>
$primary: #2ab59e;
$breakpoint: 755px;

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

/* 햄버거 버튼 */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;

  span {
    display: block;
    width: 22px;
    height: 2px;
    background: #333;
    border-radius: 2px;
    transition: background 0.2s;
  }

  &:hover span {
    background: $primary;
  }
}

/* 모바일 드롭다운 */
.mobile-menu {
  display: none;
  flex-direction: column;
  background: white;
  border-top: 1px solid #eee;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;

  &.open {
    max-height: 400px;
  }
}

.mobile-link {
  display: block;
  padding: 14px 24px;
  font-size: 0.95rem;
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
  background: none;
  border: none;
  text-align: left;
  width: 100%;
  cursor: pointer;

  &:hover,
  &.router-link-active {
    background: #f5fffe;
    color: $primary;
  }
}

.mobile-logout {
  font-size: 0.95rem;
  font-weight: 500;
}

.mobile-divider {
  border: none;
  border-top: 1px solid #eee;
  margin: 4px 0;
}

/* 반응형 */
@media (max-width: $breakpoint) {
  .desktop-only {
    display: none !important;
  }

  .mobile-only {
    display: flex;
  }

  .hamburger {
    display: flex;
  }

  .mobile-menu {
    display: flex;
  }
}

@media (min-width: #{$breakpoint + 1px}) {
  .mobile-only {
    display: none !important;
  }
}
</style>
