import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBootcampStore = defineStore('bootcamps', () => {
  const bootcampList = ref([])
  const bootcamp = ref(null)

  const getBootcampList = function () {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/bootcamps/'
    })
    .then(res => bootcampList.value = res.data)
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

  return { bootcampList, bootcamp, getBootcampList, getBootcamp }
})
