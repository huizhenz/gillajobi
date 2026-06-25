<template>
    <div class="competition-card" @click="goDetail(competition.id)">
        <p class="host">{{ competition.host }}</p>
        <h3 class="title">{{ competition.title }}</h3>
        <p v-if="competition.keyword" class="keyword">{{ competition.keyword }}</p>
        <p v-if="competition.start_date" class="close-date">{{ competition.start_date }}~</p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  competition: Object
})

const router = useRouter()

const goDetail = (pk) => {
  router.push({ name: 'CompetitionDetailView', params: { competitionPk: pk } })
}
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.competition-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .host {
    font-size: 12px;
    color: #888;
    font-weight: 500;
  }

  .title {
    font-size: 15px;
    font-weight: 700;
    color: #222;
    line-height: 1.4;
    flex: 1;
  }

  .keyword {
    font-size: 12px;
    color: #fff;
    background-color: $primary;
    padding: 3px 10px;
    border-radius: 20px;
    align-self: flex-start;
  }

  .close-date {
    font-size: 13px;
    color: #666;
    text-align: right;
    margin-top: auto;
  }
}
</style>