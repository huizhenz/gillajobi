<template>
    <div class="calendar-wrapper">

        <div class="calendar-header">
            <button @click="prevMonth">←</button>
            <h2>{{ currentYear }}년 {{ currentMonth }}월</h2>
            <button @click="nextMonth">→</button>
        </div>

        <div class="calendar-grid">
            <div class="day-label" v-for="day in ['월','화','수','목','금','토','일']" :key="day">
                {{ day }}
            </div>

            <div
                class="day-cell"
                :style="cell ? getRangeBgStyle(getDateKey(cell)) : {}"
                v-for="(cell, index) in calendarCells"
                :key="index"
            >
                <span v-if="cell">{{ cell }}</span>
                <template v-if="cell">
                    <div
                        class="event-badge"
                        v-for="(event, i) in eventMapFull[getDateKey(cell)]"
                        :key="i"
                        :style="getBadgeStyle(event.category)"
                        @mouseenter="onBadgeEnter(event)"
                        @mouseleave="onBadgeLeave(event)"
                        @click.stop="router.push({ name: event.routeName, params: event.routeParam })"
                    >
                        <span class="category-tag">{{ event.category[0] }}</span>
                        <span class="event-title">{{ event.title }}</span>
                    </div>
                </template>
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const router = useRouter()

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth() + 1)

const prevMonth = () => {
    if (currentMonth.value === 1) {
        currentMonth.value = 12
        currentYear.value--
    } else {
        currentMonth.value--
    }
}

const nextMonth = () => {
    if (currentMonth.value === 12) {
        currentMonth.value = 1
        currentYear.value++
    } else {
        currentMonth.value++
    }
}

const calendarCells = computed(() => {
    const firstDay = new Date(currentYear.value, currentMonth.value - 1, 1).getDay()
    const daysInMonth = new Date(currentYear.value, currentMonth.value, 0).getDate()
    
    // 월요일 시작이라 일요일(0)은 6으로 변환
    const startOffset = firstDay === 0 ? 6 : firstDay - 1
    
    const cells = Array(startOffset).fill(null) // 빈 칸
    for (let i = 1; i <= daysInMonth; i++) cells.push(i)
    const totalNeeded = Math.ceil(cells.length / 7) * 7
    while (cells.length < totalNeeded) cells.push(null) // 뒤 빈 칸
    
    return cells
})

const events = ref([])

const loadCalendarEvents = async () => {
    if (!userStore.isLogin) {
        console.log('[Calendar] 비로그인 상태')
        return
    }

    try {
        const profileRes = await axios.get('http://127.0.0.1:8000/api/v1/accounts/profile/', {
            headers: { Authorization: `Token ${userStore.token}` }
        })
        console.log('[Calendar] 프로필:', profileRes.data)

        const positions = profileRes.data.profile?.preferred_position ?? []
        const keyword = positions[0] ?? ''
        console.log('[Calendar] 희망직무 키워드:', keyword)
        if (!keyword) return

        const res = await axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
            params: { q: keyword }
        })
        console.log('[Calendar] 검색 결과:', res.data)

        const mapped = []

        res.data.jobs.slice(0, 5).forEach(item => {
            if (item.close_date) mapped.push({
                title: item.title,
                category: '채용공고',
                start: item.close_date,
                end: item.close_date,
                routeName: 'JobDetailView',
                routeParam: { jobPk: item.id },
            })
        })

        res.data.bootcamps.slice(0, 5).forEach(item => {
            if (item.close_date) mapped.push({
                title: item.title,
                category: '부트캠프',
                start: item.close_date,
                end: item.close_date,
                routeName: 'BootcampDetailView',
                routeParam: { bootcampPk: item.id },
            })
        })

        res.data.certifications.slice(0, 5).forEach(item => {
            if (item.exam_start && item.exam_end) mapped.push({
                title: item.name,
                category: '자격증',
                start: item.exam_start,
                end: item.exam_end,
                routeName: 'CertificationDetailView',
                routeParam: { jm_cd: item.jm_cd },
            })
        })

        res.data.competitions.slice(0, 5).forEach(item => {
            if (item.start_date) mapped.push({
                title: item.title,
                category: '공모전',
                start: item.start_date,
                end: item.end_date ?? item.start_date,
                routeName: 'CompetitionDetailView',
                routeParam: { competitionPk: item.id },
            })
        })

        events.value = mapped
    } catch (err) {
        console.error('[Calendar] 데이터 로딩 실패:', err.message)
        console.error('[Calendar] 상태코드:', err.response?.status)
        console.error('[Calendar] 응답:', err.response?.data)
    }
}

