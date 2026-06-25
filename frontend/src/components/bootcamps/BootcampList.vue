<template>
  <div class="bootcamp-grid">
    <BootcampDetail
      v-for="bootcamp in sortedList"
      :key="bootcamp.pk"
      :bootcamp="bootcamp"
    />
  </div>
</template>

<script setup>
import { useBootcampStore } from '@/stores/bootcampStore';
import { onMounted, computed } from 'vue';
import BootcampDetail from './BootcampDetail.vue';
import { getSortKey } from '@/composables/useDday.js';

const store = useBootcampStore();

const sortedList = computed(() =>
  [...(store.bootcampList ?? [])].sort((a, b) => getSortKey(a.close_date) - getSortKey(b.close_date))
)

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
