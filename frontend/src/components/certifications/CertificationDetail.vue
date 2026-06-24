<template>
    <div class="certification-card" @click="goDetail(certification.jm_cd)">
        <h3 class="name">{{ certification.name }}</h3>
        <p class="series">{{ certification.series_name }}</p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  certification: Object
})

const router = useRouter()

const goDetail = (jm_cd) => {
  router.push({ name: 'CertificationDetailView', params: { jm_cd: jm_cd } })
}
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.certification-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .name {
    font-size: 15px;
    font-weight: 700;
    color: #222;
    line-height: 1.4;
  }

  .series {
    font-size: 12px;
    color: #888;
  }
}
</style>