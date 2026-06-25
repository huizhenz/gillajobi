import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import MainView from '@/views/MainView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'SignupView',
      component: () => import('@/views/SignupView.vue'),
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: () => import('@/views/ProfileView.vue'),
    },
    {
      path: '/profile/:username/update',
      name: 'UpdateProfileView',
      component: () => import('@/views/UpdateProfileView.vue'),
    },
    {
      path: '/login',
      name: 'LoginView',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/calendar',
      name: 'CalendarView',
      component: () => import('@/views/CalendarView.vue'),
    },
    {
      path: '/community',
      name: 'CommunityView',
      component: () => import('@/views/CommunityView.vue'),
    },
    {
      path: '/community/article',
      name: 'articleCreate',
      component: () => import('@/views/CommunityFormView.vue'),
    },
    {
      path: '/community/:pk',
      name: 'Articledetail',
      component: () => import('@/views/CommunityDetailView.vue'),
    },
    {
      path: '/community/:pk/update',
      name: 'articleUpdate',
      component: () => import('@/views/CommunityUpdateView.vue'),
    },
    {
      path: '/jobs',
      name: 'JobView',
      component: () => import('@/views/JobView.vue'),
    },
    {
      path: '/competition',
      name: 'CompetitionView',
      component: () => import('@/views/CompetitionView.vue'),
    },
    
    {
      path: '/certification',
      name: 'CertificationView',
      component: () => import('@/views/CertificationView.vue'),
    },
    {
      path: '/bootcamp',
      name: 'BootcampView',
      component: () => import('@/views/BootcampView.vue'),
    },
    {
      path: '/bootcamp/:bootcampPk',
      name: 'BootcampDetailView',
      component: () => import('@/views/BootcampDetailView.vue'),
    },
    {
      path: '/search',
      name: 'SearchView',
      component: () => import('@/views/SearchView.vue'),
    },
    {
      path: '/jobs/:jobPk',
      name: 'JobDetailView',
      component: () => import('@/views/JobDetailView.vue'),
    },
    {
      path: '/certification/:jm_cd',
      name: 'CertificationDetailView',
      component: () => import('@/views/CertificationDetailView.vue'),
    },
    {
      path: '/competition/:competitionPk',
      name: 'CompetitionDetailView',
      component: () => import('@/views/CompetitionDetailView.vue'),
    },
  ],
})

router.beforeEach((to, from) => {
  const userStore = useUserStore()

  if ((to.name === 'ProfileView' || to.name === 'UpdateProfileView' || to.name === 'CalendarView' || to.name === 'articleCreate' || to.name === 'Articledetail' || to.name === 'articleUpdate') && !userStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LoginView' }
  }
})

export default router
