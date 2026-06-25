<template>
  <div>
    <div class="competition-grid">
      <CompetitionDetail
        v-for="competition in store.competitionList"
        :key="competition.pk"
        :competition="competition"
      />
    </div>
    <div ref="sentinel" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useCompetitionStore } from '@/stores/competitionStore.js';
import CompetitionDetail from './CompetitionDetail.vue';
import { getSortKey } from '@/composables/useDday.js';

const store = useCompetitionStore();
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.competitionList ?? [])].sort((a, b) => getSortKey(a.end_date) - getSortKey(b.end_date))
)

onMounted(() => {
  store.getCompetitionList()

  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && store.hasMore) {
      store.loadMore()
    }
  })
  observer.observe(sentinel.value)
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>

<style lang="scss" scoped>
.competition-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}
</style>
