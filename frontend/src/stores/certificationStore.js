import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCertificationStore = defineStore('certifications', () => {
  const certificationList = ref([])
  const certification = ref(null)

  const getCertificationList = function () {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/certifications/fetch/'
    })
    .then(res => certificationList.value = res.data)
    .catch(err => console.log(err))
  }

  const getCertification = function (jm_cd) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/certifications/fetch/detail/${jm_cd}/`
    })
    .then(res => certification.value = res.data)
    .catch(err => console.log(err))
  }

  return { certificationList, certification, getCertificationList, getCertification }
})
