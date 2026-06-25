<template>
    <div class="competition-card" @click="goDetail(competition.id)">
        <div class="card-top">
            <p class="host">{{ competition.host }}</p>
            <h3 class="title">{{ competition.title }}</h3>
            <p v-if="competition.keyword" class="keyword">{{ competition.keyword }}</p>
        </div>
        <div class="card-bottom">
            <span class="category">{{ competition.category }}</span>
            <span v-if="competition.start_date" class="start-date">{{ competition.start_date }}~</span>
        </div>
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
  color: #2ab59e;
  font-weight: 500;
}

.start-date {
  font-size: 14px;
  color: #999;
}
</style>
