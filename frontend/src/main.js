import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import '@/assets/styles/index.css' 

const app = createApp(App)
app.use(router)
app.mount('#app')