<template>
    <div class="calendar-wrapper">

        <div class="calendar-header">
            <button @click="prevMonth">←</button>
            <h2>2026년 6월</h2>
            <button @click="nextMonth">→</button>
        </div>

        <div class="calendar-grid">
            <div class="day-label" v-for="day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']" :key="day">
                {{ day }}
            </div>

            <div
                class="day-cell"
                :class="{ highlighted: cell && isInRange(cell) }"
                v-for="(cell, index) in calendarCells"
                :key="index"
            >
                <span v-if="cell">{{ cell }}</span>
                <template v-if="cell">
                    <div
                        class="event-badge"
                        v-for="(event, i) in eventMapFull[getDateKey(cell)]"
                        :key="i"
                        @mouseenter="hoveredEvent = event"
                        @mouseleave="hoveredEvent = null"
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
import { ref, computed } from 'vue'

const currentYear = ref(2026)
const currentMonth = ref(6) // 6월

const calendarCells = computed(() => {
    const firstDay = new Date(currentYear.value, currentMonth.value - 1, 1).getDay()
    const daysInMonth = new Date(currentYear.value, currentMonth.value, 0).getDate()
    
    // 월요일 시작이라 일요일(0)은 6으로 변환
    const startOffset = firstDay === 0 ? 6 : firstDay - 1
    
    const cells = Array(startOffset).fill(null) // 빈 칸
    for (let i = 1; i <= daysInMonth; i++) cells.push(i)
    while (cells.length < 42) cells.push(null) // 뒤 빈 칸
    
    return cells
})

const events = ref([
    { title: '2026 부트캠프', category: '부트캠프', start: '2026-06-10', end: '2026-06-24' },
    { title: '2026 희망청년 공모전', category: '공모전', start: '2026-05-28', end: '2026-06-01' },
    { title: '2026 ai 해커톤', category: '공모전', start: '2026-06-10', end: '2026-06-15' },
    { title: '2026 sk 하이닉스 수시채용', category: '채용공고', start: '2026-06-27', end: '2026-06-30' },
    { title: '2026 SQLD 60회', category: '자격증', start: '2026-06-20', end: '2026-06-28' },
])

const eventMap = computed(() => {
    const map = {}
    events.value.forEach(event => {
        if (!map[event.end]) map[event.end] = []
        map[event.end].push(event.title)
    })
    return map
})

const eventMapFull = computed(() => {
    const map = {}
    events.value.forEach(event => {
        if (!map[event.end]) map[event.end] = []
        map[event.end].push(event)
    })
    return map
})

const hoveredEvent = ref(null)

const isInRange = (day) => {
    if (!hoveredEvent.value) return false
    const dateKey = getDateKey(day)
    return dateKey >= hoveredEvent.value.start && dateKey <= hoveredEvent.value.end
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
    padding: 24px;
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
    padding: 8px 0;
}

.day-cell {
    min-height: 72px;
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

    &.highlighted {
    background: rgba(42, 181, 158, 0.12);
}
}

.event-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 4px;
    padding: 2px 6px;
    background: $teal;
    color: white;
    border-radius: 4px;
    font-size: 11px;
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
    background: rgba(255, 255, 255, 0.3);
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
</style>