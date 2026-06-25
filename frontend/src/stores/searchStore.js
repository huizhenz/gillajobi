import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const keyword = ref('')
  const searchedKeyword = ref('')
  const isLoading = ref(false)
  const results = ref({
    jobs: [],
    bootcamps: [],
    certifications: [],
    competitions: [],
  })

  const search = function () {
    if (!keyword.value.trim()) return
    searchedKeyword.value = keyword.value
    isLoading.value = true
    results.value = { jobs: [], bootcamps: [], certifications: [], competitions: [] }
    axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
      params: { q: searchedKeyword.value }
    })
    .then(res => { results.value = res.data })
    .catch(err => console.error(err))
    .finally(() => { isLoading.value = false })
  }

  return { keyword, searchedKeyword, isLoading, results, search }
})
