import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import ImageTool from './views/ImageTool.vue'
import DocTool from './views/DocTool.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ImageTool },
    { path: '/doc', component: DocTool },
  ]
})

createApp(App).use(router).mount('#app')
