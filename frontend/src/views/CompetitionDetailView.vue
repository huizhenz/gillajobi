<template>
  <div v-if="store.competition" class="competition-detail">

    <!-- 타이틀 + 디데이 -->
    <div class="detail-header">
      <h2>{{ store.competition.title }}</h2>
      <span v-if="dday" class="dday-badge" :class="{ closed: dday === '마감' }">{{ dday }}</span>
    </div>

    <!-- AI 적합도 점수 -->
    <div v-if="fitScore && fitScore.score !== null" class="ai-score-banner">
      <span class="ai-score-badge" :class="scoreBadgeClass(fitScore.score)">AI 적합도 {{ fitScore.score }}점</span>
      <span class="ai-score-reason">{{ fitScore.reason }}</span>
    </div>

    <!-- 썸네일 + 공모전 정보 -->
    <section class="info-section main-section">
      <div v-if="store.competition.thumbnail" class="thumbnail-wrap">
        <img :src="store.competition.thumbnail" class="thumbnail" alt="썸네일" />
      </div>
      <div class="info-col">
        <h3 class="section-title">공모전 정보</h3>
        <div class="info-rows">
          <div v-if="store.competition.host" class="info-row">
            <span class="label">주최사</span>
            <span class="value">{{ store.competition.host }}</span>
          </div>
          <div v-if="store.competition.keyword" class="info-row">
            <span class="label">분야</span>
            <span class="value">{{ store.competition.keyword }}</span>
          </div>
          <div v-if="store.competition.start_date || store.competition.end_date" class="info-row">
            <span class="label">접수 기간</span>
            <span class="value">{{ store.competition.start_date }} ~ {{ store.competition.end_date }}</span>
          </div>
          <div v-if="store.competition.homepage" class="info-row">
            <span class="label">홈페이지</span>
            <a :href="store.competition.homepage" target="_blank" class="link-value">공모전 홈페이지 바로가기</a>
          </div>
          <div v-if="store.competition.detail_url" class="info-row">
            <span class="label">상세 페이지</span>
            <a :href="store.competition.detail_url" target="_blank" class="link-value">상세 페이지 바로가기</a>
          </div>
        </div>
      </div>
    </section>

    <!-- 공모 요강 -->
    <section v-if="store.competition.description" class="info-section">
      <h3 class="section-title">공모 요강</h3>
      <div class="info-rows">
        <div v-for="(value, key) in store.competition.description" :key="key" class="info-row">
          <span class="label">{{ key }}</span>
          <span class="value">{{ value }}</span>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { useCompetitionStore } from '@/stores/competitionStore'
import { useAiScoreStore } from '@/stores/aiScoreStore'
import { useRoute } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useDday } from '@/composables/useDday.js'

const store = useCompetitionStore()
const aiScoreStore = useAiScoreStore()
const route = useRoute()

const { dday } = useDday(() => store.competition?.end_date)

const fitScore = computed(() => aiScoreStore.getScore('competitions', route.params.competitionPk))

const scoreBadgeClass = (score) => {
  if (score >= 80) return 'badge-green'
  if (score >= 60) return 'badge-yellow'
  return 'badge-orange'
}

onMounted(() => {
  store.getCompetition(route.params.competitionPk)
  aiScoreStore.getSingleScore('competitions', route.params.competitionPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.competition-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 22px 28px;

  h2 {
    font-size: 24px;
    font-weight: 700;
    color: #222;
    line-height: 1.4;
  }
}

.dday-badge {
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  border: 1.5px solid #333;
  border-radius: 50px;
  padding: 6px 18px;
  white-space: nowrap;
  letter-spacing: 0.03em;

  &.closed {
    color: #aaa;
    border-color: #ccc;
  }
}

.info-section {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 24px 28px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: $primary;
  letter-spacing: 0.05em;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.info-row {
  display: flex;
  gap: 24px;
  padding: 12px 0;
  border-bottom: 1px solid #f7f7f7;
  font-size: 16px;

  &:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  .label {
    flex-shrink: 0;
    width: 110px;
    color: #888;
    font-weight: 600;
  }

  .value {
    color: #222;
    line-height: 1.6;
    word-break: keep-all;
    white-space: pre-line;
  }
}

.link-value {
  color: $primary;
  font-size: 16px;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }
}

.main-section {
  display: flex;
  gap: 100px;
  align-items: flex-start;
}

.thumbnail-wrap {
  flex-shrink: 0;
  width: 27%;
}

.thumbnail {
  width: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.info-col {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-self: stretch;
}

.ai-score-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 14px 24px;
}

.ai-score-badge {
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 50px;

  &.badge-green  { background: #d4f5ee; color: #1a8c7b; }
  &.badge-yellow { background: #fff8d4; color: #9a7d00; }
  &.badge-orange { background: #fdebd0; color: #c06000; }
}

.ai-score-reason {
  font-size: 14px;
  color: #555;
}
</style>
