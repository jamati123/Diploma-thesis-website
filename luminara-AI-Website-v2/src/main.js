// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { auth } from './firebaseConfig'; // Importiere die initialisierte Auth-Instanz
// main.js
import 'katex/dist/katex.min.css';


const app = createApp(App);

// Wenn du Firebase Auth global verfügbar machen möchtest, kannst du es als Plugin hinzufügen
app.config.globalProperties.$auth = auth;

app.use(router);
app.mount('#app');
