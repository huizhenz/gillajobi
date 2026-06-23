<template>
  <div>
    <form @submit.prevent="updateProfile">
      <div>
        <h2>기본 정보</h2>

        <div>
          <label for="profile_image">프로필 이미지</label>
          <input type="file" id="profile_image" accept="image/*" @change="onImageChange" />
        </div>

        <div>
          <label for="last_name">성</label>
          <input type="text" id="last_name" v-model.trim="last_name" />
        </div>

        <div>
          <label for="first_name">이름</label>
          <input type="text" id="first_name" v-model.trim="first_name" />
        </div>

        <div v-for="field in arrayFields" :key="field.key">
          <label>{{ field.label }}</label>
          <div>
            <span v-for="(item, index) in field.arr.value" :key="index">
              {{ item }}
              <button type="button" @click="removeItem(field.arr, index)">x</button>
            </span>
          </div>
          <input
            type="text"
            v-model="field.input.value"
            @keyup.enter.prevent="addItem(field.arr, field.input)"
            :placeholder="field.placeholder"
          />
          <button type="button" @click="addItem(field.arr, field.input)">추가</button>
        </div>

        <div>
          <label for="desired_salary">희망 연봉</label>
          <input type="text" id="desired_salary" v-model.trim="desired_salary" />
        </div>
      </div>

      <button type="submit">프로필 등록</button>
    </form>
    <div>
      <router-link to="/">나중에 등록하기</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from "@/stores/userStore.js";

const userStore = useUserStore();

onMounted(async () => {
  const data = await userStore.getProfile()
  if (!data) return

  first_name.value = data.user.first_name || ''
  last_name.value = data.user.last_name || ''
  education.value = data.profile.education || []
  certification.value = data.profile.certification || []
  experience.value = data.profile.experience || []
  language.value = data.profile.language || []
  preferred_location.value = data.profile.preferred_location || []
  preferred_position.value = data.profile.preferred_position || []
  desired_salary.value = data.profile.desired_salary || ''
})

const first_name = ref('')
const last_name = ref('')
const profile_image = ref(null)

const onImageChange = (e) => {
  profile_image.value = e.target.files[0] || null
}

const education = ref([])
const educationInput = ref('')

const certification = ref([])
const certificationInput = ref('')

const experience = ref([])
const experienceInput = ref('')

const language = ref([])
const languageInput = ref('')

const preferred_location = ref([])
const preferredLocationInput = ref('')

const preferred_position = ref([])
const preferredPositionInput = ref('')

const desired_salary = ref('')

const arrayFields = [
  { key: 'education', label: '학력', arr: education, input: educationInput, placeholder: '학력 입력 후 추가' },
  { key: 'certification', label: '자격증', arr: certification, input: certificationInput, placeholder: '자격증 입력 후 추가' },
  { key: 'experience', label: '경력', arr: experience, input: experienceInput, placeholder: '경력 입력 후 추가' },
  { key: 'language', label: '어학', arr: language, input: languageInput, placeholder: '어학 입력 후 추가' },
  { key: 'preferred_location', label: '희망 근무 지역', arr: preferred_location, input: preferredLocationInput, placeholder: '지역 입력 후 추가' },
  { key: 'preferred_position', label: '희망 직무', arr: preferred_position, input: preferredPositionInput, placeholder: '직무 입력 후 추가' },
]

const addItem = (arr, inputRef) => {
  if (inputRef.value.trim()) {
    arr.value.push(inputRef.value.trim())
    inputRef.value = ''
  }
}

const removeItem = (arr, index) => {
  arr.value.splice(index, 1)
}

const updateProfile = () => {
  const payload = {
    first_name: first_name.value,
    last_name: last_name.value,
    profile_image: profile_image.value,
    education: education.value,
    certification: certification.value,
    experience: experience.value,
    language: language.value,
    preferred_location: preferred_location.value,
    preferred_position: preferred_position.value,
    desired_salary: desired_salary.value
  }
  userStore.updateProfile(payload)
}
</script>

<style scoped>

</style>
