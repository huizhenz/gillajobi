<template>
    <div class="bootcamp-card" @click="goDetail(bootcamp.id)">
        <div class="card-top">
            <p class="company-name">{{ bootcamp.company }}</p>
            <h3 class="title">{{ bootcamp.title }}</h3>
        </div>
        <div class="card-bottom">
            <span class="category">{{ bootcamp.category }}</span>
            <span v-if="bootcamp.close_date" class="close-date">~ {{ bootcamp.close_date }}</span>
        </div>
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
.bootcamp-card {
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  padding: 20px;
  height: 200px;
  box-sizing: border-box;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }
}

.card-top {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.company-name {
  font-size: 14px;
  color: #888;
  font-weight: 500;
  margin: 0;
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #222;
  line-height: 1.4;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  font-size: 14px;
  color: #2ab59e;
  font-weight: 500;
}

.close-date {
  font-size: 14px;
  color: #999;
}
</style>
