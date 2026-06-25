<template>
  <form class="comment-form" @submit.prevent="createComment">
    <input type="text" name="content" id="content" v-model="content" placeholder="댓글을 입력하세요" class="comment-input">
    <button class="btn-submit">작성</button>
  </form>
</template>

<script setup>
import { useCommentStore } from '@/stores/comments.js'
import { ref } from 'vue';
const store = useCommentStore()
const props = defineProps({
  articlePk: Number
})
const content = ref('')
const createComment = function () {
  if (!content.value.trim()) return
  store.commentCreate(props.articlePk, content.value)
  content.value = ''
}
</script>

<style scoped>
.comment-form {
  display: flex;
  gap: 8px;
}

.comment-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.comment-input:focus {
  border-color: #2ab59e;
}

.btn-submit {
  background-color: #2ab59e;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s;
}

.btn-submit:hover {
  background-color: #239e8a;
}
</style>