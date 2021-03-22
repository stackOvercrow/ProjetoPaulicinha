<template>
  <div>
    <form id="app" @submit="checkForm" action="http://localhost:5000/log_in" method="post">
        <h1>
            Página de Login
        </h1>
        <p>
            <label for="username">Nome de Usuário</label>
            <input id="username" v-model="username" type="text" name="username">
        </p>
        <p>
            <label for="password">Senha</label>
            <input id="password" v-model="password" type="password" name="password">
        </p>

        <p v-if="errors.length">
            <b>Por favor, corrija os seguintes erros:</b>

            <ul>
                <li v-for="error in errors" :key=error> {{ error }} </li>
            </ul>
        </p>
        
        <p>
            <input type="submit" value="Login">
        </p>
    </form>
  </div>
</template>

<script>

export default {
    name: 'login',

    data: () => ({
        errors: [],
        username: null,
        password: null,
        loginUrl: 'http://localhost:5000/log_in',       
    }),

    methods:{
        checkForm: function (e) {
            this.errors = [];
            
            if(this.name && this.age){
                return true;
            }

            if(!this.username){
                this.errors.push('O nome de usuário é obrigatório.');
            }else{
                if(this.username.length > 12){
                    this.errors.push('O nome de usuário deve ter até 12 caracteres.')
                }
            }

            if(!this.password){
                this.errors.push('A senha é obrigatória.');
            }else{
                if(this.password.length < 8 || this.password.length > 12){
                    this.errors.push('A senha deve ter entre 8 e 12 caracteres.')
                }
            }

            if(this.errors.length){
                e.preventDefault();
            } 
        }
    }
}
</script>

<style scoped>
#app{
    background-color: #eeaa7b;
    display: block;
    width: 99%;
    margin: auto;
    box-shadow: 1px 1px 3px grey;
    font-family: sans-serif;
    font-size: 12pt;
}

#app label{
    display: block;
    padding-bottom: 5px;
    padding-top: 5px;
}
</style>
