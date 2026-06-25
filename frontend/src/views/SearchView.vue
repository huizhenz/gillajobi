<template>
    <div class="search-container">
        <h2 class="search-title">"{{ searchStore.keyword }}" 검색 결과</h2>

        <section class="category-section">
            <h3 class="category-title">채용공고</h3>
            <router-link to="/jobs">더보기</router-link>
    
            <div class="card-grid">
                <div v-for="job in searchStore.results.jobs" :key="job.id" class="card">
                    <span class="card-type">채용</span>
                    <p class="card-title">{{ job.title }}</p>
                </div>
            </div>
        </section>

        <section class="category-section">
            <h3 class="category-title">부트캠프</h3>
            <router-link to="/bootcamp">더보기</router-link>

            <div class="card-grid">
                <div v-for="bootcamp in searchStore.results.bootcamps" :key="bootcamp.id" class="card">
                    <span class="card-type">부트캠프</span>
                    <p class="card-title">{{ bootcamp.title }}</p>
                </div>
            </div>
        </section>

        <section class="category-section">
            <h3 class="category-title">자격증</h3>
            <router-link to="/certification">더보기</router-link>

            <div class="card-grid">
                <div v-for="cert in searchStore.results.certifications" :key="cert.id" class="card">
                    <span class="card-type">자격증</span>
                    <p class="card-title">{{ cert.title }}</p>
                </div>
            </div>
        </section>

        <section class="category-section">
            <h3 class="category-title">공모전</h3>
            <router-link to="/competition">더보기</router-link>

            <div class="card-grid">
                <div v-for="comp in searchStore.results.competitions" :key="comp.id" class="card">
                    <span class="card-type">공모전</span>
                    <p class="card-title">{{ comp.title }}</p>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { RouterLink } from 'vue-router';

const searchStore = useSearchStore()
onMounted(() => {
    searchStore.search()
})
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.search-container {
    padding: 40px 60px;
}

.search-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 40px;
    color: #111;
}

.category-section {
    margin-bottom: 48px;
}

.category-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid $teal;
    color: #111;
}

.card-grid {
    display: flex;
    gap: 16px;
}

.card {
    flex: 1;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    cursor: pointer;
    transition: box-shadow 0.2s;

    &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
}

.card-type {
    font-size: 12px;
    color: white;
    background-color: $teal;
    padding: 3px 10px;
    border-radius: 20px;
}

.card-title {
    margin-top: 12px;
    font-size: 15px;
    font-weight: 600;
    color: #222;
}
</style>