<template>
  <div class="header">
    <img id="logo" v-bind:src="require('../assets/' + logo)">
    <img id="pageIcon" v-bind:src="require('../assets/' + icon)">
    <nav id="menuTopo" v-on:mouseout="pageLogo()">   
        <ul>
            <li class="nav-item" v-on:mouseover="changeLogo('index.png')"><router-link to="/">Home</router-link></li>
            <li class="nav-item" v-on:mouseover="changeLogo('mapa.png')"><router-link to="/mapa">Mapa</router-link></li>
            <li class="nav-item" v-on:mouseover="changeLogo('contato.png')"><router-link to="/contato">Contato</router-link></li>
            <div id="NotLogged" v-if="userLogged == 'Not Logged'">
                <li class="nav-item" v-on:mouseover="changeLogo('login.png')"><router-link to="/login">Login</router-link></li>
                <li class="nav-item" v-on:mouseover="changeLogo('register.png')"><router-link to="/register">Registre-se</router-link></li>
            </div>
            <li v-else class="nav-item" v-on:click="logout" v-on:mouseover="changeLogo('login.png')"><router-link to="/">Logout</router-link></li>
        </ul>
    </nav>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'navBar',

    data: function(){
        return{
            icon: 'index.png',
            logo: 'smallLogo.png',
            currentPath: '',
            userLogged: '',
            logoutSuceed: ''
        }
    },

    mounted(){
        axios
            .get('http://localhost:5000/user_logged', {withCredentials: true})
            .then(response => {
                this.userLogged = response.data.status
                this.$emit('userLogged', this.userLogged)
            });
    },

    methods: {
        changeLogo: function(image){
            this.icon = image
        },

        pageLogo: function(){
            this.currentPath = this.$router.history.current.path.substring(1, this.$router.history.current.path.length)
            this.icon = this.currentPath + '.png'
        },

        logout: function(){
            fetch('http://localhost:5000/logout', {
                method: 'POST',
                credentials: 'include'
            })
            .then(response => {
                this.logoutSuceed = response.data;
                location.reload();
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    div#NotLogged{
        display: ruby;
    }

    div.header{
        background-color: #f47c48;
        display: block;
        border: solid;
        border-color: #f25c26;
        box-shadow: 2px 2px grey;
        width: 99%;
        margin: auto;
        margin-bottom: 10px;
    }

    div.header img#pageIcon{
        float: right;
    }

    img#logo{
        width: 170px;
        height: 130px;
    }

    nav#menuTopo{
        display: inline-block;
    }

    nav#menuTopo ul{
        list-style: none;
        margin-left: 300px;
    }

    nav#menuTopo li{
        margin-right: 130px;
        display: inline-block;
        color: #DCD0C0;
        font-family: sans-serif;
        font-size: 11pt;
        text-shadow: 1px 1px black;
        text-transform: uppercase;
    }

    nav#menuTopo li:hover{
        background-color: #f25c26;
        transition: 0.5s;
    }

    nav#menuTopo li a{
        color: #DCD0C0;
        text-decoration: none;
    }
</style>
