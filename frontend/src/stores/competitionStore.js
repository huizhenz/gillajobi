import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCompetitionStore = defineStore('competitions', () => {
  const competitionList = ref([])
  const competition = ref(null)

  const getCompetitionList = function () {
    return axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/competitions/fetch/'
    })
    .then(res => competitionList.value = res.data)
    .catch(err => console.log(err))
  }

  const getCompetition = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/competitions/fetch/detail/${pk}/`
    })
    .then(res => competition.value = res.data)
    .catch(err => console.log(err))
  }

  return { competitionList, competition, getCompetitionList, getCompetition }
})
