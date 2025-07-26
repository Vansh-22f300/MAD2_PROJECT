import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from '@/components/HelloWorld.vue'
import Login from '@/components/Login.vue'
import Admin from '@/components/Admin.vue'
import Signup from '@/components/Signup.vue'
import Manage_Subject from '@/components/Manage_Subject.vue'
import Add_Chapter from '@/components/Add_Chapter.vue'
import Manage_Quiz from '@/components/Manage_Quiz.vue'
import Add_Question from '@/components/Add_Question.vue'
import View_Question from '@/components/View_Question.vue'

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
      path: '/add_question/:quiz_id',
      name: 'add_question',
      component: Add_Question,
    },
    {
      path: '/view_questions/:quiz_id',
      name: 'view_question',
      component: View_Question,
    }

  ],
})

export default router
