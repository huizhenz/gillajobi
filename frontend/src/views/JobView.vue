<template>
    <div>
        <div class="search-area">
            <SearchBox label="jobs" :extra-params="{ region: jobStore.selectedRegion }" @results="onResults" />
        </div>
        <div class="filter-area">
            <select class="filter-select" :value="jobStore.selectedRegion" @change="jobStore.setRegion($event.target.value)">
                <option value="">전체 지역</option>
                <option v-for="region in jobStore.regions" :key="region" :value="region">{{ region }}</option>
            </select>
        </div>
        <Gillajobi_pick type="jobs" />
        <job-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { useJobStore } from '@/stores/jobStore'
import JobList from '@/components/jobs/JobList.vue'
import SearchBox from '@/components/common/SearchBox.vue'
import axios from 'axios'
import Gillajobi_pick from '@/components/common/gillajobi_pick.vue'

const searchStore = useSearchStore()
const jobStore = useJobStore()
jobStore.selectedRegion = ''  // setup 단계에서 초기화 → 자식 onMounted보다 먼저 실행

const searchResults = ref(null)
const searchedKeyword = ref('')

onMounted(() => {
  jobStore.getRegions()
})

const onResults = (items) => {
  searchedKeyword.value = searchStore.keyword
  searchResults.value = items
}

// 검색 결과 모드일 때 region 변경 시 검색 재실행
watch(() => jobStore.selectedRegion, async (newRegion) => {
  if (searchResults.value === null || !searchedKeyword.value) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
      params: { q: searchedKeyword.value, label: 'jobs', region: newRegion },
    })
    searchResults.value = res.data.jobs
  } catch (err) {
    console.error(err)
  }
})
</script>

<style lang="scss" scoped>
div {
  padding: 32px 0;
}

.search-area {
  display: flex;
  justify-content: center;
  padding: 0 24px 16px;
}

.filter-area {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #333;
  background: #fff;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: #2ab59e;
  }
}
</style>
