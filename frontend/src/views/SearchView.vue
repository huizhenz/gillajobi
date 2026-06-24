<template>
    <div>
        <h2>{{ searchStore.keyword }} 검색 결과</h2>

        <div>
            <h3>채용공고</h3>
            <div v-for="job in searchStore.results.jobs" :key="job.id">
                {{ job.title }}
            </div>
        </div>

        <div>
            <h3>부트캠프</h3>
            <div v-for="bootcamp in searchStore.results.bootcamps" :key="bootcamp.id">
                {{ bootcamp.title }}
            </div>
        </div>

        <div>
            <h3>자격증</h3>
            <div v-for="cert in searchStore.results.certifications" :key="cert.id">
                {{ cert.title }}
            </div>
        </div>

        <div>
            <h3>공모전</h3>
            <div v-for="comp in searchStore.results.competitions" :key="comp.id">
                {{ comp.title }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()
onMounted(() => {
    searchStore.search()
})

</script>

<style lang="scss" scoped>

</style>