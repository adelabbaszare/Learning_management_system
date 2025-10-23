import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
import './assets/custom-bulma.scss'

const api = axios.create({
  baseURL: "https://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

createApp(App).use(store).use(router, axios).mount('#app')
