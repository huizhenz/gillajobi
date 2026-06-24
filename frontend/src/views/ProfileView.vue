<template>
  <div>
    <div v-if="profileData">
      <h1>내 프로필</h1>

      <h2>기본 정보</h2>
      <p>아이디: {{ profileData.user.username }}</p>
      <p>닉네임: {{ profileData.user.nickname }}</p>
      <p>이메일: {{ profileData.user.email }}</p>
      <p>이름: {{ profileData.user.last_name }}{{ profileData.user.first_name }}</p>
      <p>성별: {{ profileData.user.gender }}</p>
      <p>생년월일: {{ profileData.user.birth }}</p>
      <div v-if="profileData.user.profile_image">
        <p>프로필 이미지:</p>
        <img :src="profileData.user.profile_image" alt="프로필 이미지" width="100">
      </div>

      <hr>

      <h2>프로필 정보</h2>

      <div v-if="profileData.profile.education?.length">
        <h3>학력</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.education" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.certification?.length">
        <h3>자격증</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.certification" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.experience?.length">
        <h3>경력</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.experience" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.language?.length">
        <h3>언어</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.language" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.preferred_location?.length">
        <h3>선호 지역</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.preferred_location" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.preferred_position?.length">
        <h3>선호 직무</h3>
        <ul>
          <li v-for="(item, idx) in profileData.profile.preferred_position" :key="idx">{{ item }}</li>
        </ul>
      </div>

      <div v-if="profileData.profile.desired_salary">
        <h3>희망 연봉</h3>
        <p>{{ profileData.profile.desired_salary }}</p>
      </div>

      <hr>
      <router-link :to="{ name: 'UpdateProfileView', params: { username: userStore.username } }">프로필 수정</router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const profileData = ref(null)

onMounted(async () => {
  profileData.value = await userStore.getProfile()
})
</script>

<style lang="scss" scoped>

</style>
