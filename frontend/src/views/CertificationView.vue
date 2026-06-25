<template>
    <div>
        <div class="search-area">
            <SearchBox label="certifications" @results="onResults" />
        </div>
        <GillajobiPick type="certifications" />
        <certification-list :search-results="searchResults" :searched-keyword="searchedKeyword" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import CertificationList from '@/components/certifications/CertificationList.vue'
import SearchBox from '@/components/common/SearchBox.vue'
import GillajobiPick from '@/components/common/gillajobi_pick.vue'

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

.search-area {
  display: flex;
  justify-content: center;
  padding: 0 24px 32px;
}
</style>
