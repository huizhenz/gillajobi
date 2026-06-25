<template>
  <div class="calendar-page">
    <div class="calendar-area">
      <Calendar />
    </div>
    <div class="todo-area">
      <div class="todo-card">
        <span class="todo-label">완료한 To-do</span>
        <p class="todo-count">{{ todoStore.completedCount }}<span class="todo-unit">개</span></p>
        <div class="todo-progress-wrap">
          <div class="todo-progress-bar" :style="{ width: todoProgress + '%' }"></div>
        </div>
        <p class="todo-next">전체 {{ todoStore.todoList.length }}개 중 {{ todoStore.completedCount }}개 완료</p>
      </div>
      <Todolist />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import Calendar from '@/components/calendar/Calendar.vue';
import Todolist from '@/components/calendar/TodoList.vue';
import { useTodoStore } from '@/stores/todoStore'

const todoStore = useTodoStore()

const todoProgress = computed(() => {
  const total = todoStore.todoList.length
  if (!total) return 0
  return Math.round((todoStore.completedCount / total) * 100)
})

onMounted(() => {
  todoStore.getTodoList()
})
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
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.todo-card {
  width: 100%;
  background: #2ab59e;
  border-radius: 14px;
  padding: 18px 20px;
  color: white;
  box-sizing: border-box;
}

.todo-label {
  font-size: 0.90rem;
  font-weight: 600;
  opacity: 0.9;
  display: block;
  margin-bottom: 10px;
}

.todo-count {
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 12px;
}

.todo-unit {
  font-size: 1rem;
  font-weight: 600;
  margin-left: 2px;
}

.todo-progress-wrap {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  height: 6px;
  margin-bottom: 10px;
  overflow: hidden;
}

.todo-progress-bar {
  height: 100%;
  background: white;
  border-radius: 20px;
  transition: width 0.5s ease;
}

.todo-next {
  font-size: 0.78rem;
  opacity: 0.85;
}
</style>