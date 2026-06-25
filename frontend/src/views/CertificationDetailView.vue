<template>
  <div v-if="store.certification" class="certification-detail">

    <!-- 타이틀 + 디데이 -->
    <div class="detail-header">
      <h2>{{ store.certification.name }}</h2>
      <span v-if="dday" class="dday-badge" :class="{ closed: dday === '마감' }">{{ dday }}</span>
    </div>

    <!-- AI 적합도 점수 -->
    <div v-if="fitScore && fitScore.score !== null" class="ai-score-banner">
      <span class="ai-score-badge" :class="scoreBadgeClass(fitScore.score)">AI 적합도 {{ fitScore.score }}점</span>
      <span class="ai-score-reason">{{ fitScore.reason }}</span>
    </div>

    <!-- 자격증 정보 -->
    <section class="info-section">
      <h3 class="section-title">자격증 정보</h3>
      <div class="info-rows">
        <div v-if="store.certification.series_name" class="info-row">
          <span class="label">계열</span>
          <span class="value">{{ store.certification.series_name }}</span>
        </div>
        <div v-if="store.certification.qualification_cl" class="info-row">
          <span class="label">등급</span>
          <span class="value">{{ store.certification.qualification_cl }}</span>
        </div>
        <div v-if="store.certification.major_job_field" class="info-row">
          <span class="label">직무 대분류</span>
          <span class="value">{{ store.certification.major_job_field }}</span>
        </div>
        <div v-if="store.certification.minor_job_field" class="info-row">
          <span class="label">직무 중분류</span>
          <span class="value">{{ store.certification.minor_job_field }}</span>
        </div>
      </div>
    </section>

    <!-- 시험 일정 -->
    <template v-if="store.certification.examinations?.length">
      <section
        v-for="exam in store.certification.examinations"
        :key="exam.id"
        class="info-section"
      >
        <h3 class="section-title">{{ exam.plan_name }}</h3>
        <div class="info-rows">
          <div v-if="exam.doc_reg_start || exam.doc_reg_end" class="info-row">
            <span class="label">필기 접수</span>
            <span class="value">{{ exam.doc_reg_start }} ~ {{ exam.doc_reg_end }}</span>
          </div>
          <div v-if="exam.doc_exam_start || exam.doc_exam_end" class="info-row">
            <span class="label">필기 시험</span>
            <span class="value">{{ exam.doc_exam_start }} ~ {{ exam.doc_exam_end }}</span>
          </div>
          <div v-if="exam.doc_pass_start || exam.doc_pass_end" class="info-row">
            <span class="label">필기 합격 발표</span>
            <span class="value">{{ exam.doc_pass_start }} ~ {{ exam.doc_pass_end }}</span>
          </div>
          <div v-if="exam.prac_reg_start || exam.prac_reg_end" class="info-row">
            <span class="label">실기 접수</span>
            <span class="value">{{ exam.prac_reg_start }} ~ {{ exam.prac_reg_end }}</span>
          </div>
          <div v-if="exam.prac_exam_start || exam.prac_exam_end" class="info-row">
            <span class="label">실기 시험</span>
            <span class="value">{{ exam.prac_exam_start }} ~ {{ exam.prac_exam_end }}</span>
          </div>
          <div v-if="exam.prac_pass_start || exam.prac_pass_end" class="info-row">
            <span class="label">최종 합격 발표</span>
            <span class="value">{{ exam.prac_pass_start }} ~ {{ exam.prac_pass_end }}</span>
          </div>
        </div>
      </section>
    </template>
    <p v-else class="no-exam">등록된 시험 일정이 없습니다.</p>

  </div>
</template>

<script setup>
import { onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCertificationStore } from '@/stores/certificationStore.js'
import { useAiScoreStore } from '@/stores/aiScoreStore'
import { useDday } from '@/composables/useDday.js'

const route = useRoute()
const store = useCertificationStore()
const aiScoreStore = useAiScoreStore()

const { dday } = useDday(() => store.certification?.examinations?.[0]?.doc_reg_end)

const fitScore = computed(() =>
  store.certification?.id ? aiScoreStore.getScore('certifications', store.certification.id) : null
)

const scoreBadgeClass = (score) => {
  if (score >= 80) return 'badge-green'
  if (score >= 60) return 'badge-yellow'
  return 'badge-orange'
}

watch(() => store.certification?.id, (id) => {
  if (id) aiScoreStore.getSingleScore('certifications', id)
})

onMounted(() => {
  store.getCertification(route.params.jm_cd)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.certification-detail {
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
  }
}

.no-exam {
  font-size: 16px;
  color: #aaa;
  text-align: center;
  padding: 40px 0;
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
