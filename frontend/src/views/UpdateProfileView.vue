<template>
  <div class="update-page">
    <div class="update-card">

      <div class="tab-bar">
        <span class="tab active">프로필 수정</span>
      </div>

      <div class="form-section">
        <form @submit.prevent="updateProfile">

          <div class="section-header">
            <h3>기본 정보</h3>
          </div>

          <div class="info-grid">
            <div class="form-item">
              <label for="last_name" class="form-label">성</label>
              <input type="text" id="last_name" v-model.trim="last_name" class="form-input" />
            </div>

            <div class="form-item">
              <label for="first_name" class="form-label">이름</label>
              <input type="text" id="first_name" v-model.trim="first_name" class="form-input" />
            </div>

            <div class="form-item full">
              <label class="form-label">프로필 이미지</label>
              <div class="avatar-upload">
                <div class="avatar-preview">
                  <img v-if="imagePreview" :src="imagePreview" class="avatar-img" />
                  <div v-else class="avatar-placeholder">
                    <span>{{ (last_name || first_name) ? (last_name + first_name).charAt(0).toUpperCase() : '' }}</span>
                  </div>
                  <label for="profile_image" class="avatar-btn">+</label>
                </div>
                <input type="file" id="profile_image" accept="image/*" @change="onImageChange" class="hidden-file-input" />
              </div>
            </div>

            <div v-for="field in arrayFields" :key="field.key" class="form-item full">
              <label class="form-label">{{ field.label }}</label>
              <p v-if="field.key === 'preferred_position'" class="field-notice">* 반드시 1개 이상의 희망직무를 입력해주세요.</p>
              <div class="tag-input-row">
                <input
                  type="text"
                  v-model="field.input.value"
                  @keydown.enter.prevent="addItem(field.arr, field.input)"
                  :placeholder="field.placeholder"
                  :class="['form-input', { 'input-error': field.key === 'preferred_position' && positionError }]"
                />
                <button type="button" class="btn-add" @click="addItem(field.arr, field.input)">추가</button>
              </div>
              <div class="tag-list">
                <span v-for="(item, index) in field.arr.value" :key="index" class="tag">
                  {{ item }}
                  <button type="button" class="tag-remove" @click="removeItem(field.arr, index)">×</button>
                </span>
              </div>
              <p v-if="field.key === 'preferred_position' && positionError" class="error-msg">{{ positionError }}</p>
            </div>

            <div class="form-item full">
              <label for="desired_salary" class="form-label">희망 연봉</label>
              <div class="salary-wrap">
                <input type="text" id="desired_salary" v-model.trim="desired_salary" class="form-input" placeholder="숫자 입력" />
                <span class="salary-unit">만원</span>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <router-link :to="{ name: 'MainView' }" class="btn-skip">나중에 등록하기</router-link>
            <button type="submit" class="btn-submit">프로필 등록</button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
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
  if (data.user.profile_image) {
    imagePreview.value = data.user.profile_image
  }
})

const first_name = ref('')
const last_name = ref('')
const profile_image = ref(null)
const imagePreview = ref(null)

const onImageChange = (e) => {
  const file = e.target.files[0] || null
  profile_image.value = file
  if (file) {
    imagePreview.value = URL.createObjectURL(file)
  } else {
    imagePreview.value = null
  }
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
const positionError = ref('')

watch(preferred_position, (val) => {
  if (val.length > 0) positionError.value = ''
}, { deep: true })

const desired_salary = ref('')

const arrayFields = [
  { key: 'education', label: '학력', arr: education, input: educationInput},
  { key: 'certification', label: '자격증', arr: certification, input: certificationInput },
  { key: 'experience', label: '경력', arr: experience, input: experienceInput },
  { key: 'language', label: '어학', arr: language, input: languageInput },
  { key: 'preferred_location', label: '희망 근무 지역', arr: preferred_location, input: preferredLocationInput },
  { key: 'preferred_position', label: '희망 직무', arr: preferred_position, input: preferredPositionInput},
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
  if (preferred_position.value.length === 0) {
    positionError.value = '희망 직무를 입력하지 않으면 AI 추천 기능을 사용할 수 없습니다.'
    return
  }
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

<style lang="scss" scoped>
$primary: #2ab59e;

.update-page {
  min-height: 100vh;
  padding: 40px 24px;
}

.update-card {
  max-width: 720px;
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
    color: $primary;
    border-bottom: 2px solid $primary;
  }
}

.form-section {
  padding: 28px;
}

.section-header {
  margin-bottom: 24px;

  h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #1a1a1a;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px 32px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;

  &.full {
    grid-column: 1 / -1;
  }
}

.form-label {
  font-size: 0.9rem;
  color: #999;
  font-weight: 500;
}

.field-notice {
  font-size: 0.78rem;
  color: #e53935;
  margin: 2px 0 4px;
}

.form-input {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.92rem;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
  background: #fafafa;

  &::placeholder {
    color: #bbb;
  }

  &:focus {
    border-color: $primary;
    background: white;
  }
}

.hidden-file-input {
  display: none;
}

.avatar-upload {
  display: flex;
  align-items: center;
}

.avatar-preview {
  position: relative;
  width: 150px;
  height: 200px;
}

.avatar-img {
  width: 150px;
  height: 200px;
  border-radius: 5%;
  object-fit: cover;
  border: 2px solid #e0e0e0;
}

.avatar-placeholder {
  width: 150px;
  height: 200px;
  border-radius: 5%;
  background: #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: white;
}

.avatar-btn {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: $primary;
  color: white;
  font-size: 1.2rem;
  text-align: center;
  line-height: 22px;
  cursor: pointer;
  border: 2px solid white;
  display: block;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #e6f7f5;
  color: $primary;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.tag-remove {
  background: none;
  border: none;
  color: $primary;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;

  &:hover {
    color: #d00;
  }
}

.tag-input-row {
  display: flex;
  gap: 8px;
}

.input-error {
  border-color: #e53e3e !important;
  background: #fff5f5 !important;
}

.error-msg {
  font-size: 0.82rem;
  color: #e53e3e;
  margin: 4px 0 0;
}

.salary-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.salary-wrap .form-input {
  width: auto;
  flex: 1;
}

.salary-unit {
  font-size: 1.05rem;
  color: #999;
  white-space: nowrap;
}

.btn-add {
  background: #f0f0f0;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0 16px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;

  &:hover {
    background: #e0e0e0;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.btn-skip {
  font-size: 0.88rem;
  color: #999;
  text-decoration: none;

  &:hover {
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

  .info-grid {
    grid-template-columns: 1fr;
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

  .btn-skip {
    text-align: center;
  }
}
</style>
