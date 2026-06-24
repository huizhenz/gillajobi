<template>
  <div class="job-grid">
    <JobDetail
      v-for="job in store.jobList"
      :key="job.id"
      :job="job"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useJobStore } from '@/stores/jobStore.js';
import JobDetail from './JobDetail.vue';

const store = useJobStore();

onMounted(() => {
  store.getJobList();
})
</script>

<style lang="scss" scoped>
.job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}
</style>
