<template>
  <div v-if="store.bootcamp" class="bootcamp-detail">
    <h2>{{ store.bootcamp.title }}</h2>
    <p v-if="dday">{{ dday }}</p>

    <section>
      <h3>운영 기관</h3>
      <p><span>기관명</span>{{ store.bootcamp.company?.name }}</p>
    </section>

    <section>
      <h3>부트캠프 정보</h3>
      <p><span>지역</span>{{ store.bootcamp.region?.name }}</p>
      <p><span>과정 유형</span>{{ store.bootcamp.program_process }}</p>
      <p><span>수강료</span>{{ store.bootcamp.expense }}</p>
      <p><span>기간</span>{{ store.bootcamp.period }}</p>
      <p><span>참여 시간</span>{{ store.bootcamp.participation_time }}</p>
      <p><span>취업 연계</span>{{ store.bootcamp.recruitment_linkage }}</p>
      <p v-if="store.bootcamp.close_date"><span>마감일</span>{{ store.bootcamp.close_date }}</p>
      <p v-else><span>마감일</span>{{ store.bootcamp.close_date_text }}</p>
      <p v-if="store.bootcamp.ai_fit_score !== null"><span>AI 적합도</span>{{ store.bootcamp.ai_fit_score }}</p>
    </section>

    <section v-if="store.bootcamp.skills?.length">
      <h3>기술 스택</h3>
      <div class="skill-tags">
        <span v-for="skill in store.bootcamp.skills" :key="skill.id" class="skill-tag">{{ skill.name }}</span>
      </div>
    </section>

    <a :href="store.bootcamp.recruitment_url" target="_blank">지원하기</a>
  </div>
</template>

<script setup>
import { useBootcampStore } from '@/stores/bootcampStore'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useDday } from '@/composables/useDday.js'

const store = useBootcampStore()
const route = useRoute()

const { dday } = useDday(() => store.bootcamp?.close_date)

onMounted(() => {
  store.getBootcamp(route.params.bootcampPk)
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.bootcamp-detail {
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  gap: 24px;

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
    }
  }

  .skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding-top: 4px;
  }

  .skill-tag {
    background-color: #e6f7f5;
    color: $primary;
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid #b2e8e0;
  }

  a {
    display: inline-block;
    background: $primary;
    color: #fff;
    padding: 12px 28px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    align-self: flex-start;

    &:hover {
      opacity: 0.85;
    }
  }
}
</style>
