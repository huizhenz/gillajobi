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
import { getSortKey } from '@/composables/useDday.js';

const store = useCertificationStore();
const sentinel = ref(null)
let observer = null

const sortedList = computed(() =>
  [...(store.certificationList ?? [])].sort((a, b) =>
    a.name.localeCompare(b.name, 'ko')
  )
)

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
