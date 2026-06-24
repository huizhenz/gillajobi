<template>
  <div class="certification-grid">
    <CertificationDetail
      v-for="certification in store.certificationList"
      :key="certification.pk"
      :certification="certification"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import CertificationDetail from './CertificationDetail.vue';
import { useCertificationStore } from '@/stores/certificationStore.js';

const store = useCertificationStore();

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
