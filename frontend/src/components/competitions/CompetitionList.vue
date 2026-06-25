<template>
  <div>
    <!-- 검색 -->
    <template v-if="searchResults !== null">
      <p class="search-status" v-if="searchResults.length">"{{ searchedKeyword }}" 검색 결과 {{ searchResults.length }}건</p>
      <p v-else>키워드에 일치하는 정보가 없습니다.</p>
      <div class="competition-grid">
        <router-link
          v-for="comp in searchResults"
          :key="comp.id"
          :to="`/competition/${comp.id}`"
          class="competition-card"
        >
          <div class="card-top">
            <p class="host">{{ comp.host }}</p>
            <h3 class="title">{{ comp.title }}</h3>
            <p v-if="comp.keyword" class="keyword">{{ comp.keyword }}</p>
          </div>
          <div class="card-bottom">
            <span class="category">{{ comp.category }}</span>
            <span v-if="comp.start_date" class="start-date">{{ comp.start_date }}~</span>
          </div>
        </router-link>
      </div>
    </template>

    <!-- 목록 -->
    <template v-else>
      <h2 class="section-title">전체 공모전</h2>
      <hr class="section-divider">
      <div class="competition-grid">
        <CompetitionDetail
          v-for="competition in sortedList"
          :key="competition.pk"
          :competition="competition"
        />
      </div>
      <div ref="sentinel" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useCompetitionStore } from '@/stores/competitionStore.js'
import CompetitionDetail from './CompetitionDetail.vue'
import { getSortKey } from '@/composables/useDday.js'

defineProps({
  searchResults: { type: Array, default: null },
  searchedKeyword: { type: String, default: '' },
})

const store = useCompetitionStore()
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.competitionList ?? [])].sort((a, b) => getSortKey(a.end_date) - getSortKey(b.end_date))
)

onMounted(() => {
  store.getCompetitionList()
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && store.hasMore) store.loadMore()
  })
  observer.observe(sentinel.value)
})

onUnmounted(() => { observer?.disconnect() })
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 8px;
  padding: 0;
}

.section-divider {
  border: none;
  border-top: 2px solid $primary;
  margin: 0 0 16px;
}

.competition-grid {
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

.competition-card {
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

.host {
  font-size: 14px;
  color: #888;
  font-weight: 500;
  margin: 0;
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #222;
  line-height: 1.4;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.keyword {
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
  color: $primary;
  font-weight: 500;
}

.start-date {
  font-size: 14px;
  color: #999;
}
</style>
