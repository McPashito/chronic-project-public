import { createRouter, createWebHistory } from 'vue-router'

import PublicLayout from '@/layouts/PublicLayout.vue'
import PrivateLayout from '@/layouts/PrivateLayout.vue'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import DiabetesView from '@/views/DiabetesView.vue'
import ContactView from '@/views/ContactView.vue'
import RegisterView from '@/views/RegisterView.vue'
import DashboardView from '@/views/DashboardView.vue'
import GlucemiasView from '@/views/GlucemiasView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SettingsView from '@/views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: PublicLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: 'diabetes',
          name: 'diabetes',
          component: DiabetesView,
        },
        {
          path: 'login',
          name: 'login',
          component: LoginView,
        },
        {
          path: 'contact',
          name: 'contact',
          component: ContactView,
        },
        {
          path: 'register',
          name: 'register',
          component: RegisterView,
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
        },
      ],
    },

    {
      path: '/',
      component: PrivateLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'glucemias',
          name: 'glucemias',
          component: GlucemiasView,
        },
        {
          path: 'profile',
          name: 'profile',
          component: ProfileView,
        },
        {
          path: 'settings',
          name: 'settings',
          component: SettingsView,
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.matched.some((record) => record.meta.requiresAuth) && !token) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
