<template>
  <div>
    <article id="index">
      <img class="image" src="../assets/pauliceia.jpeg">
      <p><a href="http://www.pauliceia.dpi.inpe.br/portal/home">Site oficial do Projeto Pauliceia.</a></p>
      <img class="image" src="../assets/stackovercrow.jpeg">
      <p><a href="https://github.com/stackOvercrow">Clique aqui para acessar meu Github.</a></p>
    </article>
  </div>
</template>

<script>
export default {
  name: 'contact'
}
</script>

<style scoped>
body{
  background-color: #ffffff;
  color: black;
}

a{
  text-decoration: none;
  margin: 2px;
  color: black;
}

a:hover{
  color: white;
}

p{
  text-align: center;
  margin: 5px;
}

article#index{
  display: flex;
  flex-direction: column;
  margin: auto;
  background-color: #EEAA7B;
  box-shadow: 0 0 10px grey;
  border-radius: 5px;
  width: 99%;
  height: 560px;
  margin-bottom: 5px;
}

.image{
  border-style: ridge;
  border-color: white;
  padding: 5px;
  width: 9%;
  margin: auto;
}
</style>
