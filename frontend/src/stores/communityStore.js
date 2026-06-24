import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import router from '@/router'
import { useUserStore } from '@/stores/userStore'

export const useCommunityStore = defineStore('community', () => {
  const labelList = ref([])
  const getLabelList = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/community/labels/'
    })
    .then(res => labelList.value = res.data)
    .catch(err => console.log(err))
  }

  const articleList = ref([])
  const getArticleList = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/community/articles/'
    })
    .then(res => articleList.value = res.data)
    .catch(err => console.log(err))
  }
  const detailArticle = ref([])
  const getDetailArticle = function (pk) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/community/articles/${pk}/`
    })
    .then(res => detailArticle.value = res.data)
    .catch(err => console.log(err))
  }

  const createArticle = function ({title, content, label}) {
    const userStore = useUserStore()
    return axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/community/articles/',
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        title,
        content,
        label
      }
    })
    .then(() => router.push({ name: 'CommunityView' }))
    .catch(err => console.log(err))
  }

  const updateArticle = function ({pk, title, content}) {
    const userStore = useUserStore()
    return axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v1/community/articles/${pk}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: {
        title,
        content
      }
    })
    .then(() => router.push({ name: 'Articledetail', params: { pk } }))
    .catch(err => console.log(err))
  }

  const deleteArticle = function (pk) {
    const userStore = useUserStore()
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/community/articles/${pk}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
    })
    .then(() => router.push({name:'CommunityView'}))
    .catch(err => console.log(err))
  }
  return { labelList, getLabelList, articleList, getArticleList, detailArticle, getDetailArticle, createArticle, deleteArticle, updateArticle }
})