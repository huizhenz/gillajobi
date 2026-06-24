<template>
  <div class="competition-grid">
    <CompetitionDetail
      v-for="competition in store.competitionList"
      :key="competition.pk"
      :competition="competition"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCompetitionStore } from '@/stores/competitionStore.js';
import CompetitionDetail from './CompetitionDetail.vue';

const store = useCompetitionStore();

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
