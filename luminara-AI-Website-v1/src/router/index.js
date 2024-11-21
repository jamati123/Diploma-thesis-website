// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Importieren Sie Ihre Hauptansichten
import HomeView from '../views/HomeView.vue';
import DashboardView from '../views/DashboardView.vue';
import AccountView from '../views/AccountView.vue';
import ApplicationsView from '../views/ApplicationsView.vue';

// Importieren Sie die Sidebar-Komponenten als Unterrouten
import LuminaraOllama from '../components/LuminaraOllama.vue';
import OllamaChat from '../components/OllamaChat.vue';
import LuminaraImage from '../components/LuminaraImage.vue';
import LuminaraGallery from '../components/LuminaraGallery.vue';
import ChatGPT from '../components/ChatGPTComponent.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/account',
    name: 'Account',
    component: AccountView,
  },
  {
    path: '/applications',
    name: 'Applications',
    component: ApplicationsView,
    children: [
      {
        path: 'ollama',
        name: 'LuminaraOllama',
        component: LuminaraOllama,
      },
      {
        path: 'chat',
        name: 'OllamaChat',
        component: OllamaChat,
      },
      {
        path: 'image',
        name: 'LuminaraImage',
        component: LuminaraImage,
      },
      {
        path: 'gallery',
        name: 'LuminaraGallery',
        component: LuminaraGallery,
      },
        {
        path: 'chatgpt',
        name: 'ChatGPT',
        component: ChatGPT,
        },
        
      // Weitere Unterrouten können hier hinzugefügt werden
    ],
  },
  // Weitere Routen können hier hinzugefügt werden
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
