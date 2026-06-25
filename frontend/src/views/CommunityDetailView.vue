<template>
  <div class="detail-wrap">
    <div class="list-nav">
      <button class="btn-list" @click="router.push({ name: 'CommunityView' })">← 목록으로</button>
    </div>
    <div class="article-box">
      <div class="article-top">
        <span class="label-badge" v-if="store.detailArticle.label_name">{{ store.detailArticle.label_name }}</span>
        <span class="article-meta">{{ store.detailArticle.nickname }} · {{ store.detailArticle.created_at?.slice(0, 10) }}</span>
      </div>
      <h2 class="article-title">{{ store.detailArticle.title }}</h2>
      <hr class="article-divider" />
      <p class="article-content">{{ store.detailArticle.content }}</p>
      <div class="article-actions" v-if="store.detailArticle.username === userStore.username">
        <button class="btn-edit" @click="router.push({name:'articleUpdate', params:{pk:store.detailArticle.id}})">수정</button>
        <button class="btn-delete" @click="store.deleteArticle(store.detailArticle.id)">삭제</button>
      </div>
    </div>

    <div class="comment-section">
      <h3 class="comment-title">댓글</h3>
      <CommentCreate :articlePk="store.detailArticle.id"/>
      <ul class="comment-list">
        <CommentList
          v-for="comment in store.detailArticle.comments"
          :key="comment.id"
          :comment="comment"
        />
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCommunityStore } from '@/stores/communityStore.js';
import { useUserStore } from '@/stores/userStore.js';
import CommentCreate from '@/components/community/CommentCreate.vue';
import CommentList from '@/components/community/CommentList.vue';

const route = useRoute()
const router = useRouter()
const store = useCommunityStore();
const userStore = useUserStore();

onMounted(() => {
  store.getDetailArticle(route.params.pk)
})
</script>


<style scoped>
.detail-wrap {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.article-box {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 28px 32px;
  margin-bottom: 28px;
}

.article-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.label-badge {
  background-color: #e6f7f5;
  color: #2ab59e;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
}

.article-meta {
  font-size: 0.82rem;
  color: #999;
}

.article-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px;
}

.article-divider {
  border: none;
  border-top: 1px solid #f0f0f0;
  margin: 16px 0;
}

.article-content {
  font-size: 1rem;
  color: #333;
  line-height: 1.7;
  min-height: 80px;
  white-space: pre-wrap;
}

.article-actions {
  display: flex;
  gap: 8px;
  margin-top: 20px;
  justify-content: flex-end;
}

.btn-edit {
  background: #f0f0f0;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
}

.btn-edit:hover {
  background: #e0e0e0;
}

.btn-delete {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
}

.btn-delete:hover {
  background: #fecaca;
}

.comment-section {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
}

.comment-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 16px;
}

.comment-list {
  list-style: none;
  padding: 0;
  margin: 16px 0 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.list-nav {
  margin-bottom: 16px;
}

.btn-list {
  background: none;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 7px 16px;
  font-size: 0.88rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-list:hover {
  background: #f5f5f5;
  color: #2ab59e;
  border-color: #2ab59e;
}
</style>
