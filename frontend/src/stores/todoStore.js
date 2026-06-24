import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './userStore'

export const useTodoStore = defineStore('todos', () => {
  const userStore = useUserStore()
  const todoList = ref([])

  const completedCount = computed(() =>
    todoList.value.filter(t => t.is_completed).length
  )

  const getTodoList = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/todos/',
      headers: {
        Authorization: `Token ${userStore.token}`
      },
    })
    .then(res => todoList.value = res.data)
    .catch(err => console.log(err))
  }

  const createTodo = function ({ todo }) {
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/todos/',
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: { todo }
    })
    .then(() => getTodoList())
    .catch(err => console.log(err))
  }

  const updateTodo = function ({ pk, is_completed }) {
    return axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/todos/${pk}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: { is_completed }
    })
    .then(() => getTodoList())
    .catch(err => console.log(err))
  }

  const deleteTodo = function (pk) {
    return axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/todos/${pk}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
    })
    .then(() => getTodoList())
    .catch(err => console.log(err))
  }

  return { todoList, completedCount, getTodoList, createTodo, deleteTodo, updateTodo }
})