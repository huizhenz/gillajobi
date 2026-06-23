<template>
  <div v-if="store.bootcamp">
    <h1>{{ store.bootcamp.title }}</h1>
    <p>{{ store.bootcamp.company?.name }}</p>
    <p>{{ store.bootcamp.region?.name }}</p>
    <p>{{ store.bootcamp.expense }}</p>
    <p>{{ store.bootcamp.period }}</p>
    <p>{{ store.bootcamp.participation_time }}</p>
    <p>{{ store.bootcamp.program_process }}</p>
    <p>{{ store.bootcamp.recruitment_linkage }}</p>
    <p v-if="store.bootcamp.close_date">~ {{ store.bootcamp.close_date }}</p>
    <p v-else>{{ store.bootcamp.close_date_text }}</p>
    <div>
      <span v-for="skill in store.bootcamp.skills" :key="skill.id">{{ skill.name }} </span>
    </div>
    <a :href="store.bootcamp.recruitment_url" target="_blank">지원하기</a>
  </div>
</template>

<script setup>
import { useBootcampStore } from '@/stores/bootcampStore';
import { useRoute } from 'vue-router';
import { onMounted } from 'vue';

const store = useBootcampStore();
const route = useRoute();

onMounted(() => {
  store.getBootcamp(route.params.bootcampPk);
})
</script>

<style lang="scss" scoped>

</style>