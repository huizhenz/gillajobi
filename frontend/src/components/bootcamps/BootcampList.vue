<template>
  <div>
    <h1>BootCamp List</h1>
    <BootcampDetail
      v-for="bootcamp in store.bootcampList"
      :key="bootcamp.pk"
      :bootcamp="bootcamp"
    />
  </div>
</template>

<script setup>
import { useBootcampStore } from '@/stores/bootcampStore';
import { onMounted } from 'vue';
import BootcampDetail from './BootcampDetail.vue';

const store = useBootcampStore();

onMounted(() => {
  store.getBootcampList();
})
</script>

<style lang="scss" scoped>

</style>
