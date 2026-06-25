<template>
    <div>
        <div class="search-filter-area">
            <SearchBox label="certifications" @results="onResults" />
        </div>
        <template v-if="searchResults === null">
            <AiRecommend type="certifications" />
            <GillajobiPick type="certifications" />
        </template>
        <certification-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
        <TopButton />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import CertificationList from '@/components/certifications/CertificationList.vue'
import SearchBox from '@/components/common/SearchBox.vue'
import GillajobiPick from '@/components/common/gillajobi_pick.vue'
import AiRecommend from '@/components/common/AiRecommend.vue'
import TopButton from '@/components/common/TopButton.vue'

const searchStore = useSearchStore()
const searchResults = ref(null)
const searchedKeyword = ref('')
const onResults = (items) => {
  searchedKeyword.value = searchStore.keyword
  searchResults.value = items
}
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

</style>
