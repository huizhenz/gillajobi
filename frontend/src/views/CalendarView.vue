<template>
  <div class="calendar-page">
    <p class="page-tip">* 일정에 마우스를 올려놓으면 지원 가능 타임라인이 보여요</p>
    <div class="calendar-area">
      <Calendar />
    </div>
    <div class="todo-area">
      <TodoProgressCard />
      <Todolist />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Calendar from '@/components/calendar/Calendar.vue'
import Todolist from '@/components/calendar/TodoList.vue'
import TodoProgressCard from '@/components/common/TodoProgressCard.vue'
import { useTodoStore } from '@/stores/todoStore'

const todoStore = useTodoStore()

onMounted(() => {
  todoStore.getTodoList()
})
</script>

<style lang="scss" scoped>
.calendar-page {
    display: flex;
    flex-wrap: wrap;
    gap: 40px;
    padding: 5vh 0;
    margin: 0 auto;
    max-width: 1400px;
}

.page-tip {
    width: 100%;
    font-size: 0.85rem;
    color: #2ab59e;
    margin: 0;
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

@media (max-width: 810px) {
  .calendar-page {
    flex-direction: column;
    padding: 20px 16px;
    margin: 0;
    gap: 40px;
  }

  .calendar-area {
    flex: none;
    width: 100%;
  }

  .todo-area {
    flex: none;
    width: 100%;
  }
}
</style>
