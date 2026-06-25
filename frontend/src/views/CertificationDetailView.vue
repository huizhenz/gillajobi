<template>
  <div v-if="store.certification" class="certification-detail">
    <h2 class="name">{{ store.certification.name }}</h2>
    <p class="series">{{ store.certification.series_name }}</p>
    <p v-if="dday">{{ dday }}</p>

    <div v-if="store.certification.examinations && store.certification.examinations.length" class="exam-section">
      <div
        v-for="exam in store.certification.examinations"
        :key="exam.id"
        class="exam-card"
      >
        <p class="plan-name">{{ exam.plan_name }}</p>
        <div class="exam-dates">
          <div class="date-row">
            <span class="label">필기 접수</span>
            <span class="value">{{ exam.doc_reg_start }}</span>
          </div>
          <div class="date-row">
            <span class="label">필기 시험</span>
            <span class="value">{{ exam.doc_exam_start }}</span>
          </div>
          <div class="date-row">
            <span class="label">실기 접수</span>
            <span class="value">{{ exam.prac_reg_start }}</span>
          </div>
          <div class="date-row">
            <span class="label">실기 시험</span>
            <span class="value">{{ exam.prac_exam_start }}</span>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="no-exam">등록된 시험 일정이 없습니다.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCertificationStore } from '@/stores/certificationStore.js'
import { useDday } from '@/composables/useDday.js'

const route = useRoute()
const store = useCertificationStore()

const { dday } = useDday(() => store.certification?.examinations?.[0]?.doc_reg_end)

onMounted(() => {
  store.getCertification(route.params.jm_cd)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.certification-detail {
  padding: 32px 0;

  .name {
    font-size: 24px;
    font-weight: 700;
    color: #222;
    margin-bottom: 6px;
  }

  .series {
    font-size: 14px;
    color: #888;
    margin-bottom: 32px;
  }

  .exam-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .exam-card {
    background: #fff;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
    padding: 20px;

    .plan-name {
      font-size: 14px;
      font-weight: 600;
      color: $primary;
      margin-bottom: 14px;
    }

    .exam-dates {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .date-row {
      display: flex;
      justify-content: space-between;
      font-size: 13px;

      .label {
        color: #888;
      }

      .value {
        color: #333;
        font-weight: 500;
      }
    }
  }

  .no-exam {
    color: #aaa;
    font-size: 14px;
  }
}
</style>
