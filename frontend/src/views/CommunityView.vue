<template>
  <div class="community-wrap">
    <div class="community-header">
      <h1>커뮤니티</h1>
      <RouterLink :to="{name:'articleCreate'}" class="btn-create">+ 글쓰기</RouterLink>
    </div>

    <div class="filter-bar">
      <button
        class="filter-btn"
        :class="{ active: selectedLabel === null }"
        @click="selectedLabel = null"
      >전체</button>
      <button
        v-for="lbl in store.labelList"
        :key="lbl.id"
        class="filter-btn"
        :class="{ active: selectedLabel === lbl.id }"
        @click="selectedLabel = lbl.id"
      >{{ lbl.name }}</button>
    </div>

    <ul class="article-list">
      <div
          v-for="article in filteredArticles"
          :key="article.id"
          class="article-card"
          @click="goDetail(article.id)"
        >
        <div class="article-card-top">
          <span class="label-badge" v-if="article.label_name">{{ article.label_name }}</span>
          <span class="article-id">#{{ article.id }}</span>
        </div>
        <h3 class="article-title">{{ article.title }} [{{ article.comment_count }}]</h3>
        <div class="article-meta">{{ article.username }}</div>
      </div>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/communityStore';

const router = useRouter()
const store = useCommunityStore();
const selectedLabel = ref(null)

onMounted(() => {
  store.getArticleList()
  store.getLabelList()
})

const filteredArticles = computed(() => {
  if (selectedLabel.value === null) return store.articleList
  return store.articleList.filter(article => article.label === selectedLabel.value)
})

const goDetail = (pk) => {
  router.push({name:'Articledetail', params:{pk: pk}})
}
</script>

<style scoped>
.community-wrap {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.community-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a1a;
}

.btn-create {
  background-color: #2ab59e;
  color: white;
  padding: 8px 18px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.btn-create:hover {
  background-color: #239e8a;
}

.filter-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-btn {
  background: #f0f0f0;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 0.88rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
}

.filter-btn:hover {
  border-color: #2ab59e;
  color: #2ab59e;
}

.filter-btn.active {
  background-color: #2ab59e;
  border-color: #2ab59e;
  color: white;
  font-weight: 600;
}

.article-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 16px 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}

.article-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.article-card-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.label-badge {
  background-color: #e6f7f5;
  color: #2ab59e;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
}

.article-id {
  font-size: 0.78rem;
  color: #aaa;
}

.article-title {
  font-size: 1rem;
  font-weight: 600;
  color: #222;
  margin: 0 0 8px;
}

.article-meta {
  font-size: 0.82rem;
  color: #888;
}
</style>
