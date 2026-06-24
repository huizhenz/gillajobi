<template>
  <div v-if="store.competition" class="competition-detail">
    <img v-if="store.competition.thumbnail" :src="store.competition.thumbnail" class="thumbnail" alt="썸네일"  />
    <h2>{{ store.competition.title }}</h2>

    <section>
      <h3>공모전 정보</h3>
      <p><span>주최사</span>{{ store.competition.host }}</p>
      <p><span>분야</span>{{ store.competition.keyword }}</p>
      <p><span>접수 시작</span>{{ store.competition.start_date }}</p>
      <p><span>접수 종료</span>{{ store.competition.end_date }}</p>
    </section>

    <section v-if="store.competition.description">
      <h3>공모 요강</h3>
      <p v-for="(value, key) in store.competition.description" :key="key">
        <span>{{ key }}</span>{{ value }}
      </p>
    </section>

    <section>
      <h3>링크</h3>
      <p v-if="store.competition.homepage">
        <a :href="store.competition.homepage" target="_blank">공식 홈페이지</a>
      </p>
      <p v-if="store.competition.detail_url">
        <a :href="store.competition.detail_url" target="_blank">상세 페이지</a>
      </p>
    </section>
  </div>
</template>

<script setup>
import { useCompetitionStore } from '@/stores/competitionStore'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'

const store = useCompetitionStore()
const route = useRoute()

onMounted(() => {
  store.getCompetition(route.params.competitionPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;



.competition-detail {
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  gap: 24px;

  .thumbnail {
    width: 30%;
    object-fit: cover;
    border-radius: 10px;
  }

  h2 {
    font-size: 24px;
    font-weight: 700;
    color: #222;
  }

  section {
    background: #fff;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;

    h3 {
      font-size: 14px;
      font-weight: 600;
      color: $primary;
      padding-bottom: 10px;
      border-bottom: 1px solid #f0f0f0;
    }

    p {
      font-size: 14px;
      color: #333;
      display: flex;
      justify-content: space-between;

      span {
        color: #888;
        flex-shrink: 0;
        width: 100px;
      }

      a {
        color: $primary;
        text-decoration: none;
        &:hover { text-decoration: underline; }
      }
    }
  }
}
</style>
