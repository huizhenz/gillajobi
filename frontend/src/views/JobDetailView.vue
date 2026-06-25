<template>
  <div v-if="store.job" class="job-detail">

    <!-- 타이틀 + 디데이 -->
    <div class="detail-header">
      <h2>{{ store.job.recruitment?.title }}</h2>
      <span v-if="dday" class="dday-badge" :class="{ closed: dday === '마감' }">{{ dday }}</span>
    </div>

    <!-- 채용 정보 -->
    <section class="info-section">
      <h3 class="section-title">채용 정보</h3>
      <div class="info-rows">
        <div v-if="store.job.company?.name" class="info-row">
          <span class="label">회사명</span>
          <span class="value">{{ store.job.company.name }}</span>
        </div>
        <div v-if="store.job.recruitment?.career" class="info-row">
          <span class="label">경력</span>
          <span class="value">{{ store.job.recruitment.career }}</span>
        </div>
        <div v-if="store.job.recruitment?.education" class="info-row">
          <span class="label">학력</span>
          <span class="value">{{ store.job.recruitment.education }}</span>
        </div>
        <div v-if="store.job.recruitment?.salary" class="info-row">
          <span class="label">급여</span>
          <span class="value">{{ store.job.recruitment.salary }}</span>
        </div>
        <div v-if="store.job.recruitment?.employment_type" class="info-row">
          <span class="label">고용 형태</span>
          <span class="value">{{ store.job.recruitment.employment_type }}</span>
        </div>
        <div v-if="store.job.recruitment?.working_type" class="info-row">
          <span class="label">근무 형태</span>
          <span class="value">{{ store.job.recruitment.working_type }}</span>
        </div>
        <div v-if="store.job.recruitment?.recruitment_count" class="info-row">
          <span class="label">모집 인원</span>
          <span class="value">{{ store.job.recruitment.recruitment_count }}명</span>
        </div>
        <div v-if="cleanAddress(store.job.recruitment?.region)" class="info-row">
          <span class="label">근무 지역</span>
          <span class="value">{{ cleanAddress(store.job.recruitment.region) }}</span>
        </div>
        <div v-if="store.job.recruitment?.created_date" class="info-row">
          <span class="label">등록일</span>
          <span class="value">{{ store.job.recruitment.created_date }}</span>
        </div>
        <div v-if="store.job.recruitment?.close_date" class="info-row">
          <span class="label">마감일</span>
          <span class="value">{{ store.job.recruitment.close_date }}</span>
        </div>
      </div>
    </section>

    <!-- 채용 절차 -->
    <section v-if="store.job.processes?.length" class="info-section">
      <h3 class="section-title">채용 절차</h3>
      <div class="process-steps">
        <span
          v-for="(process, idx) in store.job.processes"
          :key="process.id"
          class="step"
        >
          {{ process.name }}<span v-if="idx < store.job.processes.length - 1" class="arrow"> →</span>
        </span>
      </div>
    </section>

    <!-- 상세 정보 -->
    <section class="info-section detail-section">
      <h3 class="section-title">상세 정보</h3>
      <div class="info-rows">
        <div v-if="store.job.job_description" class="info-row">
          <span class="label">직무 내용</span>
          <span class="value">{{ store.job.job_description }}</span>
        </div>
        <div v-if="store.job.qualification" class="info-row">
          <span class="label">자격 요건</span>
          <span class="value">{{ store.job.qualification }}</span>
        </div>
        <div v-if="store.job.preferred_qualification" class="info-row">
          <span class="label">우대 사항</span>
          <span class="value">{{ store.job.preferred_qualification }}</span>
        </div>
        <div v-if="store.job.license" class="info-row">
          <span class="label">필요 자격증</span>
          <span class="value">{{ store.job.license }}</span>
        </div>
        <div v-if="store.job.computer_skill" class="info-row">
          <span class="label">컴퓨터 능력</span>
          <span class="value">{{ store.job.computer_skill }}</span>
        </div>
        <div v-if="store.job.foreign_language" class="info-row">
          <span class="label">외국어</span>
          <span class="value">{{ store.job.foreign_language }}</span>
        </div>
        <div v-if="store.job.working_hours" class="info-row">
          <span class="label">근무 시간</span>
          <span class="value">{{ store.job.working_hours }}</span>
        </div>
        <div v-if="store.job.break_time" class="info-row">
          <span class="label">휴게 시간</span>
          <span class="value">{{ store.job.break_time }}</span>
        </div>
        <div v-if="cleanAddress(store.job.address)" class="info-row">
          <span class="label">주소</span>
          <span class="value">{{ cleanAddress(store.job.address) }}</span>
        </div>
        <div v-if="store.job.social_insurance" class="info-row">
          <span class="label">4대 보험</span>
          <span class="value">{{ store.job.social_insurance }}</span>
        </div>
        <div v-if="store.job.retirement_pay" class="info-row">
          <span class="label">퇴직금</span>
          <span class="value">{{ store.job.retirement_pay }}</span>
        </div>
        <div v-if="store.job.submission_documents" class="info-row">
          <span class="label">제출 서류</span>
          <span class="value">{{ store.job.submission_documents }}</span>
        </div>
        <div v-if="store.job.application_method" class="info-row">
          <span class="label">지원 방법</span>
          <span class="value">{{ store.job.application_method }}</span>
        </div>
      </div>
    </section>

    <!-- 지도 -->
    <KakaoMap v-if="mapAddress" :address="mapAddress" />

    <!-- 지원하기 -->
    <div class="apply-wrap">
      <a :href="store.job.recruitment?.recruitment_url" target="_blank" class="apply-btn">지원하기</a>
    </div>

  </div>
</template>

<script setup>
import { useJobStore } from '@/stores/jobStore'
import { useRoute } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useDday } from '@/composables/useDday.js'
import KakaoMap from '@/components/jobs/KakaoMap.vue'

const store = useJobStore()
const route = useRoute()

const { dday } = useDday(() => store.job?.recruitment?.close_date)

const cleanAddress = (addr) => addr ? addr.replace(/지도\s*보기.*$/, '').trim() : ''

const mapAddress = computed(() => {
  const addr = store.job?.address || store.job?.recruitment?.region || ''
  return cleanAddress(addr)
})

onMounted(() => {
  store.getJob(route.params.jobPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.job-detail {
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
  text-transform: uppercase;
  letter-spacing: 0.05em;
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

.process-steps {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  font-size: 16px;
  color: #333;

  .step {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .arrow {
    color: $primary;
    font-weight: 700;
  }
}

.detail-section .info-row .value {
  white-space: pre-line;
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
</style>
