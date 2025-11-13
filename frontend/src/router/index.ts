import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Analyze from '@/views/Analyze.vue';
import About from '@/views/About.vue';
import Simulate from '@/views/Simulate.vue';

// Create router
const routes = [
  { path: '/', name: 'home', component: Home, children: [], },
  { path: '/analyze', name: 'analyze', component: Analyze, children: [], },
  { path: '/simulate', name: 'simulate', component: Simulate, children: [], },
  { path: '/about', name: 'about', component: About, children: [], },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;