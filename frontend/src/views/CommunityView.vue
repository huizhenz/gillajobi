<template>
  <div class="community-wrap">
    <div class="community-header">
      <div class="community-title-group">
        <h1>커뮤니티</h1>
        <span class="community-subtitle">취업준비, 같이 하면 덜 외로워요. 후기와 꿀팁을 나눠보세요</span>
      </div>
      <RouterLink v-if="userstore.isLogin" :to="{name:'articleCreate'}" class="btn-create">+ 글쓰기</RouterLink>
    </div>
    <div v-if="userstore.isLogin">
    <div class="filter-bar">
      <button
        class="filter-btn"
        :class="{ active: selectedLabel === null }"
        @click="selectedLabel = null"
      >전체</button>
      <button
        v-for="lbl in store.labelList"
        :key="lbl.id"
        class="filter-btn label-btn"
        :class="{ active: selectedLabel === lbl.id }"
        :style="getLabelStyle(lbl.name)"
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
          <span class="label-badge" v-if="article.label_name" :style="getLabelStyle(article.label_name)">{{ article.label_name }}</span>
        </div>
        <h3 class="article-title">{{ article.title }}</h3>
        <div class="article-meta">
          <span>{{ article.created_at?.slice(0, 10) }} · {{ article.nickname }}</span>
          <span class="comment-count">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            {{ article.comment_count }}
          </span>
        </div>
      </div>
    </ul>
    </div>
    <div v-else class="gate-container">
      <div class="gate-blur">
        <div class="fake-card" v-for="n in 6" :key="n">
          <div class="fake-bar short"></div>
          <div class="fake-bar long"></div>
          <div class="fake-bar mid"></div>
        </div>
      </div>
      <div class="gate-overlay">
        <div class="gate-card">
          <p class="gate-title">로그인 후 이용가능합니다</p>
          <div class="gate-links">
            <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink>
            <span>|</span>
            <RouterLink :to="{ name: 'SignupView' }">회원가입</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { RouterLink, useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/communityStore';
import { useUserStore } from '@/stores/userStore';

const router = useRouter()
const store = useCommunityStore();
const userstore = useUserStore();
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

const labelColorMap = {
  '자격증':  { backgroundColor: '#E7EFFB', color: '#7AB8E8', borderColor: '#E7EFFB' },
  '부트캠프': { backgroundColor: '#FEF9E7', color: '#E8C04A', borderColor: '#FEF9E7' },
  '공모전':  { backgroundColor: '#F0FAF5', color: '#6EC49A', borderColor: '#F0FAF5' },
  '채용공고': { backgroundColor: '#FBEBE1', color: '#E55627', borderColor: '#FBEBE1' },
}

const getLabelStyle = (name) => labelColorMap[name] ?? {}
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

.community-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.community-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a1a;
}

.community-subtitle {
  font-size: 0.90rem;
  color: #999;
  margin-top: 10px;
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

.label-btn {
  font-weight: 600;
}

.label-btn.active {
  filter: brightness(0.88);
  font-weight: 700;
}

.label-btn:hover {
  filter: brightness(0.93);
  color: inherit;
  border-color: inherit;
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
  font-size: 0.75rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
}

.article-title {
  font-size: 1rem;
  font-weight: 600;
  color: #222;
  margin: 0 0 8px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  color: #888;
}

.comment-count {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #aaa;
  font-size: 0.8rem;
}

/* 비로그인 블러 게이트 */
.gate-container {
  position: relative;
}

.gate-blur {
  display: flex;
  flex-direction: column;
  gap: 12px;
  filter: blur(1px);
  pointer-events: none;
  user-select: none;
}

.fake-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.fake-bar {
  background: #e8e8e8;
  border-radius: 4px;
  height: 13px;
}
.fake-bar.short { width: 28%; }
.fake-bar.long  { width: 65%; }
.fake-bar.mid   { width: 18%; }

.gate-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gate-card {
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.14);
  padding: 44px 64px;
  text-align: center;
}

.gate-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 16px;
}

.gate-links {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  font-size: 0.95rem;
  color: #bbb;
}

.gate-links a {
  color: #2ab59e;
  text-decoration: none;
  font-weight: 600;
}

.gate-links a:hover {
  text-decoration: underline;
}

@media (max-width: 810px) {
  .community-wrap {
    margin: 20px auto;
    padding: 0 12px;
  }


  .article-card {
    padding: 14px 16px;
  }

  .gate-card {
    padding: 32px 28px;
    margin: 0 16px;
  }
}
</style>
