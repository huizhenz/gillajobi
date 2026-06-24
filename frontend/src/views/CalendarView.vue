<template>
  <div class="calendar-page">
    <div class="calendar-area">
      <Calendar />
    </div>
    <div class="todo-area">
      <Todolist />
    </div>
  </div>
</template>

<script setup>
import Calendar from '@/components/calendar/Calendar.vue';
import Todolist from '@/components/calendar/TodoList.vue';
</script>

<style lang="scss" scoped>
.calendar-page {
    display: flex;
    gap: 24px;
    padding: 40px;
    margin: 0 -24px;
}

.calendar-area {
    flex: 8;
}

.todo-area {
    flex: 2;
}
</style>