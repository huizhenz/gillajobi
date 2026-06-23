<template>
    <div>
    <app-nav/>
        <div>
            <router-view/>
        </div>
    <app-footer/>
    </div>
</template>

<script setup>
import AppNav from './components/common/AppNav.vue';
import AppFooter from './components/common/AppFooter.vue';

</script>

<style scoped>

</style>
