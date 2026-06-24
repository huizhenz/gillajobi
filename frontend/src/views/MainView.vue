<template>
    <div class="main-container">
        <div class="image-wrapper">
            <img src="../assets/main.png" alt="길라잡이 메인 이미지">
        </div>
        <div class="content-wrapper">
            <div class="heading">안녕하세요, 민진님 :) <br> 당신을 취업의 길로 이끌 <br> 가이드 <span>길라잡이</span>입니다.</div>
            <form class="search-form" @submit.prevent="goToSearch">
                <input v-model="searchStore.keyword" type="text" placeholder="관심 직무를 검색해보세요.">
            </form>
            <div class="example-tags">
                ex. 마케팅, 클라우드 엔지니어, 영상 디자인
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useSearchStore } from '@/stores/searchStore'

const searchStore = useSearchStore()
const router = useRouter()

const goToSearch = () => {
    router.push('/search')
}
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.main-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 60px;
    padding: 80px 120px;
}

.image-wrapper {
    flex: 0 0 auto;

    img {
        width: 420px;
        object-fit: contain;
    }
}

.content-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.heading {
    font-size: 42px;
    font-weight: 700;
    line-height: 1.4;
    text-align: center;
    color: #111;

    span {
        color: $teal;
    }
}

.search-form {
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

        &::placeholder {
            color: #aaa;
        }
    }
}

.example-tags {
    font-size: 14px;
    color: #555;
}
</style>
