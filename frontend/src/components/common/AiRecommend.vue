<template>
  <div class="ai-recommend-wrapper">
    <h2 class="ai-recommend-title">✨ AI 추천 {{ LABEL[type] }}</h2>
    <hr class="ai-recommend-divider">
    <div class="ai-recommend-content">
      <!-- AI 추천 내용 -->
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  type: {
    type: String,
    required: true,
  },
})

const LABEL = {
  jobs: '채용공고',
  bootcamps: '부트캠프',
  certifications: '자격증',
  competitions: '공모전',
}

const { type } = props
</script>

<style lang="scss" scoped>
.ai-recommend-wrapper {
  padding: 20px 0;
}

.ai-recommend-title {
  font-size: 22px;
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
