<template>
  <div class="ai-recommend-wrapper">
    <h2 class="ai-recommend-title">✨ AI 추천 {{ LABEL[type] }}</h2>
    <hr class="ai-recommend-divider">

    <div v-if="userStore.isLogin" class="ai-recommend-content">
      <!-- 로그인 시 AI 추천 내용 -->
    </div>

    <div v-else class="gate-container">
      <div class="gate-overlay">
        <div class="gate-card">
          <p class="gate-title">로그인 후 AI 추천을 받아보세요</p>
          <div class="gate-links">
            <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink>
            <span>|</span>
            <RouterLink :to="{ name: 'SignupView' }">회원가입</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
})

const LABEL = {
  jobs: '채용공고',
  bootcamps: '부트캠프',
  certifications: '자격증',
  competitions: '공모전',
}

const userStore = useUserStore()
</script>

<style lang="scss" scoped>
.ai-recommend-wrapper {
  padding: 20px 0;
}

.ai-recommend-title {
  font-size: 22px;
  font-weight: 700;
  color: #222;
  margin: 0 0 8px;
}

.ai-recommend-divider {
  border: none;
  border-top: 2px solid #2ab59e;
  margin: 0 0 16px;
}

.ai-recommend-content {
  min-height: 80px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 0.9rem;
}

/* 비로그인 게이트 */
.gate-container {
  position: relative;
  height: 200px;
}

.gate-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gate-card {
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.14);
  padding: 32px 48px;
  text-align: center;
}

.gate-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 14px;
}

.gate-links {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  font-size: 0.9rem;
  color: #bbb;

  a {
    color: #2ab59e;
    text-decoration: none;
    font-weight: 600;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
