import BootcampView from '@/views/BootcampView.vue'
import CalenderView from '@/views/CalenderView.vue'
import CertificationView from '@/views/CertificationView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CompetitionView from '@/views/CompetitionView.vue'
import JobView from '@/views/JobView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SignupView from '@/views/SignupView.vue'
import { createRouter, createWebHistory } from 'vue-router'


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
      component: SignupView,
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/jobs',
      name: 'JobView',
      component: JobView,
    },
    {
      path: '/competition',
      name: 'CompetitionView',
      component: CompetitionView,
    },
    {
      path: '/community',
      name: 'CommunityView',
      component: CommunityView,
    },
    {
      path: '/certification',
      name: 'CertificationView',
      component: CertificationView,
    },
    {
      path: '/calender',
      name: 'CalenderView',
      component: CalenderView,
    },
    {
      path: '/bootcamp',
      name: 'BootcampView',
      component: BootcampView,
    },        
  ],
})

export default router
