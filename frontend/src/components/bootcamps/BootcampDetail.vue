<template>
    <div @click="goDetail(bootcamp.id)">
        <p>{{ bootcamp.company?.name }}</p>
        <h3>{{ bootcamp.title }}</h3>
        <p v-if="bootcamp.close_date">~ {{ bootcamp.close_date }}</p>
        <hr>
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

</style>