<template>
  <div class="certification-grid">
    <CertificationDetail
      v-for="certification in sortedList"
      :key="certification.pk"
      :certification="certification"
    />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import CertificationDetail from './CertificationDetail.vue';
import { useCertificationStore } from '@/stores/certificationStore.js';
import { getSortKey } from '@/composables/useDday.js';

const store = useCertificationStore();

const sortedList = computed(() =>
  [...(store.certificationList ?? [])].sort(
    (a, b) => getSortKey(a.examinations?.[0]?.doc_reg_end) - getSortKey(b.examinations?.[0]?.doc_reg_end)
  )
)

onMounted(() => {
  store.getCertificationList();
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
