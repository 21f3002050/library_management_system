import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import UserSignup from "../components/UserSignup.vue";
import UserLogin from "../components/UserLogin.vue";
import UserDashboard from "../components/UserDashboard.vue";
import LibrarianDashboard from "../components/LibrarianDashboard.vue";
import EbookManagement from '@/components/EbookManagement.vue';
import SearchComponent from '../components/SearchComponent.vue';
import ManageRequests from '../components/ManageRequests.vue';
import ManageStatistics from '../components/ManageStatistics.vue';

import SectionPage from "../components/SectionPage.vue";




const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/signup",
    name: "UserSignup",
    component: UserSignup,
  },
  {
    path: "/login",
    name: "UserLogin",
    component: UserLogin,
  },
  {
    path: "/user-dashboard",
    name: "UserDashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/librarian-dashboard",
    name: "LibrarianDashboard",
    component: LibrarianDashboard,
    meta: { requiresAuth: true, role: "librarian" },
  },
  {
    path: "/sections/:sectionId",
    name: "SectionPage",
    component: SectionPage,
    meta: { requiresAuth: true, role: "librarian" },
  },
  {
    path: '/sections/:sectionId/ebooks',
    name: 'EbookManagement',
    component: EbookManagement,
    meta: { requiresAuth: true, role: 'librarian' }
  },
    {
      path: '/search',
      name: 'SearchComponent',
      component: SearchComponent
    },
    {
      path: '/manage-requests',
      name: 'ManageRequests',
      component: ManageRequests,
      meta: { requiresAuth: true, requiresRole: 'librarian' }
    },
    {
      path: '/manage-statistics',
      name: 'ManageStatistics',
      component: ManageStatistics,
      meta: { requiresAuth: true, requiresRole: 'librarian' }
    },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for required authentication and roles
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({ name: 'UserLogin' });
    } else if (to.meta.role && to.meta.role !== role) {
      next({ name: 'Home' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
