<template>
    <div class="calendar-wrapper">

        <!-- 헤더 -->
        <div class="calendar-header">
            <button @click="prevMonth">←</button>
            <h2>2026년 6월</h2>
            <button @click="nextMonth">→</button>
        </div>

        <!-- 요일 행 -->
        <div class="calendar-grid">
            <div class="day-label" v-for="day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']" :key="day">
                {{ day }}
            </div>

            <!-- 날짜 셀 42칸 -->
            <div class="day-cell" v-for="(cell, index) in calendarCells" :key="index">
                <span v-if="cell">{{ cell }}</span>
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
</style>