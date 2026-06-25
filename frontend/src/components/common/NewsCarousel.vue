<template>
    <section v-if="news.length" class="news-section">
        <h2 class="section-title">일자리 뉴스</h2>
        <div class="carousel">
            <button class="arrow" @click="prev" :disabled="currentIndex === 0">&#8249;</button>
            <Transition name="fade" mode="out-in">
                <div :key="currentIndex" class="cards">
                    <a
                        v-for="item in visibleItems"
                        :key="item.url"
                        :href="item.url"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="card"
                    >
                        <div class="thumb">
                            <img
                                :src="item.thumbnail || fallbackImg"
                                :alt="item.title"
                                @error="e => e.target.src = fallbackImg"
                            >
                        </div>
                        <p class="card-title">{{ item.title }}</p>
                    </a>
                </div>
            </Transition>
            <button class="arrow" @click="next" :disabled="currentIndex >= maxIndex">&#8250;</button>
        </div>
        <div class="dots">
            <span
                v-for="i in maxIndex + 1"
                :key="i"
                class="dot"
                :class="{ active: currentIndex === i - 1 }"
                @click="currentIndex = i - 1"
            />
        </div>
    </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const ITEMS_PER_PAGE = 3
const fallbackImg = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"%3E%3Crect width="320" height="180" fill="%23f0f0f0"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" fill="%23aaa" font-size="14"%3E이미지 없음%3C/text%3E%3C/svg%3E'

const news = ref([])
const currentIndex = ref(0)

const maxIndex = computed(() => Math.max(0, news.value.length - ITEMS_PER_PAGE))
const visibleItems = computed(() => news.value.slice(currentIndex.value, currentIndex.value + ITEMS_PER_PAGE))

const prev = () => { if (currentIndex.value > 0) currentIndex.value-- }
const next = () => { if (currentIndex.value < maxIndex.value) currentIndex.value++ }

onMounted(() => {
    axios.get('http://127.0.0.1:8000/api/v1/category/news/')
        .then(res => { news.value = res.data.news || [] })
        .catch(() => {})
})
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.news-section {
    padding: 48px 0 60px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111;
    margin-bottom: 24px;
    text-align: center;
}

.carousel {
    display: flex;
    align-items: center;
    gap: 12px;
}

.arrow {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid $teal;
    background: #fff;
    color: $teal;
    font-size: 24px;
    line-height: 1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, color 0.2s;

    &:hover:not(:disabled) {
        background: $teal;
        color: #fff;
    }

    &:disabled {
        border-color: #ddd;
        color: #ddd;
        cursor: default;
    }
}

.cards {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    text-decoration: none;
    color: inherit;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #eee;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s, box-shadow 0.2s;

    &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(42, 181, 158, 0.18);
    }
}

.thumb {
    width: 100%;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: #f5f5f5;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

.card-title {
    padding: 12px 14px;
    font-size: 14px;
    font-weight: 500;
    color: #222;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 20px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ddd;
    cursor: pointer;
    transition: background 0.2s;

    &.active {
        background: $teal;
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@media (max-width: 900px) {
    .cards {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .cards {
        grid-template-columns: 1fr;
    }
}
</style>
