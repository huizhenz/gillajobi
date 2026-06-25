import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBootcampStore = defineStore('bootcamps', () => {
  const bootcampList = ref([])
  const bootcamp = ref(null)
  const currentPage = ref(1)
  const hasMore = ref(true)
  const isLoading = ref(false)

  const getBootcampList = function () {
    bootcampList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () {
    if (isLoading.value || !hasMore.value) return Promise.resolve()

    isLoading.value = true
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/bootcamps/?page=${currentPage.value}`
    })
    .then(res => {
      bootcampList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const getBootcamp = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/bootcamps/${pk}/`
    })
    .then(res => bootcamp.value = res.data)
    .catch(err => console.log(err))
  }

  return { bootcampList, bootcamp, hasMore, isLoading, getBootcampList, loadMore, getBootcamp }
})
