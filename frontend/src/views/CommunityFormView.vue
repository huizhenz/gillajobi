<template>
  <div class="update-page">
    <div class="update-card">

      <div class="tab-bar">
        <span class="tab active">게시글 작성</span>
      </div>

      <div class="form-section">
        <form @submit.prevent="createArticle()">

          <div class="form-item">
            <label for="label" class="form-label">카테고리</label>
            <select id="label" v-model="selectedLabel" class="form-input">
              <option value="">카테고리 선택</option>
              <option v-for="lbl in communityStore.labelList" :key="lbl.id" :value="lbl.id">
                {{ lbl.name }}
              </option>
            </select>
          </div>

          <div class="form-item">
            <label for="title" class="form-label">제목</label>
            <input type="text" id="title" v-model="title" class="form-input" placeholder="제목을 입력하세요" />
          </div>

          <div class="form-item">
            <label for="content" class="form-label">내용</label>
            <textarea id="content" v-model="content" class="form-textarea" placeholder="내용을 입력하세요" rows="12"></textarea>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="$router.back()">취소</button>
            <button type="submit" class="btn-submit">작성하기</button>
          </div>

        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useCommunityStore } from '@/stores/communityStore';
import { onBeforeRouteLeave } from 'vue-router';

const communityStore = useCommunityStore();

const title = ref('')
const content = ref('')
const selectedLabel = ref('')

onMounted(() => {
  communityStore.getLabelList()
})

const isWriting = ref(false)

watch([title, content], ([t, c]) => {
  if (t || c) isWriting.value = true
})

const createArticle = function () {
  const article = {
    title: title.value,
    content: content.value,
    label: selectedLabel.value || null,
  }
  isWriting.value = false
  communityStore.createArticle(article)
}

onBeforeRouteLeave(() => {
  if (!isWriting.value) return true
  return window.confirm("작성중이던 게시글이 있습니다. 다른 경로로 이동시 작성중이던 내용은 소멸됩니다. 이동하시겠습니까?")
})
</script>

<style lang="scss" scoped>
$primary: #2ab59e;

.update-page {
  min-height: 100vh;
  padding: 40px 24px;
}

.update-card {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  font-size: 0.95rem;
  font-weight: 600;
  color: #bbb;

  &.active {
    font-size: 1.2rem;
  }

  &.active {
    color: $primary;
    border-bottom: 2px solid $primary;
  }
}

.form-section {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 1rem;
  color: #999;
  font-weight: 600;
  margin-top: 20px;
}

.form-item:first-child .form-label {
  margin-top: 0;
}

.form-input {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px 14px;
  margin-top: 10px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
  background: #fafafa;
  appearance: none;

  &::placeholder {
    color: #bbb;
  }

  &:focus {
    border-color: $primary;
    background: white;
  }
}

.form-textarea {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px 14px;
  margin-top: 10px;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
  background: #fafafa;
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;

  &::placeholder {
    color: #bbb;
  }

  &:focus {
    border-color: $primary;
    background: white;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel {
  background: none;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 0.88rem;
  color: #999;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #f5f5f5;
    color: #555;
  }
}

.btn-submit {
  background: $primary;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: #239e8a;
  }
}

@media (max-width: 810px) {
  .update-page {
    padding: 16px 12px;
  }

  .update-card {
    border-radius: 12px;
  }

  .tab-bar {
    padding: 0 16px;
  }

  .form-section {
    padding: 16px;
  }

  .form-actions {
    flex-direction: column-reverse;
    align-items: stretch;
    gap: 10px;
  }

  .btn-submit {
    width: 100%;
    text-align: center;
    padding: 14px;
  }

  .btn-cancel {
    width: 100%;
    text-align: center;
  }
}
</style>
