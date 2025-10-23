import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import About from '../views/About.vue'
import SignUp from '@/views/SignUp.vue'
import LogIn from '@/views/LogIn.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
