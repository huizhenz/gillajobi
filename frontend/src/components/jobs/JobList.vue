<template>
  <div>
    <!-- 검색 -->
    <template v-if="searchResults !== null">
      <p class="search-status" v-if="searchResults.length">"{{ searchedKeyword }}" 검색 결과 {{ searchResults.length }}건</p>
      <p v-else>키워드에 일치하는 정보가 없습니다.</p>
      <div class="job-grid">
        <router-link
          v-for="job in searchResults"
          :key="job.id"
          :to="`/jobs/${job.id}`"
          class="job-card"
        >
          <p class="company-name">{{ job['company__name'] }}</p>
          <h3 class="title">{{ job.title }}</h3>
          <p v-if="job.close_date" class="close-date">~ {{ job.close_date }}</p>
        </router-link>
      </div>
    </template>

    <!-- 목록  -->
    <template v-else>
      <div class="job-grid">
        <JobDetail
          v-for="job in sortedList"
          :key="job.pk"
          :job="job"
        />
      </div>
      <div ref="sentinel" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useJobStore } from '@/stores/jobStore.js'
import JobDetail from './JobDetail.vue'
import { getSortKey } from '@/composables/useDday.js'

defineProps({
  searchResults: { type: Array, default: null },
  searchedKeyword: { type: String, default: '' },
})

const store = useJobStore()
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.jobList ?? [])].sort((a, b) => getSortKey(a.close_date) - getSortKey(b.close_date))
)

onMounted(() => {
  store.getJobList()
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && store.hasMore) store.loadMore()
  })
  observer.observe(sentinel.value)
})

onUnmounted(() => { observer?.disconnect() })
</script>

<style lang="scss" scoped>
.job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}

.search-status {
  font-size: 0.9rem;
  color: #666;
  margin: 0 0 12px;
  padding: 0 4px;
}

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
  text-decoration: none;
  color: inherit;

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
