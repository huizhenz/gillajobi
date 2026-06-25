<template>
    <div class="main-container">
        <div class="image-wrapper">
            <img src="../assets/main.gif" alt="길라잡이 메인 이미지">
        </div>
        <div class="content-wrapper">
            <div class="heading" :class="{ typing: !isTypingDone }" v-html="displayedHtml"></div>

            <form class="search-form" @submit.prevent="goToSearch">
                <input v-model="searchStore.keyword" type="text" placeholder="관심 직무를 검색해보세요.">
            </form>
            <div class="example-tags">
                <span class="example-label">ex.</span>
                <span class="example-tag">마케팅</span>
                <span class="example-tag">건축</span>
                <span class="example-tag">보안관제</span>
            </div>
        </div>
    </div>
    <NewsCarousel />
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSearchStore } from '@/stores/searchStore'
import { useUserStore } from '@/stores/userStore'
import NewsCarousel from '@/components/common/NewsCarousel.vue'

const searchStore = useSearchStore()
const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const goToSearch = () => {
    router.push({ name: 'SearchView' })
}

const displayedText = ref('')
const isTypingDone = ref(false)
let typeTimer = null

const windowWidth = ref(window.innerWidth)
const handleResize = () => { windowWidth.value = window.innerWidth }

const fullText = computed(() => {
    if (userStore.isLogin && userStore.nickname) {
        return `안녕하세요, ${userStore.nickname}님 :) \n당신을 취업의 길로 이끌 \n가이드 길라잡이입니다.`
    }
    return `안녕하세요 :) \n당신을 취업의 길로 이끌 \n가이드 길라잡이입니다.`
})

const displayedHtml = computed(() => {
    const text = displayedText.value
    const isNarrow = windowWidth.value <= 1420
    const firstNewline = text.indexOf('\n')

    let greeting = firstNewline === -1 ? text : text.slice(0, firstNewline)

    if (isNarrow && greeting.includes('안녕하세요, ')) {
        greeting = greeting.replace('안녕하세요, ', '안녕하세요,<br>')
    }

    if (firstNewline === -1) {
        return `<span class="line-greeting">${greeting}</span>`
    }

    const rest = text.slice(firstNewline + 1)
        .replace(/\n/g, '<br>')
        .replace('길라잡이', '<span class="teal">길라잡이</span>')

    return `<span class="line-greeting">${greeting}</span>${rest}`
})

const startTyping = () => {
    displayedText.value = ''
    isTypingDone.value = false
    let index = 0
    if (typeTimer) clearInterval(typeTimer)

    typeTimer = setInterval(() => {
        if (index < fullText.value.length) {
            displayedText.value += fullText.value[index]
            index++
        } else {
            clearInterval(typeTimer)
            isTypingDone.value = true
        }
    }, 90)
}

watch(() => route.fullPath, () => {
    startTyping()
})

onMounted(() => {
    window.addEventListener('resize', handleResize)
    startTyping()
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    if (typeTimer) clearInterval(typeTimer)
})
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.main-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 60px;
    padding: 120px 60px 0px 60px;
}

.image-wrapper {
    flex: 0 0 auto;

    img {
        width: 520px;
        object-fit: contain;
    }
}

.content-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}

.heading {
    font-size: 42px;
    font-weight: 700;
    line-height: 1.4;
    text-align: center;
    color: #111;
    max-width: 600px;
    width: 100%;
    min-height: 180px;
    margin-bottom: 24px;

    :deep(.teal) {
        color: $teal;
    }

    :deep(.line-greeting) {
        display: block;
        font-size: 1em;
        font-weight: 700;
        color: #111;
        margin-bottom: 0;
    }

    &.typing::after {
        content: '|';
        color: $teal;
        animation: blink 0.7s step-end infinite;
    }
}

@keyframes blink {
    50% { opacity: 0; }
}

.search-form {
    max-width: 600px;
    width: 100%;

    input {
        width: 100%;
        padding: 18px 24px 18px 52px;
        border: 2px solid $teal;
        border-radius: 50px;
        font-size: 16px;
        outline: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%232DCFC4' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: 20px center;
        box-sizing: border-box;
        box-shadow: 0 8px 32px rgba(42, 181, 158, 0.28);

        &::placeholder {
            color: #aaa;
        }
    }
}

.example-tags {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    max-width: 600px;
    width: 100%;
}

.example-label {
    font-size: 14px;
    color: #aaa;
    font-weight: 500;
    margin-right: 2px;
}

.example-tag {
    font-size: 14px;
    color: #666;
    background: #f2f2f2;
    border-radius: 20px;
    padding: 6px 16px;
}

@media (max-width: 1200px) {
    .image-wrapper {
        img {
            width: 400px;
        }
    }

    .heading {
        font-size: 38px;
    }
}

@media (max-width: 1000px) {
    .main-container {
        flex-direction: column;
        padding: 40px 24px;
        gap: 24px;
    }

    .image-wrapper {
        img {
            width: 100%;
            max-width: 320px;
        }
    }

    .content-wrapper {
        width: 100%;
        gap: 24px;
    }

    .heading {
        font-size: 38px;
    }
}
</style>
