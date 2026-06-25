import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import router from '@/router'


export const useUserStore = defineStore('user', () => {
    const BASE_URL = 'http://localhost:8000/api/v1/accounts'
    const token = ref('')
    const username = ref('')
    const nickname = ref('')


    const signUp = (payload) => {
        const formData = new FormData()
        formData.append('username', payload.username)
        formData.append('email', payload.email)
        formData.append('password1', payload.password1)
        formData.append('password2', payload.password2)
        formData.append('nickname', payload.nickname)
        formData.append('gender', payload.gender)
        if (payload.birth) {
            formData.append('birth', payload.birth)
        }
        if (payload.profile_image) {
            formData.append('profile_image', payload.profile_image)
        }
        return axios({
            url: `${BASE_URL}/registration/`,
            method: 'POST',
            data: formData,
        }).then(response => {
            console.log(response);
            token.value = response.data.key;
            username.value = payload.username;
            nickname.value = payload.nickname;
            router.push({ name: 'UpdateProfileView', params: { username: username.value } })
        }).catch(error => {
            console.log(error.response.data);
            throw error;
        });
    }

    const logIn = (payload) => {
        return axios({
            url: `${BASE_URL}/login/`,
            method: 'POST',
            data: {
                username: payload.username,
                password: payload.password
            }
        }).then(async response => {
            console.log(response);
            token.value = response.data.key;
            username.value = payload.username;
            const profile = await getProfile()
            if (profile) nickname.value = profile.user.nickname
            router.push({ name: 'MainView' })
        }).catch(error => {
            console.log(error);
            throw error;
        });
    }

    const isLogin = computed(() => {
        return token.value ? true : false
    })

    const clearAuth = () => {
        token.value = null
        username.value = null
        nickname.value = null
    }

    const logOut = function () {
        axios({
            method: 'post',
            url: `${BASE_URL}/logout/`,
            headers: {
                Authorization: `Token ${token.value}`
            }
        })
        .then(() => {
            clearAuth()
            router.push({ name: 'MainView' })
        })
        .catch(err => {
            console.log(err)
            clearAuth()
            router.push({ name: 'MainView' })
        })
    }

    const getProfile = () => {
        return axios({
            url: `${BASE_URL}/profile/`,
            method: 'GET',
            headers: {
                Authorization: `Token ${token.value}`
            }
        }).then(response => {
            return response.data
        }).catch(error => {
            console.log(error);
            if (error.response?.status === 401) {
                clearAuth()
            }
            return null
        });
    }

    const initAuth = async () => {
        if (!token.value) return
        const profile = await getProfile()
        if (profile) {
            nickname.value = profile.user.nickname
            username.value = profile.user.username
        }
    }

    const updateProfile = (payload) => {
        const formData = new FormData()
        if (payload.first_name) formData.append('first_name', payload.first_name)
        if (payload.last_name) formData.append('last_name', payload.last_name)
        if (payload.profile_image) formData.append('profile_image', payload.profile_image)
        formData.append('education', JSON.stringify(payload.education))
        formData.append('certification', JSON.stringify(payload.certification))
        formData.append('experience', JSON.stringify(payload.experience))
        formData.append('language', JSON.stringify(payload.language))
        formData.append('preferred_location', JSON.stringify(payload.preferred_location))
        formData.append('preferred_position', JSON.stringify(payload.preferred_position))
        if (payload.desired_salary) formData.append('desired_salary', payload.desired_salary)
        return axios({
            url: `${BASE_URL}/profile/`,
            method: 'PATCH',
            headers: {
                Authorization: `Token ${token.value}`
            },
            data: formData,
        }).then(response => {
            console.log(response);
            router.push({ name: 'ProfileView', params: { username: username.value } })
        }).catch(error => {
            console.log(error);
        });
    }


    return {
        BASE_URL,
        token,
        username,
        nickname,
        isLogin,
        signUp,
        logIn,
        logOut,
        getProfile,
        updateProfile,
        initAuth,
        clearAuth,
    }
}, { persist: true })
