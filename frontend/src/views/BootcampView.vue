<template>
    <div>
        <div class="search-filter-area">
            <select class="filter-select" :value="bootcampStore.selectedRegion" @change="bootcampStore.setRegion($event.target.value)">
                <option value="">전체 지역</option>
                <option v-for="region in bootcampStore.regions" :key="region" :value="region">{{ region }}</option>
            </select>
            <select class="filter-select" :value="bootcampStore.selectedCategory" @change="bootcampStore.setCategory($event.target.value)">
                <option value="">전체 카테고리</option>
                <option v-for="cat in bootcampStore.categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
            <SearchBox label="bootcamps" :extra-params="{ region: bootcampStore.selectedRegion, category: bootcampStore.selectedCategory }" @results="onResults" />
        </div>
        <AiRecommend type="bootcamps" />
        <GillajobiPick type="bootcamps" />
        <bootcamp-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { useBootcampStore } from '@/stores/bootcampStore'
import BootcampList from '@/components/bootcamps/BootcampList.vue'
import SearchBox from '@/components/common/SearchBox.vue'
import GillajobiPick from '@/components/common/gillajobi_pick.vue'
import AiRecommend from '@/components/common/AiRecommend.vue'
import axios from 'axios'

const searchStore = useSearchStore()
const bootcampStore = useBootcampStore()
bootcampStore.selectedRegion = ''      // setup 단계에서 초기화
bootcampStore.selectedCategory = ''

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

const rerunSearch = async () => {
  if (searchResults.value === null || !searchedKeyword.value) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
      params: {
        q: searchedKeyword.value,
        label: 'bootcamps',
        region: bootcampStore.selectedRegion,
        category: bootcampStore.selectedCategory,
      },
    })
    searchResults.value = res.data.bootcamps
  } catch (err) {
    console.error(err)
  }
}

watch(() => bootcampStore.selectedRegion, rerunSearch)
watch(() => bootcampStore.selectedCategory, rerunSearch)
</script>

<style lang="scss" scoped>
div {
  padding: 32px 0;
}

.search-filter-area {
  display: flex;
  align-items: center;
  justify-content: center;
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
