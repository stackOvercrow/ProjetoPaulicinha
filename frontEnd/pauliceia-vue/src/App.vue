<template>
  <div>
    <navBar @userLogged= "getUser"/>
    <router-view :userLogged="this.userLogged"/>
    <footerBar />
  </div>
</template>

<script>
import navBar from './components/NavBar'
import footerBar from './components/FooterComponent'

export default {
  name: 'App',
  components: {
    navBar,
    footerBar,
  },

  data: function(){
      return{
          userLogged: null
      }
  },
  
  methods:{
    getUser(value){
      this.userLogged = value
    }
  }
}
</script>