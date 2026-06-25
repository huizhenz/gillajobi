<template>
  <div class="ai-recommend-wrapper">
    <h2 class="ai-recommend-title">✨ AI 추천 {{ LABEL[type] }}</h2>
    <hr class="ai-recommend-divider">

    <!-- 비로그인 -->
    <div v-if="typeState.status === 'not_logged_in'" class="ai-recommend-message">
      <p>로그인 후 AI 추천을 받아보세요</p>
      <router-link :to="{ name: 'LoginView' }" class="msg-link">로그인하기</router-link>
    </div>

    <!-- 프로필 미입력 -->
    <div v-else-if="typeState.status === 'empty_profile'" class="ai-recommend-message">
      <p>프로필을 입력하면 AI 맞춤 추천을 받을 수 있어요</p>
      <router-link :to="{ name: 'UpdateProfileView', params: { username: userStore.username } }" class="msg-link">프로필 입력하기</router-link>
    </div>

    <!-- 계산 중 -->
    <div v-else-if="typeState.status === 'computing' || typeState.loading" class="ai-recommend-message">
      <span class="spinner"></span>
      <p>AI가 맞춤 추천을 계산하고 있어요...</p>
    </div>

    <!-- 관련 결과 없음 -->
    <div v-else-if="typeState.status === 'no_match'" class="ai-recommend-message">
      <p>프로필과 일치하는 {{ LABEL[type] }}이(가) 없습니다.</p>
    </div>

    <!-- 오류 -->
    <div v-else-if="typeState.status === 'error'" class="ai-recommend-message">
      <p>추천을 불러오지 못했습니다.</p>
    </div>

    <!-- 추천 카드 -->
    <div v-else-if="typeState.status === 'ready'" class="pick-list">
      <router-link
        v-for="item in typeState.items"
        :key="item.id"
        :to="item.link"
        class="pick-card"
      >
        <div class="card-header">
          <div class="card-top">
            <p class="subtitle">{{ item.company }}</p>
            <p class="title">{{ item.title }}</p>
            <p class="reason">{{ item.reason }}</p>
          </div>
          <span class="score-badge" :class="scoreBadgeClass(item.score)">{{ item.score }}</span>
        </div>
        <div class="card-bottom">
          <span class="category">{{ item.category }}</span>
          <span class="close-date" v-if="item.close_date">~{{ item.close_date }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useAiScoreStore } from '@/stores/aiScoreStore'
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

const aiScoreStore = useAiScoreStore()
const userStore = useUserStore()

const typeState = computed(() => aiScoreStore.state[props.type])

const scoreBadgeClass = (score) => {
  if (score >= 80) return 'badge-green'
  if (score >= 60) return 'badge-yellow'
  return 'badge-orange'
}

onMounted(async () => {
  await aiScoreStore.getRecommendations(props.type)
  if (typeState.value.status === 'computing') {
    aiScoreStore.pollUntilReady(props.type)
  }
})
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

.ai-recommend-message {
  min-height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #888;
  font-size: 0.9rem;

  p { margin: 0; }
}

.msg-link {
  color: #2ab59e;
  font-weight: 600;
  text-decoration: none;
  &:hover { text-decoration: underline; }
}

.spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 3px solid #e0e0e0;
  border-top-color: #2ab59e;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pick-list {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.pick-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  height: 200px;
  box-sizing: border-box;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s;
  min-width: 0;

  &:hover {
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  min-width: 0;
}

.card-top {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.subtitle {
  font-size: 0.83rem;
  color: #888;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.title {
  font-size: 0.99rem;
  font-weight: 600;
  color: #222;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.reason {
  font-size: 0.78rem;
  color: #888;
  margin: 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.score-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 0.82rem;
  font-weight: 700;
  flex-shrink: 0;

  &.badge-green  { background: #d4f5ee; color: #1a8c7b; }
  &.badge-yellow { background: #fff8d4; color: #9a7d00; }
  &.badge-orange { background: #fdebd0; color: #c06000; }
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  font-size: 0.83rem;
  color: #2ab59e;
  font-weight: 500;
}

.close-date {
  font-size: 0.83rem;
  color: #aaa;
}

@media (max-width: 810px) {
  .pick-list {
    flex-direction: column;
  }

  .pick-card {
    flex: 1 1 100%;
    height: 200px;
  }
}
</style>
