<template>
  <div class="profile-page">
    <div v-if="profileData" class="profile-layout">

      <!-- 왼쪽 패널 -->
      <div class="left-card">
        <div class="avatar-wrap">
          <img v-if="profileData.user.profile_image" :src="profileData.user.profile_image" class="avatar-img" />
          <div v-else class="avatar-circle">{{ avatarLetter }}</div>
        </div>
        <p class="name">{{ profileData.user.nickname }}</p>
        <p class="username">@{{ profileData.user.username }}</p>
        <div class="badge-list">
          <span v-for="(pos, i) in profileData.profile.preferred_position" :key="i" class="position-badge">
            희망 직무 · {{ pos }}
          </span>
        </div>
        <div class="todo-card">
          <span class="todo-label">완료한 To-do</span>
          <p class="todo-count">{{ todoStore.completedCount }}<span class="todo-unit">개</span></p>
          <div class="todo-progress-wrap">
            <div class="todo-progress-bar" :style="{ width: todoProgress + '%' }"></div>
          </div>
          <p class="todo-next">전체 {{ todoStore.todoList.length }}개 중 {{ todoStore.completedCount }}개 완료</p>
        </div>

      </div>

      <!-- 오른쪽 패널 -->
      <div class="right-card">
        <div class="tab-bar">
          <span class="tab" :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">개인정보</span>
          <span class="tab" :class="{ active: activeTab === 'articles' }" @click="activeTab = 'articles'">작성한 글</span>
        </div>

        <!-- 개인정보 탭 -->
        <div class="info-section" v-if="activeTab === 'info'">
          <div class="section-header">
            <h3>기본 정보</h3>
            <router-link :to="{ name: 'UpdateProfileView', params: { username: userStore.username } }" class="btn-edit">수정하기</router-link>
          </div>

          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">성명</span>
              <span class="info-value">{{ profileData.user.last_name }}{{ profileData.user.first_name }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">생년월일</span>
              <span class="info-value">{{ profileData.user.birth }}</span>
            </div>
            <div class="info-item full">
              <span class="info-label">학력</span>
              <span class="info-value">{{ profileData.profile.education?.join(', ') || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">희망 직무</span>
              <span class="info-value">{{ profileData.profile.preferred_position?.join(', ') || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">희망 분야</span>
              <span class="info-value">{{ profileData.profile.preferred_location?.join(', ') || '-' }}</span>
            </div>
            <div class="info-item full">
              <span class="info-label">희망 연봉</span>
              <span class="info-value">{{ profileData.profile.desired_salary ? profileData.profile.desired_salary + '만원' : '-' }}</span>
            </div>
            <div class="info-item full" v-if="profileData.profile.experience?.length">
              <span class="info-label">경력</span>
              <span class="info-value">{{ profileData.profile.experience.join(', ') }}</span>
            </div>
            <div class="info-item full" v-if="profileData.profile.certification?.length">
              <span class="info-label">자격증</span>
              <span class="info-value">{{ profileData.profile.certification.join(', ') }}</span>
            </div>
            <div class="info-item full" v-if="profileData.profile.language?.length">
              <span class="info-label">언어</span>
              <span class="info-value">{{ profileData.profile.language.join(', ') }}</span>
            </div>
          </div>
        </div>

        <!-- 작성한 글 탭 -->
        <div class="article-section" v-if="activeTab === 'articles'">
          <div v-if="myArticles.length === 0" class="no-articles">작성한 글이 없습니다.</div>
          <div
            v-for="article in myArticles"
            :key="article.id"
            class="my-article-card"
            @click="goDetail(article.id)"
          >
            <div class="my-article-top">
              <span class="label-badge" v-if="article.label_name" :style="getLabelStyle(article.label_name)">{{ article.label_name }}</span>
            </div>
            <h3 class="my-article-title">{{ article.title }}</h3>
            <div class="my-article-meta">
              <span>{{ article.created_at?.slice(0, 10) }}</span>
              <span class="comment-count">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                {{ article.comment_count }}
              </span>
            </div>
          </div>
        </div>

      </div>

    </div>
    <div v-else class="loading">프로필 정보를 불러오는 중...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useCommunityStore } from '@/stores/communityStore'
import { useTodoStore } from '@/stores/todoStore'

const userStore = useUserStore()
const communityStore = useCommunityStore()
const todoStore = useTodoStore()
const router = useRouter()

const profileData = ref(null)
const activeTab = ref('info')

const avatarLetter = computed(() => {
  const name = profileData.value?.user?.nickname || profileData.value?.user?.username || ''
  return name.charAt(0).toUpperCase()
})

const myArticles = computed(() =>
  communityStore.articleList.filter(a => a.username === userStore.username)
)

const goDetail = (pk) => {
  router.push({ name: 'Articledetail', params: { pk } })
}

const labelColorMap = {
  '자격증':  { backgroundColor: '#E7EFFB', color: '#7AB8E8', borderColor: '#E7EFFB' },
  '부트캠프': { backgroundColor: '#FEF9E7', color: '#E8C04A', borderColor: '#FEF9E7' },
  '공모전':  { backgroundColor: '#F0FAF5', color: '#6EC49A', borderColor: '#F0FAF5' },
  '채용공고': { backgroundColor: '#FBEBE1', color: '#E55627', borderColor: '#FBEBE1' },
}

const getLabelStyle = (name) => labelColorMap[name] ?? {}

const todoProgress = computed(() => {
  const total = todoStore.todoList.length
  if (!total) return 0
  return Math.round((todoStore.completedCount / total) * 100)
})


onMounted(async () => {
  profileData.value = await userStore.getProfile()
  communityStore.getArticleList()
  todoStore.getTodoList()
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.profile-page {
  margin-top: 20px;
  padding: 40px 24px;
}

.profile-layout {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

/* 왼쪽 카드 */
.left-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.avatar-wrap {
  margin-bottom: 8px;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #e6e6e6;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1a1a1a;
}

.username {
  font-size: 0.85rem;
  color: #999;
}

.badge-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 4px;
  align-items: center;
}

.position-badge {
  background: #e6f7f5;
  color: $primary;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}

/* 투두 카드 */
.todo-card {
  width: 100%;
  background: #2ab59e;
  border-radius: 14px;
  padding: 18px 20px;
  margin-top: 8px;
  color: white;
}

.todo-label {
  font-size: 0.90rem;
  font-weight: 600;
  opacity: 0.9;
  display: block;
  margin-bottom: 10px;
}

.todo-count {
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 12px;
}

.todo-unit {
  font-size: 1rem;
  font-weight: 600;
  margin-left: 2px;
}


.todo-progress-wrap {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  height: 6px;
  margin-bottom: 10px;
  overflow: hidden;
}

.todo-progress-bar {
  height: 100%;
  background: white;
  border-radius: 20px;
  transition: width 0.5s ease;
}

.todo-next {
  font-size: 0.78rem;
  opacity: 0.85;
}

/* 오른쪽 카드 */
.right-card {
  flex: 1;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  overflow: hidden;
}

.tab-bar {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 0 28px;
}

.tab {
  padding: 16px 4px;
  margin-right: 24px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #bbb;
  cursor: pointer;

  &.active {
    color: $primary;
    border-bottom: 2px solid $primary;
    font-size: 1.2rem;
  }

  &.disabled {
    cursor: default;
  }
}

.info-section {
  padding: 28px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a1a1a;
  }
}

.btn-edit {
  font-size: 0.85rem;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 6px 14px;
  text-decoration: none;
  transition: border-color 0.2s, color 0.2s;

  &:hover {
    border-color: $primary;
    color: $primary;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;

  &.full {
    grid-column: 1 / -1;
  }
}

.info-label {
  font-size: 16px;
  color: #999;
  font-weight: 600;
  margin-bottom: 10px;
}

.info-value {
  font-size: 16px;
  color: #1a1a1a;
  font-weight: 500;
}

.loading {
  text-align: center;
  color: #999;
  margin-top: 80px;
}

/* 작성한 글 탭 */
.article-section {
  padding: 20px 28px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.no-articles {
  font-size: 0.9rem;
  color: #bbb;
  text-align: center;
  padding: 40px 0;
}

.my-article-card {
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 16px 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }
}

.my-article-top {
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

.my-article-title {
  font-size: 1rem;
  font-weight: 600;
  color: #222;
  margin: 0 0 8px;
}

.my-article-meta {
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

/* 탭 cursor 통일 */
.tab {
  cursor: pointer;
}

@media (max-width: 810px) {
  .profile-page {
    padding: 20px 12px;
  }

  .profile-layout {
    flex-direction: column;
  }

  .left-card {
    width: 100%;
  }

  .right-card {
    width: 100%;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .info-item.full {
    grid-column: 1;
  }
}
</style>
