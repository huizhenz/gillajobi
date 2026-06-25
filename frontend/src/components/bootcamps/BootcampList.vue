<template>
  <div>
    <div class="bootcamp-grid">
      <BootcampDetail
        v-for="bootcamp in store.bootcampList"
        :key="bootcamp.pk"
        :bootcamp="bootcamp"
      />
    </div>
    <div ref="sentinel" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useBootcampStore } from '@/stores/bootcampStore';
import BootcampDetail from './BootcampDetail.vue';

const store = useBootcampStore();
const sentinel = ref(null)
let observer = null

onMounted(() => {
  store.getBootcampList()

  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && store.hasMore) {
      store.loadMore()
    }
  })
  observer.observe(sentinel.value)
})

onUnmounted(() => {
  observer?.disconnect()
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
