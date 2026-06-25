<template>
    <div class="certification-card" @click="goDetail(certification.jm_cd)">
        <div class="card-top">
            <p class="series">{{ certification.series_name }}</p>
            <h3 class="name">{{ certification.name }}</h3>
            
        </div>
        <div class="card-bottom">
            <p v-if="certification.major_job_field" class="category-sub">{{ certification.major_job_field }}</p>
            <span class="detail-link">시험 일정 보러 가기 →</span>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  certification: Object
})

const router = useRouter()

const goDetail = (jm_cd) => {
  router.push({ name: 'CertificationDetailView', params: { jm_cd: jm_cd } })
}
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.certification-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  height: 200px;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }
}

.card-top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.series {
  font-size: 14px;
  color: #888;
  font-weight: 500;
  margin: 0;
}

.name {
  font-size: 17px;
  font-weight: 700;
  color: #222;
  line-height: 1.4;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.category-sub {
  font-size: 0.83rem;
  color: #2ab59e;
  font-weight: 500;
  margin: 0;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  font-size: 14px;
  color: $primary;
  font-weight: 500;
}

.detail-link {
  font-size: 13px;
  color: #fff;
  font-weight: 600;
  background: $primary;
  padding: 6px 14px;
  border-radius: 7px;
  white-space: nowrap;
}
</style>
