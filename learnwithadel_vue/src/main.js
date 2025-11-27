import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'
import './assets/custom-bulma.scss';
import 'highlight.js/styles/github.css';

/*import 'highlight.js/styles/monokai.css';*/

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1/",
  headers: {
    "Content-Type": "application/json",
  },
});

createApp(App).use(store).use(router, axios).mount('#app')
