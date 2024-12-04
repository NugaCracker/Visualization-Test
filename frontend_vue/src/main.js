import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';

axios.defaults.baseURL = 'http://127.0.0.1:8081';  // Flask 서버 기본 URL 설정
createApp(App).mount('#app')
