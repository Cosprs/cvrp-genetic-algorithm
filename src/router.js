import Vue from 'vue'
import Router from 'vue-router'
import VueDemo from '@/components/VueDemo'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: VueDemo
    }
  ]
})
