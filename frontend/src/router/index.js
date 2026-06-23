import BootcampView from '@/views/BootcampView.vue'
import CalendarView from '@/views/CalendarView.vue'
import CertificationView from '@/views/CertificationView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CompetitionView from '@/views/CompetitionView.vue'
import JobView from '@/views/JobView.vue'
import LoginView from '@/views/LoginView.vue'
import MainView from '@/views/MainView.vue'
import ProfileView from '@/views/ProfileView.vue'
import UpdateProfileView from '@/views/UpdateProfileView.vue'
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
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView,
      children: [
        {
          path: 'update',
          name: 'UpdateProfileView',
          component: UpdateProfileView,
        }
      ]
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/calendar',
      name: 'CalendarView',
      component: CalendarView,
    },
    {
      path: '/community',
      name: 'CommunityView',
      component: CommunityView,
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
      path: '/certification',
      name: 'CertificationView',
      component: CertificationView,
    },
    {
      path: '/bootcamp',
      name: 'BootcampView',
      component: BootcampView,
    },
    {
      path: '/bootcamp/:bootcampPk',
      name: 'BootcampDetailView',
      component: () => import('@/views/BootcampDetailView.vue'),
    },
  ],
})

export default router
