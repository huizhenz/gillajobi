<template>
    <div>
        <h1>게시글 생성 </h1>
        <form @submit.prevent="createArticle()">
        <label for="label" class="form-label">카테고리:</label>
        <select id="label" v-model="selectedLabel" class="form-input">
          <option value="">카테고리 선택</option>
          <option v-for="lbl in communityStore.labelList" :key="lbl.id" :value="lbl.id">
            {{ lbl.name }}
          </option>
        </select>

        <label for="title" class="form-label">제목:</label>
        <input type="text" name="title" v-model="title" class="form-input">

        <label for="content" class="form-label">내용:</label>
        <textarea name="content" id="content" cols="30" rows="10" v-model="content" class="form-textarea"></textarea>
        <input type="submit" value="create">
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCommunityStore } from '@/stores/communityStore';
// import { watch } from 'vue';
const communityStore = useCommunityStore();

const title = ref('')
const content = ref('')
const selectedLabel = ref('')

onMounted(() => {
  communityStore.getLabelList()
})

// watch(() => communityStore.detailArticle, (val) => {
//   pk.value = val.id
//   title.value = val.title
//   content.value = val.content
// })
const createArticle = function () {
  const article = {
    title: title.value,
    content: content.value,
    label: selectedLabel.value || null,
  }
  communityStore.createArticle(article)
}


</script>

<style lang="scss" scoped>

</style>