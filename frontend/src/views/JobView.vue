<template>
    <div>
        <div class="search-area">
            <SearchBox label="jobs" @results="onResults" />
        </div>
        <div class="filter-area">
            <select class="filter-select" :value="jobStore.selectedRegion" @change="jobStore.setRegion($event.target.value)">
                <option value="">전체 지역</option>
                <option v-for="region in jobStore.regions" :key="region" :value="region">{{ region }}</option>
            </select>
        </div>
        <job-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { useJobStore } from '@/stores/jobStore'
import JobList from '@/components/jobs/JobList.vue'
import SearchBox from '@/components/common/SearchBox.vue'

const searchStore = useSearchStore()
const jobStore = useJobStore()
const searchResults = ref(null)
const searchedKeyword = ref('')

onMounted(() => {
  jobStore.getRegions()
})

const onResults = (items) => {
  searchedKeyword.value = searchStore.keyword
  searchResults.value = items
}
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
