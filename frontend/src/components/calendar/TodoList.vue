<template>
  <div class="todo-wrapper">
    <div class="todo-header">
      <span class="todo-title">TodoList</span>
    </div>
    <hr class="divider" />

    <ul class="todo-list">
      <li v-for="todo in todoStore.todoList" :key="todo.id" class="todo-item">
        <input
          type="checkbox"
          :checked="todo.is_completed"
          @change="todoStore.updateTodo({ pk: todo.id, is_completed: !todo.is_completed })"
          class="todo-checkbox"
        />
        <span :class="['todo-text', { done: todo.is_completed }]">
          {{ todo.todo }}
        </span>
        <button class="todo-delete" @click="todoStore.deleteTodo(todo.id)">×</button>
      </li>
    </ul>

    <div class="todo-input-area">
      <input
        v-model="newTodo"
        type="text"
        placeholder=""
        @keyup.enter="handleCreate"
        class="todo-input"
      />
      <button class="todo-add-btn" @click="handleCreate">추가</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTodoStore } from '@/stores/todoStore'

const todoStore = useTodoStore()
const newTodo = ref('')

const handleCreate = function () {
  if (!newTodo.value.trim()) return
  todoStore.createTodo({ todo: newTodo.value.trim() })
  newTodo.value = ''
}

onMounted(() => {
  todoStore.getTodoList()
})
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.todo-wrapper {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    height: 100%;
}

.todo-header {
    margin-bottom: 12px;
}

.todo-title {
    font-size: 18px;
    font-weight: 700;
    color: #111;
}

.divider {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin-bottom: 16px;
}

.todo-list {
    list-style: none;
    padding: 0;
    margin: 0 0 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.todo-checkbox {
    width: 20px;
    height: 20px;
    accent-color: $teal;
    cursor: pointer;
    flex-shrink: 0;
}

.todo-text {
    flex: 1;
    font-size: 14px;
    color: #333;

    &.done {
        text-decoration: line-through;
        color: #aaa;
    }
}

.todo-delete {
    background: none;
    border: none;
    color: #e57373;
    font-size: 16px;
    cursor: pointer;
    padding: 0 4px;
}

.todo-input-area {
    display: flex;
    gap: 8px;
    margin-top: auto;
}

.todo-input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    outline: none;

    &:focus {
        border-color: $teal;
    }
}

.todo-add-btn {
    padding: 8px 14px;
    background: $teal;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;

    &:hover {
        opacity: 0.9;
    }
}
</style>