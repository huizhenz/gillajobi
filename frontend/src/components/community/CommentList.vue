<template>
  <li class="comment-item">
    <div class="comment-body">
      <span class="comment-user">{{ comment.username }}</span>
      <span class="comment-content">{{ comment.content }}</span>
    </div>
    <button v-if="comment.username === userStore.username" class="btn-delete" @click="commentDelete">🗑</button>
  </li>
</template>

<script setup>
import { useCommentStore } from '@/stores/comments'
import { useUserStore } from '@/stores/userStore'

const store = useCommentStore()
const userStore = useUserStore()

const props = defineProps({
  comment: Object
})

const commentDelete = () => {
  store.commentDelete(props.comment.id)
}
</script>

<style scoped>
.comment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9f9f9;
  border-radius: 8px;
  padding: 10px 14px;
}

.comment-body {
  display: flex;
  gap: 10px;
  align-items: baseline;
}

.comment-user {
  font-size: 0.82rem;
  font-weight: 700;
  color: #2ab59e;
  white-space: nowrap;
}

.comment-content {
  font-size: 0.9rem;
  color: #333;
}

.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.85rem;
  color: #bbb;
  padding: 2px 4px;
  transition: color 0.2s;
}

.btn-delete:hover {
  color: #dc2626;
}
</style>
