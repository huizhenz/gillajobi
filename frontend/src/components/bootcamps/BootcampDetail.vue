<template>
    <div class="bootcamp-card" @click="goDetail(bootcamp.id)">
        <p class="company-name">{{ bootcamp.company }}</p>
        <h3 class="title">{{ bootcamp.title }}</h3>
        <p>{{ bootcamp.category }}</p>
        <p v-if="bootcamp.close_date" class="close-date">~ {{ bootcamp.close_date }}</p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  bootcamp: Object
})

const router = useRouter()

const goDetail = (pk) => {
  router.push({ name: 'BootcampDetailView', params: { bootcampPk: pk } })
}
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.bootcamp-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .company-name {
    font-size: 12px;
    color: #888;
    font-weight: 500;
  }

  .title {
    font-size: 15px;
    font-weight: 700;
    color: #222;
    line-height: 1.4;
    flex: 1;
  }

  .close-date {
    font-size: 13px;
    color: #666;
    text-align: right;
    margin-top: auto;
  }
}
</style>