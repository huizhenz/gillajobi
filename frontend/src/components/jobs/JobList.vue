<template>
  <div>
    <div class="job-grid">
      <JobDetail
        v-for="job in store.jobList"
        :key="job.pk"
        :job="job"
      />
    </div>
    <div ref="sentinel" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useJobStore } from '@/stores/jobStore.js';
import JobDetail from './JobDetail.vue';
import { getSortKey } from '@/composables/useDday.js';

const store = useJobStore();
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.jobList ?? [])].sort((a, b) => getSortKey(a.close_date) - getSortKey(b.close_date))
)

onMounted(() => {
  store.getJobList()

  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && store.hasMore) {
      store.loadMore()
    }
  })
  observer.observe(sentinel.value)
})

onUnmounted(() => {
  observer?.disconnect()
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
