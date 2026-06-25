<template>
  <div class="pick-wrapper">
    <h2 class="pick-title">🏆 길라잡이 Pick! 채용공고</h2>
    <hr class="pick-divider">
    <div class="pick-list">
      <router-link
        v-for="(item, index) in top3"
        :key="item.id"
        :to="config.getLink(item)"
        class="pick-card"
      >
        <span class="rank" :class="`rank-${index + 1}`">{{ index + 1 }}</span>
        <div class="pick-info">
          <p class="subtitle">{{ config.getSubtitle(item) }}</p>
          <p class="title">{{ config.getTitle(item) }}</p>
        </div>
        <span class="view-count">👁 {{ (item.view_count ?? 0).toLocaleString() }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
})

const BASE = 'http://127.0.0.1:8000/api/v1'

const TYPE_CONFIG = {
  jobs: {
    url: `${BASE}/jobs/top3/`,
    getTitle: item => item.title,
    getSubtitle: item => item['company__name'] ?? '',
    getLink: item => `/jobs/${item.id}`,
  },
  bootcamps: {
    url: `${BASE}/bootcamps/top3/`,
    getTitle: item => item.title,
    getSubtitle: item => item.company ?? '',
    getLink: item => `/bootcamp/${item.id}`,
  },
  certifications: {
    url: `${BASE}/certifications/top3/`,
    getTitle: item => item.name,
    getSubtitle: item => item.series_name ?? '',
    getLink: item => `/certification/${item.jm_cd}`,
  },
  competitions: {
    url: `${BASE}/competitions/top3/`,
    getTitle: item => item.title,
    getSubtitle: item => item.host ?? '',
    getLink: item => `/competition/${item.id}`,
  },
}

const config = TYPE_CONFIG[props.type]
const top3 = ref([])

onMounted(() => {
  axios.get(config.url)
    .then(res => { top3.value = res.data })
    .catch(err => console.error(err))
})
</script>

<style lang="scss" scoped>
.pick-wrapper {
  padding: 20px 0;
}

.pick-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 8px;
}

.pick-divider {
  border: none;
  border-top: 2px solid #2ab59e;
  margin: 0 0 16px;
}

.pick-list {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.pick-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  height: 200px;
  box-sizing: border-box;
  background: #fff;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s;
  min-width: 0;

  &:hover {
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  }
}

.rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 700;
  flex-shrink: 0;

  &.rank-1 { background: #FFD700; color: #7a5800; }
  &.rank-2 { background: #C0C0C0; color: #555; }
  &.rank-3 { background: #cd7f32; color: #fff; }
}

.pick-info {
  flex: 1;
  min-width: 0;

  .subtitle {
    font-size: 0.75rem;
    color: #888;
    margin: 0 0 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #222;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.view-count {
  font-size: 0.78rem;
  color: #aaa;
  flex-shrink: 0;
}

@media (max-width: 810px) {
  .pick-list {
    flex-direction: column;
  }

  .pick-card {
    flex: 1 1 100%;
    height: 200px;
  }
}
</style>
