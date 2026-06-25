<template>
  <div>
    <!-- 검색 -->
    <template v-if="searchResults !== null">
      <p class="search-status" v-if="searchResults.length">"{{ searchedKeyword }}" 검색 결과 {{ searchResults.length }}건</p>
      <p v-else>키워드에 일치하는 정보가 없습니다.</p>
      <div class="certification-grid">
        <router-link
          v-for="cert in searchResults"
          :key="cert.id"
          :to="`/certification/${cert.jm_cd}`"
          class="certification-card"
        >
          <div class="card-top">
            <p class="series">{{ cert.series_name }}</p>
            <h3 class="name">{{ cert.name }}</h3>
          </div>
          <div class="card-bottom">
            <span class="detail-link">시험 일정 보러 가기 →</span>
          </div>
        </router-link>
      </div>
    </template>

    <!-- 목록 -->
    <template v-else>
      <h2 class="section-title">전체 자격증</h2>
      <hr class="section-divider">
      <div class="certification-grid">
        <CertificationDetail
          v-for="certification in sortedList"
          :key="certification.pk"
          :certification="certification"
        />
      </div>
      <div ref="sentinel" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import CertificationDetail from './CertificationDetail.vue'
import { useCertificationStore } from '@/stores/certificationStore.js'

defineProps({
  searchResults: { type: Array, default: null },
  searchedKeyword: { type: String, default: '' },
})

const store = useCertificationStore()
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.certificationList ?? [])].sort((a, b) =>
    a.name.localeCompare(b.name, 'ko')
  )
)

onMounted(() => {
  store.getCertificationList()
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
  border-top: 2px solid #2ab59e;
  margin: 0 0 16px;
}

.certification-grid {
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

.certification-card {
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

.series {
  font-size: 14px;
  color: #888;
  font-weight: 500;
  margin: 0;
}

.name {
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

.card-bottom {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.detail-link {
  font-size: 13px;
  color: #fff;
  font-weight: 600;
  background: $primary;
  padding: 6px 14px;
  border-radius: 20px;
  white-space: nowrap;
}
</style>
