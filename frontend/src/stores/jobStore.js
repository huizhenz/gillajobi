import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useJobStore = defineStore('jobs', () => {
  const jobList = ref([])
  const job = ref(null)
  const currentPage = ref(1)
  const hasMore = ref(true)
  const isLoading = ref(false)
  const selectedRegion = ref('')
  const regions = ref([])

  const getJobList = function () {
    jobList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () {
    if (isLoading.value || !hasMore.value) return
    isLoading.value = true

    const params = new URLSearchParams({ page: currentPage.value })
    if (selectedRegion.value) params.append('region', selectedRegion.value)

    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/jobs/?${params.toString()}`
    })
    .then(res => {
      jobList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const setRegion = function (region) {
    selectedRegion.value = region
    getJobList()
  }

  const getRegions = function () {
    return axios.get('http://127.0.0.1:8000/api/v1/jobs/regions/')
      .then(res => { regions.value = res.data })
      .catch(err => console.log(err))
  }

  const getJob = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/jobs/${pk}/`
    })
    .then(res => job.value = res.data)
    .catch(err => console.log(err))
  }

  return { jobList, job, hasMore, isLoading, selectedRegion, regions, getJobList, loadMore, setRegion, getRegions, getJob }
})
