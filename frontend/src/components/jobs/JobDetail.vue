<template>
    <div class="job-card" @click="goDetail(job.id)">
        <p class="company-name">{{ job.company?.name }}</p>
        <h3 class="title">{{ job.title }}</h3>
        <p>{{ job.category }}</p>
        <p v-if="job.close_date" class="close-date">~ {{ job.close_date }}</p>
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
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .company-name {
    font-size: 12px;
    color: #888;
    font-weight: 500;
  }

  .title {
    font-size: 15px;
    font-weight: 700;
    color: #222;
    line-height: 1.4;
    flex: 1;
  }

  .close-date {
    font-size: 13px;
    color: #666;
    text-align: right;
    margin-top: auto;
  }
}
</style>