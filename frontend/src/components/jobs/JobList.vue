<template>
  <div class="job-grid">
    <JobDetail
      v-for="job in sortedList"
      :key="job.id"
      :job="job"
    />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useJobStore } from '@/stores/jobStore.js';
import JobDetail from './JobDetail.vue';
import { getSortKey } from '@/composables/useDday.js';

const store = useJobStore();

const sortedList = computed(() =>
  [...(store.jobList ?? [])].sort((a, b) => getSortKey(a.close_date) - getSortKey(b.close_date))
)

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
