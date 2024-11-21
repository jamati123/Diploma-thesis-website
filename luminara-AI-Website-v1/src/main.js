// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importieren Sie den Router

createApp(App)
  .use(router) // Router verwenden
  .mount('#app');