onMounted(() => {
    loadCalendarEvents()
})

const eventMapFull = computed(() => {
    const map = {}
    events.value.forEach(event => {
        if (!map[event.end]) map[event.end] = []
        map[event.end].push(event)
    })
    return map
})

const categoryColorMap = {
    '자격증':  { backgroundColor: '#E7EFFB', color: '#7AB8E8' },
    '부트캠프': { backgroundColor: '#FEF9E7', color: '#E8C04A' },
    '공모전':  { backgroundColor: '#F0FAF5', color: '#6EC49A' },
    '채용공고': { backgroundColor: '#FBEBE1', color: '#E55627' },
}

const getBadgeStyle = (category) => categoryColorMap[category] ?? { backgroundColor: '#eee', color: '#888' }

// hover 추적: Set으로 여러 이벤트 동시 hover 지원
const hoveredEvents = ref(new Set())
const leaveTimers = new Map()

const onBadgeEnter = (event) => {
    if (leaveTimers.has(event)) {
        clearTimeout(leaveTimers.get(event))
        leaveTimers.delete(event)
    }
    hoveredEvents.value = new Set([...hoveredEvents.value, event])
}

const onBadgeLeave = (event) => {
    const timer = setTimeout(() => {
        const next = new Set(hoveredEvents.value)
        next.delete(event)
        hoveredEvents.value = next
        leaveTimers.delete(event)
    }, 40)
    leaveTimers.set(event, timer)
}

const getRangeBgStyle = (dateKey) => {
    const matching = [...hoveredEvents.value].filter(
        e => dateKey >= e.start && dateKey <= e.end
    )
    if (matching.length === 0) return {}
    if (matching.length === 1) {
        return { backgroundColor: categoryColorMap[matching[0].category]?.backgroundColor }
    }
    const colors = matching.map(e => categoryColorMap[e.category]?.backgroundColor).filter(Boolean)
    return { background: `linear-gradient(135deg, ${colors.join(', ')})` }
}


const getDateKey = (day) => {
    const month = String(currentMonth.value).padStart(2, '0')
    const d = String(day).padStart(2, '0')
    return `${currentYear.value}-${month}-${d}`
}
</script>

<style lang="scss" scoped>
$teal: #2ab59e;

.calendar-wrapper {
    background: white;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;

    h2 {
        font-size: 18px;
        font-weight: 700;
        color: #111;
    }

    button {
        background: none;
        border: 1px solid #e0e0e0;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        cursor: pointer;
        font-size: 14px;
        color: #555;

        &:hover {
            background: #f5f5f5;
        }
    }
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
}

.day-label {
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: #888;
    padding: 8px 0 16px;
}

.day-cell {
    min-height: 80px;
    min-width: 0;
    padding: 6px;
    border-radius: 8px;
    font-size: 13px;
    color: #333;

    &:hover {
        background: #f9f9f9;
    }

    span {
        display: block;
        font-weight: 500;
    }

}

.event-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 4px;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    overflow: hidden;

    span + & {
        white-space: nowrap;
    }
}

.category-tag {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    background: rgba(0, 0, 0, 0.08);
    border-radius: 3px;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
}

.event-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
    min-width: 0;
}

@media (max-width: 810px) {
  .calendar-wrapper {
    padding: 16px 12px;
  }

  .day-cell {
    min-height: 48px;
    padding: 4px;
    font-size: 11px;
  }

  .event-badge {
    font-size: 9px;
    padding: 1px 4px;

    .category-tag {
      display: none;
    }
  }

  .calendar-header h2 {
    font-size: 15px;
  }
}
</style>