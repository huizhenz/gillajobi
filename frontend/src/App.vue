<template>
    <div class="app-layout">
        <app-nav/>
        <div class="content-wrap">
            <router-view/>
        </div>
        <app-footer/>
    </div>
</template>

<script setup>
import AppNav from './components/common/AppNav.vue';
import AppFooter from './components/common/AppFooter.vue';
</script>

<style lang="scss">
@import 'pretendard/dist/web/static/pretendard.css';

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body {
    height: 100%;
}

.app-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.content-wrap {
    flex: 1;
    max-width: 1400px;
    width: 100%;
    margin: 0 auto;
    padding: 24px;
}
</style>
