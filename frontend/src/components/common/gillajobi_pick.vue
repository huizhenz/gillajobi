<template>
  <div class="pick-wrapper">
    <h2 class="pick-title">🏆 길라잡이 Pick! {{ LABEL[props.type] }}</h2>
    <hr class="pick-divider">
    <div class="pick-list">
      <router-link
        v-for="(item, index) in top3"
        :key="item.id"
        :to="config.getLink(item)"
        class="pick-card"
      >
        <div class="card-header">
          <div class="card-top">
            <p class="subtitle">{{ config.getSubtitle(item) }}</p>
            <p class="title">{{ config.getTitle(item) }}</p>
          </div>
          <span class="rank" :class="`rank-${index + 1}`">{{ index + 1 }}</span>
        </div>
        <div class="card-bottom">
          <span class="category">{{ config.getCategory(item) }}</span>
          <span class="view-count">👁 {{ (item.view_count ?? 0).toLocaleString() }}</span>
        </div>
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
    getCategory: item => item['category__name'] ?? '',
    getLink: item => `/jobs/${item.id}`,
  },
  bootcamps: {
    url: `${BASE}/bootcamps/top3/`,
    getTitle: item => item.title,
    getSubtitle: item => item.company ?? '',
    getCategory: item => item['category__name'] ?? '',
    getLink: item => `/bootcamp/${item.id}`,
  },
  certifications: {
    url: `${BASE}/certifications/top3/`,
    getTitle: item => item.name,
    getSubtitle: item => item.series_name ?? '',
    getCategory: item => item.major_job_field ?? '',
    getLink: item => `/certification/${item.jm_cd}`,
  },
  competitions: {
    url: `${BASE}/competitions/top3/`,
    getTitle: item => item.title,
    getSubtitle: item => item.host ?? '',
    getCategory: item => item['category__name'] ?? '',
    getLink: item => `/competition/${item.id}`,
  },
}

const LABEL = {
  jobs: '채용공고',
  bootcamps: '부트캠프',
  certifications: '자격증',
  competitions: '공모전',
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
  font-size: 22px;
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
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  min-width: 0;
}

.card-top {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
  flex: 1;
}

.subtitle {
  font-size: 0.83rem;
  color: #888;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.title {
  font-size: 0.99rem;
  font-weight: 600;
  color: #222;
  margin: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 0.94rem;
  font-weight: 700;
  flex-shrink: 0;

  &.rank-1 { background: #FFD700; color: #7a5800; }
  &.rank-2 { background: #C0C0C0; color: #555; }
  &.rank-3 { background: #cd7f32; color: #fff; }
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  font-size: 0.83rem;
  color: #2ab59e;
  font-weight: 500;
}

.view-count {
  font-size: 0.86rem;
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
