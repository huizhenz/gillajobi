import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useJobStore = defineStore('jobs', () => {
  const jobList = ref([])
  const job = ref(null)
  const currentPage = ref(1) // 다음 요청 시 몇 번째 페이지인지 추적
  const hasMore = ref(true) // 마지막 페이지 도달 여부
  const isLoading = ref(false) // 요청 중 여부

  const getJobList = function () { // 처음부터 다시 시작-
    jobList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () { // 다음 페이지 가져와서 이어붙이기
    if (isLoading.value || !hasMore.value) return
    isLoading.value = true

    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/jobs/?page=${currentPage.value}`
    })
    .then(res => {
      jobList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const getJob = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/jobs/${pk}/`
    })
    .then(res => job.value = res.data)
    .catch(err => console.log(err))
  }

  return { jobList, job, hasMore, isLoading, getJobList, loadMore, getJob }
})
