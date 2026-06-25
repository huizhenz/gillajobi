import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const BASE_URL = 'http://127.0.0.1:8000/api/v1/ai_score'

// 프론트 type → 백엔드 API type
const TYPE_MAP = {
  jobs: 'job',
  bootcamps: 'bootcamp',
  certifications: 'certification',
  competitions: 'competition',
}

// 카테고리별 상세 페이지 라우터 링크 생성
const getDetailLink = (type, item) => {
  if (type === 'jobs') return `/jobs/${item.id}`
  if (type === 'bootcamps') return `/bootcamp/${item.id}`
  if (type === 'certifications') return `/certification/${item.jm_cd}`
  if (type === 'competitions') return `/competition/${item.id}`
  return '/'
}

export const useAiScoreStore = defineStore('aiScore', () => {
  // 타입별 상태
  const state = ref({
    jobs: { items: [], status: null, loading: false },
    bootcamps: { items: [], status: null, loading: false },
    certifications: { items: [], status: null, loading: false },
    competitions: { items: [], status: null, loading: false },
  })

  const singleScores = ref({}) // key: "type:id"

  const getRecommendations = async (type) => {
    const userStore = useUserStore()
    if (!userStore.isLogin) {
      state.value[type].status = 'not_logged_in'
      return
    }

    const apiType = TYPE_MAP[type]
    if (!apiType) return

    state.value[type].loading = true
    try {
      const res = await axios.get(`${BASE_URL}/recommendations/`, {
        params: { type: apiType },
        headers: { Authorization: `Token ${userStore.token}` },
      })
      const data = res.data
      state.value[type].status = data.status
      state.value[type].items = (data.items || []).map(item => ({
        ...item,
        link: getDetailLink(type, item),
      }))
    } catch (e) {
      console.error('[aiScoreStore] recommendations 오류:', e)
      state.value[type].status = 'error'
    } finally {
      state.value[type].loading = false
    }
  }

  const pollUntilReady = async (type, maxRetries = 10) => {
    for (let i = 0; i < maxRetries; i++) {
      await new Promise(resolve => setTimeout(resolve, 3000))
      await getRecommendations(type)
      const s = state.value[type].status
      if (s === 'ready' || s === 'no_match' || s === 'error') return
      if (s !== 'computing') return
    }
    // 최대 재시도 후에도 computing이면 timeout 처리
    if (state.value[type].status === 'computing') {
      state.value[type].status = 'error'
    }
  }

  const getSingleScore = async (type, id) => {
    const userStore = useUserStore()
    if (!userStore.isLogin) return

    const key = `${type}:${id}`
    if (singleScores.value[key] !== undefined) return

    const apiType = TYPE_MAP[type]
    if (!apiType) return

    try {
      const res = await axios.get(`${BASE_URL}/score/`, {
        params: { type: apiType, id },
        headers: { Authorization: `Token ${userStore.token}` },
      })
      singleScores.value[key] = res.data
    } catch (e) {
      singleScores.value[key] = { score: null }
    }
  }

  const getScore = (type, id) => singleScores.value[`${type}:${id}`] ?? null

  return {
    state,
    singleScores,
    getRecommendations,
    pollUntilReady,
    getSingleScore,
    getScore,
  }
})
