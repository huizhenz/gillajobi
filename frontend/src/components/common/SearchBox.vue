<script setup>
import { ref } from 'vue'
import { useSearchStore } from '@/stores/searchStore'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  label: {
    type: String,
    default: null,
  },
  extraParams: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['results'])

const searchStore = useSearchStore()
const router = useRouter()
const isLoading = ref(false)

const goToSearch = async () => {
  if (!searchStore.keyword.trim()) return

  if (!props.label) {
    router.push('/search')
    return
  }

  // 라벨 내 검색
  isLoading.value = true
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/category/search/', {
      params: { q: searchStore.keyword, label: props.label, ...props.extraParams },
    })
    emit('results', res.data[props.label])
    searchStore.keyword = ''
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

const clearSearch = () => {
  searchStore.keyword = ''
  emit('results', null)
}
</script>

<template>
  <form class="search-box" @submit.prevent="goToSearch">
    <input
      v-model="searchStore.keyword"
      type="text"
      placeholder="관심 직무를 검색해보세요."
      class="search-input"
    />
    <button v-if="searchStore.keyword && label" type="button" class="clear-btn" @click="clearSearch">✕</button>
    <button type="submit" class="search-btn" :disabled="isLoading">
      {{ isLoading ? '검색 중…' : '검색' }}
    </button>
  </form>
</template>

<style lang="scss" scoped>
$primary: #2ab59e;

.search-box {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
  border: 2px solid $primary;
  border-radius: 50px;
  overflow: hidden;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 7px 12px;
  font-size: 0.9rem;
  background: transparent;
  color: #222;

  &::placeholder {
    color: #aaa;
  }
}

.clear-btn {
  border: none;
  background: none;
  color: #aaa;
  font-size: 0.85rem;
  padding: 0 6px;
  cursor: pointer;
  line-height: 1;

  &:hover {
    color: #555;
  }
}

.search-btn {
  border: none;
  background: $primary;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 8px 16px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;

  &:hover:not(:disabled) {
    background: #239e8a;
  }

  &:disabled {
    opacity: 0.6;
    cursor: default;
  }
}
</style>
