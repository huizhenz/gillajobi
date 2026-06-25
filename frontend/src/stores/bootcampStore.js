import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBootcampStore = defineStore('bootcamps', () => {
  const bootcampList = ref([])
  const bootcamp = ref(null)
  const currentPage = ref(1)
  const hasMore = ref(true)
  const isLoading = ref(false)
  const selectedRegion = ref('')
  const selectedCategory = ref('')
  const regions = ref([])
  const categories = ref([])

  const getBootcampList = function () {
    bootcampList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () {
    if (isLoading.value || !hasMore.value) return Promise.resolve()

    isLoading.value = true

    const params = new URLSearchParams({ page: currentPage.value })
    if (selectedRegion.value) params.append('region', selectedRegion.value)
    if (selectedCategory.value) params.append('category', selectedCategory.value)

    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/bootcamps/?${params.toString()}`
    })
    .then(res => {
      bootcampList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const setRegion = function (region) {
    selectedRegion.value = region
    getBootcampList()
  }

  const setCategory = function (category) {
    selectedCategory.value = category
    getBootcampList()
  }

  const getRegions = function () {
    return axios.get('http://127.0.0.1:8000/api/v1/bootcamps/regions/')
      .then(res => { regions.value = res.data })
      .catch(err => console.log(err))
  }

  const getCategories = function () {
    return axios.get('http://127.0.0.1:8000/api/v1/bootcamps/categories/')
      .then(res => { categories.value = res.data })
      .catch(err => console.log(err))
  }

  const getBootcamp = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/bootcamps/${pk}/`
    })
    .then(res => bootcamp.value = res.data)
    .catch(err => console.log(err))
  }

  return {
    bootcampList, bootcamp, hasMore, isLoading,
    selectedRegion, selectedCategory, regions, categories,
    getBootcampList, loadMore, setRegion, setCategory,
    getRegions, getCategories, getBootcamp,
  }
})
