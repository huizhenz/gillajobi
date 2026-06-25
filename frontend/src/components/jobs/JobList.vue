<template>
  <div>
    <!-- 검색 -->
    <template v-if="searchResults !== null">
      <p class="search-status" v-if="searchResults.length">"{{ searchedKeyword }}" 검색 결과 {{ searchResults.length }}건</p>
      <p v-else class="no-result">"{{ searchedKeyword }}"에 일치하는 정보가 없습니다.</p>
      <div class="job-grid">
        <router-link
          v-for="job in searchResults"
          :key="job.id"
          :to="`/jobs/${job.id}`"
          class="job-card"
        >
          <div class="card-top">
            <p class="company-name">{{ job['company__name'] }}</p>
            <h3 class="title">{{ job.title }}</h3>
            <p v-if="job.career" class="career">{{ job.career }}</p>
          </div>
          <div class="card-bottom">
            <span class="category">{{ job.category }}</span>
            <span v-if="job.close_date" class="close-date">~ {{ job.close_date }}</span>
          </div>
        </router-link>
      </div>
    </template>

    <!-- 목록  -->
    <template v-else>
      <template v-if="selectedRegion">
        <p class="search-status">"{{ selectedRegion }}" 검색결과 {{ store.jobList.length }}건</p>
      </template>
      <template v-else>
        <h2 class="section-title">전체 채용공고</h2>
        <hr class="section-divider">
      </template>
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
  selectedRegion: { type: String, default: '' },
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
.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 8px;
  padding: 0;
}

.section-divider {
  border: none;
  border-top: 2px solid #2ab59e;
  margin: 0 0 16px;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}

.no-result {
  font-size: 1.2rem;
  color: #888;
  padding: 40px 0;
  text-align: center;
}

.search-status {
  font-size: 1rem;
  color: #666;
  margin: 0 0 12px;
  padding: 0 4px;
}

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
  text-decoration: none;
  color: inherit;

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
