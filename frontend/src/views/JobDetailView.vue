<template>
  <div v-if="store.job" class="job-detail">
    <h2>{{ store.job.recruitment?.title }}</h2>
    <p v-if="dday">{{ dday }}</p>

    <section>
      <h3>회사 정보</h3>
      <p><span>회사명</span>{{ store.job.company?.name }}</p>
      <p><span>업종</span>{{ store.job.company?.industry }}</p>
      <p><span>기업 규모</span>{{ store.job.company?.size }}</p>
      <p><span>설립연도</span>{{ store.job.company?.established_year }}</p>
      <p><span>연 매출</span>{{ store.job.company?.annual_sales }}</p>
      <p><span>직원 수</span>{{ store.job.company?.employee_count }}</p>
      <p v-if="store.job.company?.homepage">
        <span>홈페이지</span>
        <a :href="store.job.company.homepage" target="_blank">{{ store.job.company.homepage }}</a>
      </p>
    </section>

    <section>
      <h3>채용 정보</h3>
      <p><span>경력</span>{{ store.job.recruitment?.career }}</p>
      <p><span>학력</span>{{ store.job.recruitment?.education }}</p>
      <p><span>급여</span>{{ store.job.recruitment?.salary }}</p>
      <p><span>고용 형태</span>{{ store.job.recruitment?.employment_type }}</p>
      <p><span>근무 형태</span>{{ store.job.recruitment?.working_type }}</p>
      <p><span>모집 인원</span>{{ store.job.recruitment?.recruitment_count }}</p>
      <p><span>근무 지역</span>{{ store.job.recruitment?.region }}</p>
      <p><span>마감일</span>{{ store.job.recruitment?.close_date }}</p>
      <p><span>등록일</span>{{ store.job.recruitment?.created_date }}</p>
      <p><span>조회수</span>{{ store.job.recruitment?.view_count }}</p>
    </section>

    <section v-if="store.job.processes?.length">
      <h3>채용 절차</h3>
      <p v-for="process in store.job.processes" :key="process.id">{{ process.name }}</p>
    </section>

    <section>
      <h3>상세 정보</h3>
      <p><span>직무 내용</span>{{ store.job.job_description }}</p>
      <p><span>자격 요건</span>{{ store.job.qualification }}</p>
      <p><span>우대 사항</span>{{ store.job.preferred_qualification }}</p>
      <p><span>필요 자격증</span>{{ store.job.license }}</p>
      <p><span>컴퓨터 능력</span>{{ store.job.computer_skill }}</p>
      <p><span>외국어</span>{{ store.job.foreign_language }}</p>
      <p><span>근무 시간</span>{{ store.job.working_hours }}</p>
      <p><span>휴게 시간</span>{{ store.job.break_time }}</p>
      <p><span>주소</span>{{ store.job.address }}</p>
      <p><span>4대 보험</span>{{ store.job.social_insurance }}</p>
      <p><span>퇴직금</span>{{ store.job.retirement_pay }}</p>
      <p><span>제출 서류</span>{{ store.job.submission_documents }}</p>
      <p><span>지원 방법</span>{{ store.job.application_method }}</p>
    </section>

    <a :href="store.job.recruitment?.recruitment_url" target="_blank">지원하기</a>
  </div>
</template>

<script setup>
import { useJobStore } from '@/stores/jobStore'
import { useRoute } from 'vue-router'
import { onMounted, computed } from 'vue'
import { useDday } from '@/composables/useDday.js'

const store = useJobStore()
const route = useRoute()

const { dday } = useDday(() => store.job?.recruitment?.close_date)

onMounted(() => {
  store.getJob(route.params.jobPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.job-detail {
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  gap: 24px;

  h2 {
    font-size: 24px;
    font-weight: 700;
    color: #222;
  }

  section {
    background: #fff;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;

    h3 {
      font-size: 14px;
      font-weight: 600;
      color: $primary;
      padding-bottom: 10px;
      border-bottom: 1px solid #f0f0f0;
    }

    p {
      font-size: 14px;
      color: #333;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;

      span {
        color: #888;
        flex-shrink: 0;
        width: 110px;
      }

      a {
        color: $primary;
        text-decoration: none;
        &:hover { text-decoration: underline; }
      }
    }
  }

  > a {
    display: inline-block;
    background: $primary;
    color: #fff;
    padding: 12px 28px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    align-self: flex-start;

    &:hover {
      opacity: 0.85;
    }
  }
}
</style>
