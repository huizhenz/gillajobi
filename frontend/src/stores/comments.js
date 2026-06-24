import axios from 'axios'
import { defineStore } from 'pinia'
import { useCommunityStore } from './communityStore.js'
import { useUserStore } from './userStore.js'

export const useCommentStore = defineStore('comment', () => {
  const commentCreate = function (articlePk, content) {
    const userStore = useUserStore()
    const communityStore = useCommunityStore()
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/community/articles/${articlePk}/comments/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
      data: { content }
    })
    .then(res => communityStore.detailArticle.comments.push(res.data))
    .catch(err => console.log(err))
  }

  const commentDelete = function (commentPk) {
    const userStore = useUserStore()
    const communityStore = useCommunityStore()
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v1/community/comments/${commentPk}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      },
    })
    .then(() => {
      communityStore.detailArticle.comments = communityStore.detailArticle.comments.filter(
        (comment) => comment.id !== commentPk
      )
    })
    .catch(err => console.log(err))
  }

  return { commentCreate, commentDelete }
})
