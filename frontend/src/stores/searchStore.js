import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  const keyword = ref('')
  const results = ref({
    jobs: [],
    bootcamps: [],
    certifications: [],
    competitions: [],
  })

  const search = function () {
    axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/v1/category/search/',
        data: {
            keyword: keyword.value,
        }
    })
    .then(res => results.value = res.data)
    .catch(err => console.log(err))
  }

  return { keyword, results, search }
})
