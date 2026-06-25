<template>
    <div>
        <div class="search-area">
            <SearchBox label="bootcamps" @results="onResults" />
        </div>
        <div class="filter-area">
            <select class="filter-select" :value="bootcampStore.selectedRegion" @change="bootcampStore.setRegion($event.target.value)">
                <option value="">전체 지역</option>
                <option v-for="region in bootcampStore.regions" :key="region" :value="region">{{ region }}</option>
            </select>
            <select class="filter-select" :value="bootcampStore.selectedCategory" @change="bootcampStore.setCategory($event.target.value)">
                <option value="">전체 카테고리</option>
                <option v-for="cat in bootcampStore.categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
        </div>
        <bootcamp-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { useBootcampStore } from '@/stores/bootcampStore'
import BootcampList from '@/components/bootcamps/BootcampList.vue'
import SearchBox from '@/components/common/SearchBox.vue'

const searchStore = useSearchStore()
const bootcampStore = useBootcampStore()
const searchResults = ref(null)
const searchedKeyword = ref('')

onMounted(() => {
  bootcampStore.getRegions()
  bootcampStore.getCategories()
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
