import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import Login from '@/components/Login.vue'
import Admin from '@/components/Admin.vue'
import Signup from '@/components/Signup.vue'
import Manage_Subject from '@/components/Manage_Subject.vue'
import Add_Chapter from '@/components/Add_Chapter.vue'
import Manage_Quiz from '@/components/Manage_Quiz.vue'
import View_Question from '@/components/View_Question.vue'
import User from '@/components/User.vue'
import Start_Quiz from '@/components/Start_Quiz.vue'
import User_Results from '@/components/User_Results.vue'
import Admin_User from '@/components/Admin_User.vue'
import Admin_Summary from '@/components/Admin_Summary.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HelloWorld,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/manage_subject',
      name: 'manage_subject',
      component: Manage_Subject,
    },
    {
      path: '/add_chapter/:subject_id',
      name: 'add_chapter',
      component: Add_Chapter,
    },
    {
      path: '/manage_quiz',
      name: 'manage_quiz',
      component: Manage_Quiz,
    },
    {
      path: '/view_questions/:quiz_id',
      name: 'view_question',
      component: View_Question,
    },
    {
      path: '/user',
      name: 'user',
      component: User,
    },
    {
      path: '/start_quiz/:quiz_id',
      name: 'start_quiz',
      component: Start_Quiz,
    },
    {
      path: '/user_results',
      name: 'user_results',
      component: User_Results,
    },
    {
      path: '/admin_user',
      name: 'admin_user',
      component: Admin_User,
    },
    {
      path: '/admin_summary',
      name: 'admin_summary',
      component: Admin_Summary,

    }

  ],
})

export default router
