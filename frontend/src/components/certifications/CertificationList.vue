<template>
  <div>
    <div class="certification-grid">
      <CertificationDetail
        v-for="certification in store.certificationList"
        :key="certification.pk"
        :certification="certification"
      />
    </div>
    <div ref="sentinel" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import CertificationDetail from './CertificationDetail.vue';
import { useCertificationStore } from '@/stores/certificationStore.js';

const store = useCertificationStore();
const sentinel = ref(null)
let observer = null

onMounted(() => {
  store.getCertificationList()

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
.certification-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 24px;
}
</style>
