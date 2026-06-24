<template>
  <div class="bootcamp-grid">
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
.bootcamp-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}
</style>
