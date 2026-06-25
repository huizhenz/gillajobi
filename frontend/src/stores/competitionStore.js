import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useCompetitionStore = defineStore('competitions', () => {
  const competitionList = ref([])
  const competition = ref(null)
  const currentPage = ref(1)
  const hasMore = ref(true)
  const isLoading = ref(false)

  const getCompetitionList = function () {
    competitionList.value = []
    currentPage.value = 1
    hasMore.value = true
    return loadMore()
  }

  const loadMore = function () {
    if (isLoading.value || !hasMore.value) return Promise.resolve()

    isLoading.value = true
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/competitions/fetch/?page=${currentPage.value}`
    })
    .then(res => {
      competitionList.value.push(...res.data.results)
      hasMore.value = res.data.next !== null
      currentPage.value++
    })
    .catch(err => console.log(err))
    .finally(() => isLoading.value = false)
  }

  const getCompetition = function (pk) {
    return axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/competitions/fetch/detail/${pk}/`
    })
    .then(res => competition.value = res.data)
    .catch(err => console.log(err))
  }

  return { competitionList, competition, hasMore, isLoading, getCompetitionList, loadMore, getCompetition }
})
