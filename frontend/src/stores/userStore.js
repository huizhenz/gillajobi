import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from "axios";
import router from '@/router'


export const useUserStore = defineStore('user', () => {
    const BASE_URL = 'http://localhost:8000/api/v1/accounts'
    const token = ref('')


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
            router.push({ name: 'UpdateProfileView' })
        }).catch(error => {
            console.log(error);
        });
    }

    const logIn = (payload) => {
        axios({
            url: `${BASE_URL}/login/`,
            method: 'POST',
            data: {
                username: payload.username,
                password: payload.password
            }
        }).then(response => {
            console.log(response);
            token.value = response.data.key;
        }).catch(error => {
            console.log(error);
        });
    }

    const isLogin = computed(() => {
        return token.value ? true : false
    })

    const logOut = function () {
        axios({
            method: 'post',
            url: `${BASE_URL}/logout/`,
            headers: {
                Authorization: `Token ${token.value}`
            }
        })
        .then(res => {
            token.value = null
            // 로그아웃하면 로그인 화면으로 이동
            // router.push({ name: 'LogInView' })
        })
        .catch(err => console.log(err))
    }


    return {
        BASE_URL,
        token,
        isLogin,
        signUp,
        logIn,
        logOut,
    }
}, { persist: true })
