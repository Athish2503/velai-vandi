import { createRouter, createWebHistory } from 'vue-router'
import WorkerRegister from '../views/WorkerRegister.vue'
import WorkerDashboard from '../views/WorkerDashboard.vue'
import EmployerPost from '../views/EmployerPost.vue'
import EmployerDashboard from '../views/EmployerDashboard.vue'

const routes = [
  { path: '/', redirect: '/worker/register' },
  { path: '/worker/register', component: WorkerRegister },
  { path: '/worker/dashboard/:id', component: WorkerDashboard, props: true },
  { path: '/employer/post', component: EmployerPost },
  { path: '/employer/dashboard/:id', component: EmployerDashboard, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router