import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCertificationStore = defineStore('certifications', () => {
  const certificationList = ref([])
  const certification = ref(null)
  const currentPage = ref(1)
  const hasMore = ref(true)
  const isLoading = ref(false)

  const getCertificationList = function () {
    certificationList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () {
    if (isLoading.value || !hasMore.value) return Promise.resolve()

    isLoading.value = true
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/certifications/fetch/?page=${currentPage.value}`
    })
    .then(res => {
      certificationList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const getCertification = function (jm_cd) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/certifications/fetch/detail/${jm_cd}/`
    })
    .then(res => certification.value = res.data)
    .catch(err => console.log(err))
  }

  return { certificationList, certification, hasMore, isLoading, getCertificationList, loadMore, getCertification }
})
