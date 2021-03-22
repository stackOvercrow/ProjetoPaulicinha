<template>
  <div>
    <article id="index">
      <hgroup id="postSignature">
          <h1>O Projeto Paulicinha</h1>
          <h2>Editado pela última vez em 08/09/2020</h2>
      </hgroup>

      <p>Olá,</p>

      <p>Meu nome é Gabriel dos Reis e sou estudante de Análise e Desenvolvimento de Sistemas pelo Instituto Federal de Educação, Ciência e Tecnologia da Bahia. Ao ser aceito no Projeto Pauliceia, fui orientado a estudar determinados assuntos e usá-los para a construção de um site. Este site, que batizei de Paulicinha em referência ao projeto original, é um sistema de mapas inteligentes onde o usuário pode fazer consultas à dados geográficos. O projeto é um protótipo web GIS construído para ser apresentado à equipe do Pauliceia. O site foi construído utilizando HTML, CSS, JavaScript, Vue.js e Open Layers. O banco de dados utilizado no site é o PostgreSQL, com a extensão espacial PostGIS. O Serviço Web utiliza Python com o framework Flask. Este protótipo foi construído em 8 meses, enquanto eu aprendia as ferramentas citadas anteriormente.</p>

      <figure id="indexImage">
        <img v-if="region == 'Região Norte'" id="mainImage" src="../assets/norte.jpg" :alt="region">
        <img v-else-if="region == 'Região Nordeste'" id="mainImage" src="../assets/nordeste.jpg" :alt="region">
        <img v-else-if="region == 'Região Centro'" id="mainImage" src="../assets/centro.jpg" :alt="region">
        <img v-else-if="region == 'Região Sudeste'" id="mainImage" src="../assets/sudeste.jpg" :alt="region">
        <img v-else-if="region == 'Região Sul'" id="mainImage" src="../assets/sul.jpg" :alt="region">
        <img v-else id="mainImage" src="../assets/brasil.jpg" :alt="region">

        <figcaption id="imageSubtitle">
          <p v-if="region == ''">Mapa do Brasil.</p>
          <p v-else>Mapa da região {{this.region}}.</p>
        </figcaption>
      </figure>
    </article>
  </div>
</template>

<script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script> 
<script>
export default {
  name: 'index',
  props: {
    msg: String
  },

  data: function(){
    return{
      region: "",
      image: 'brasil.jpg'
    }
  },

  methods:{
    getLocation: function(){
      var vm = this

      if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(
          function sucess(position){
            var xhttp = new XMLHttpRequest()

            xhttp.open("GET", "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + 
              position.coords.latitude + "&lon=" + position.coords.longitude);
            xhttp.send();
            xhttp.onreadystatechange = processRequest; 
            xhttp.addEventListener("readystatechange", processRequest, false); 

            function processRequest(e) { 
                if (xhttp.readyState == 4 && xhttp.status == 200) { 
                    var response = JSON.parse(xhttp.responseText); 
                    vm.region = response.address.region
                    return; 
                } 
            } 
          }, 
          
          function error(error_message){
            console.log("Houve alguma falha ao recuperar sua localização")
          }
        )
      }else{
        alert("Geolocalização não suportada ou não permitida.")
      }
    },
  },

  beforeMount(){
    this.getLocation()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  body{
    background-color: #ffffff;
  }

  p{
    text-indent: 15px;
    text-align: justify;
    font-family: sans-serif;
    padding-right: 10px;
    padding-left: 10px;
  }

  h1{
    margin-top: 5px;
    padding-top: 5px;
    color: #ffffff;
    font-size: 18pt;
    font-family: sans-serif;
    text-shadow: 1px 1px black;
    margin-bottom: 0px;
    text-indent: 10px;
  }

  h2{
    color: #ffffff;
    font-size: 14pt;
    font-family: sans-serif;
    text-shadow: 0px 1px black;
    margin-top: 0px;
    text-indent: 15px;
    margin-bottom: 0px;
  }

  article#index{
    display: flex;
    flex-direction: column;
    margin: auto;
    background-color: #EEAA7B;
    box-shadow: 0 0 10px grey;
    border-radius: 5px;
    width: 99%;
  }

  hgroup#postSignature{
    border-bottom: solid;
    border-width: 3px;
    border-color: #ffffff;
    background-color: #f47c48;
    padding-bottom: 3px;
  }

  figure#indexImage{
    display: block;
    position: relative;
    margin-bottom: 5px;
    border: solid;
    border-color: #f25c26;
    margin-left: auto;
    margin-right: auto;
    width: 520px;
    height: 300px;
    transition: 1s;
  }

  figure#indexImage img#mainImage{
    width: 520px;
    height: 300px;
    margin-left: auto;
  }

  figure#indexImage:hover{
    border-style: dashed;
    border-color: black;
    transition: 1s;
  }

  figure#indexImage figcaption#imageSubtitle{
    width: 520px;
    color: #000000;
    font-weight: bold;
    height: 300px;
    opacity: 0;
    position: absolute;
    box-sizing: border-box;
    top: 0px;
    padding: 10px;
    transition: 1s;
  }

  figure#indexImage figcaption#imageSubtitle p{
    text-align: center;
    margin-top: 20%;
  }

  figure#indexImage:hover figcaption#imageSubtitle{
    opacity: 1;
    transition: 1s;
    background-color: rgba(105, 105, 105, .5);
  }
</style>
