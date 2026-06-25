<template>
    <div class="job-card" @click="goDetail(job.id)">
        <div class="card-top">
            <p class="company-name">{{ job.company?.name }}</p>
            <h3 class="title">{{ job.title }}</h3>
            <p v-if="job.recruitment?.career" class="career">{{ job.recruitment.career }}</p>
        </div>
        <div class="card-bottom">
            <span class="category">{{ job.category }}</span>
            <span v-if="job.close_date" class="close-date">~ {{ job.close_date }}</span>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  job: Object
})

const router = useRouter()

const goDetail = (pk) => {
  router.push({ name: 'JobDetailView', params: { jobPk: pk } })
}
</script>

<style lang="scss" scoped>
.job-card {
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

.company-name {
  font-size: 14px;
  color: #888;
  font-weight: 500;
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #222;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.career {
  font-size: 13px;
  color: #aaa;
  margin: 0;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  font-size: 14px;
  color: #2ab59e;
  font-weight: 500;
}

.close-date {
  font-size: 14px;
  color: #999;
}
</style>