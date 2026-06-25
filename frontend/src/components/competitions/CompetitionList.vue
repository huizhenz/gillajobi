<template>
  <div class="competition-grid">
    <CompetitionDetail
      v-for="competition in sortedList"
      :key="competition.pk"
      :competition="competition"
    />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useCompetitionStore } from '@/stores/competitionStore.js';
import CompetitionDetail from './CompetitionDetail.vue';
import { getSortKey } from '@/composables/useDday.js';

const store = useCompetitionStore();

const sortedList = computed(() =>
  [...(store.competitionList ?? [])].sort((a, b) => getSortKey(a.end_date) - getSortKey(b.end_date))
)

onMounted(() => {
  store.getCompetitionList();
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
