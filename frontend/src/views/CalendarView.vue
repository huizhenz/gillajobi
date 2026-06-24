<template>
  <div>
    <div>
      <div>
        <span>To-do list</span>
        <span>{{ todoStore.completedCount }} / {{ todoStore.todoList.length }}</span>
      </div>

      <ul>
        <li v-for="todo in todoStore.todoList" :key="todo.id">
          <input
            type="checkbox"
            :checked="todo.is_completed"
            @change="todoStore.updateTodo({ pk: todo.id, is_completed: !todo.is_completed })"
          />
          <span :style="todo.is_completed ? 'text-decoration: line-through' : ''">
            {{ todo.todo }}
          </span>
          <button @click="todoStore.deleteTodo(todo.id)">×</button>
        </li>
      </ul>

      <div>
        <input
          v-model="newTodo"
          type="text"
          placeholder="할 일 추가"
          @keyup.enter="handleCreate"
        />
        <button @click="handleCreate">추가</button>
      </div>
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

</style>