<template>
    <div>
        <p>여기에 검색창</p>
        <bootcamp-list/>
    </div>
</template>

<script setup>
import BootcampList from '@/components/bootcamps/BootcampList.vue';


</script>

<style lang="scss" scoped>
$primary: #2ab59e;

div {
  padding: 32px 0;
}

.search-area {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;

  p {
    color: #aaa;
    font-size: 14px;
  }
}
</style>