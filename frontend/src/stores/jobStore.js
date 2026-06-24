import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useJobStore = defineStore('jobs', () => {
  const jobList = ref([])
  const job = ref(null)

  const getJobList = function () {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/jobs/'
    })
    .then(res => jobList.value = res.data)
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

  return { jobList, job, getJobList, getJob }
})
