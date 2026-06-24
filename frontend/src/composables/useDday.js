import { ref, watch, onUnmounted } from 'vue'

export function useDday(getDateStr) {
  const dday = ref('')
  let timer = null

  const start = (endDateStr) => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }

    if (!endDateStr) {
      dday.value = ''
      return
    }

    const target = new Date(`${endDateStr}T23:59:59+09:00`)

    const update = () => {
      const diff = target - new Date()
      if (diff <= 0) {
        dday.value = '마감'
        clearInterval(timer)
        timer = null
        return
      }
      const totalSeconds = Math.floor(diff / 1000)
      const days = Math.floor(totalSeconds / 86400)
      const hours = String(Math.floor((totalSeconds % 86400) / 3600)).padStart(2, '0')
      const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0')
      const seconds = String(totalSeconds % 60).padStart(2, '0')
      dday.value = `D-${days} ${hours}:${minutes}:${seconds}`
    }

    update()
    timer = setInterval(update, 1000)
  }

  watch(getDateStr, (val) => start(val), { immediate: true })

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

  return { dday }
}
