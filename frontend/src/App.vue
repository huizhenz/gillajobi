<template>
    <div>
    <AppNav/>
        <div>
            <router-view/>
        </div>
    </div>
</template>

<script setup>
import AppNav from './components/common/AppNav.vue';
</script>

<style lang="scss">
$teal: #2ab59e;

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
</style>
