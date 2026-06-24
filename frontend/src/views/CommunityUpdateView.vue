<template>
    <div>
        <h1>게시글 수정</h1>
        <form @submit.prevent="updateArticle()">
        <label for="title" class="form-label">제목:</label>
        <input type="text" name="title" v-model="title" class="form-input">

        <label for="content" class="form-label">내용:</label>
        <textarea name="content" id="content" cols="30" rows="10" v-model="content" class="form-textarea"></textarea>
        <input type="submit" value="수정">
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCommunityStore } from '@/stores/communityStore';

const route = useRoute();
const communityStore = useCommunityStore();

const title = ref('')
const content = ref('')

onMounted(() => {
  title.value = communityStore.detailArticle.title
  content.value = communityStore.detailArticle.content
})

const updateArticle = function () {
  const article = {
    pk: route.params.pk,
    title: title.value,
    content: content.value,
  }
  communityStore.updateArticle(article)
}
</script>

<style lang="scss" scoped>

</style>
