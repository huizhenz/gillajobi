<template>
  <div class="ai-recommend-wrapper">
    <h2 class="ai-recommend-title">✨ AI 추천 채용공고</h2>
    <hr class="ai-recommend-divider">
    <div class="ai-recommend-content">
      <!-- AI 추천 내용 -->
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    required: true,
  },
})
</script>

<style lang="scss" scoped>
.ai-recommend-wrapper {
  padding: 20px 0;
}

.ai-recommend-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #222;
  margin: 0 0 8px;
}

.ai-recommend-divider {
  border: none;
  border-top: 2px solid #2ab59e;
  margin: 0 0 16px;
}

.ai-recommend-content {
  min-height: 80px;
  // border: 1px solid #d0d0d0;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 0.9rem;
}
</style>
