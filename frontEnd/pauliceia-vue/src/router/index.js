import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/IndexView'
import Contact from '@/views/ContactView'
import openLayers from '@/views/MapView'
import login from '@/views/loginView'
import register from '@/views/registerView'

Vue.use(Router)

const routes = [
    {path: '/', redirect: "/index"},  
    {path: '/index', component: Index},
    {path: '/contato', component: Contact},
    {path: '/mapa', component: openLayers},
    {path: '/login', component: login},
    {path: '/register', component: register},
  ]
  
  const router = new Router({
    mode: 'history',
    routes
  })

  export default router