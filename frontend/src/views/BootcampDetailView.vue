<template>
  <div v-if="store.bootcamp" class="bootcamp-detail">

    <!-- 타이틀 + 디데이 -->
    <div class="detail-header">
      <h2>{{ store.bootcamp.title }}</h2>
      <span v-if="dday" class="dday-badge" :class="{ closed: dday === '마감' }">{{ dday }}</span>
    </div>

    <!-- AI 적합도 점수 -->
    <div v-if="fitScore && fitScore.score !== null" class="ai-score-banner">
      <span class="ai-score-badge" :class="scoreBadgeClass(fitScore.score)">AI 적합도 {{ fitScore.score }}점</span>
      <span class="ai-score-reason">{{ fitScore.reason }}</span>
    </div>

    <!-- 부트캠프 정보 -->
    <section class="info-section">
      <h3 class="section-title">부트캠프 정보</h3>
      <div class="info-rows">
        <div v-if="store.bootcamp.company?.name" class="info-row">
          <span class="label">운영 기관</span>
          <span class="value">{{ store.bootcamp.company.name }}</span>
        </div>
        <div v-if="store.bootcamp.region?.name" class="info-row">
          <span class="label">지역</span>
          <span class="value">{{ store.bootcamp.region.name }}</span>
        </div>
        <div v-if="store.bootcamp.program_process" class="info-row">
          <span class="label">과정 유형</span>
          <span class="value">{{ store.bootcamp.program_process }}</span>
        </div>
        <div v-if="store.bootcamp.expense" class="info-row">
          <span class="label">수강료</span>
          <span class="value">{{ store.bootcamp.expense }}</span>
        </div>
        <div v-if="store.bootcamp.period" class="info-row">
          <span class="label">기간</span>
          <span class="value">{{ store.bootcamp.period }}</span>
        </div>
        <div v-if="store.bootcamp.participation_time" class="info-row">
          <span class="label">참여 시간</span>
          <span class="value">{{ store.bootcamp.participation_time }}</span>
        </div>
        <div v-if="store.bootcamp.recruitment_linkage" class="info-row">
          <span class="label">취업 연계</span>
          <span class="value">{{ store.bootcamp.recruitment_linkage }}</span>
        </div>
        <div class="info-row">
          <span class="label">마감일</span>
          <span class="value">{{ store.bootcamp.close_date || store.bootcamp.close_date_text }}</span>
        </div>
      </div>
    </section>

    <!-- 기술 스택 -->
    <section v-if="store.bootcamp.skills?.length" class="info-section">
      <h3 class="section-title">기술 스택</h3>
      <div class="skill-tags">
        <span v-for="skill in store.bootcamp.skills" :key="skill.id" class="skill-tag">{{ skill.name }}</span>
      </div>
    </section>

    <!-- 지원하기 -->
    <div class="apply-wrap">
      <a :href="store.bootcamp.recruitment_url" target="_blank" class="apply-btn">지원하기</a>
    </div>

  </div>
</template>

<script setup>
import { useBootcampStore } from '@/stores/bootcampStore'
import { useAiScoreStore } from '@/stores/aiScoreStore'
import { useRoute } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useDday } from '@/composables/useDday.js'

const store = useBootcampStore()
const aiScoreStore = useAiScoreStore()
const route = useRoute()

const { dday } = useDday(() => store.bootcamp?.close_date)

const fitScore = computed(() => aiScoreStore.getScore('bootcamps', route.params.bootcampPk))

const scoreBadgeClass = (score) => {
  if (score >= 80) return 'badge-green'
  if (score >= 60) return 'badge-yellow'
  return 'badge-orange'
}

onMounted(() => {
  store.getBootcamp(route.params.bootcampPk)
  aiScoreStore.getSingleScore('bootcamps', route.params.bootcampPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.bootcamp-detail {
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
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: 0;
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
  }
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  background-color: #e6f7f5;
  color: $primary;
  font-size: 14px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid #b2e8e0;
}

.apply-wrap {
  display: flex;
  justify-content: center;
  padding: 8px 0;
}

.apply-btn {
  display: inline-block;
  background: $primary;
  color: #fff;
  padding: 14px 48px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 700;
  transition: opacity 0.2s;

  &:hover {
    opacity: 0.85;
  }
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
