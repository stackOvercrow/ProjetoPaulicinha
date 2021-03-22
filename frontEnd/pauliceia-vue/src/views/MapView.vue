<template>
  <div id="app">
    <div class="cell map">
      <Modal v-model="modalOpen" @changeMap="changeMap" @deleteMap="deleteMap" :geojson="geojson"/> 
      <OpenLayer  id="map" :geojson="map" @getCoords="getCoords" @select="selected = $event"/>
      <div v-if="modalOpen">
        <button v-on:click="displayModal('inherit')" type="button">Ver Mapa</button> 
      </div>
      <div v-else>
        <button v-on:click="saveMap" type="button">Salvar</button>
        <button v-on:click="displayModal('none')" type="button">Escolher Mapa</button>
        <button v-on:click="deleteMap">Excluir</button>
      </div>
    </div>

    <div class="cell edit side">
      <EditLayer :author="userLogged" :coords="coordsToGeojson" :geojson="map" @change="map = $event"/>
    </div>
    <div class="cell inspect side">
      <InspectLayer v-if="selected" :feature="selected" />
      <p id="side-text" v-else>
        Para criar o seu mapa, preencha o modelo default de geojson. Atente-se que:
        <br>
        1- Seu nome será colocado no campo 'Autor' automaticamente ao tentar salvar o mapa. 
        <br>
        2- Ao clicar, a coordenada atual será copiada para o geojson (atualmente, só há suporte para polígonos com quatro lados) em sentido horário.
      </p>
    </div>
  </div>
</template>

<script>
  import OpenLayer from '../components/OpenLayer.vue'
  import EditLayer from '../components/EditLayer.vue'
  import InspectLayer from '../components/InspectLayer.vue'
  import Modal from '../components/Modal.vue'
  import axios from 'axios'
  
  export default {
    name: 'App',
    props: {
      userLogged: String,
    },
    components: {
      OpenLayer,
      EditLayer,
      InspectLayer,
      Modal
    },

    data: () => ({
      selected: undefined,
      geojson: {},
      map: null,
      modalOpen: false,
      coordsToGeojson: null,
      side: 0,
    }),

    methods: {
      getGeojson(){
        const path = 'http://localhost:5000/geojson';

        axios.get(path)
          .then((res) => {
            this.geojson = res.data.geojson
            this.map = this.geojson[0]
          })
          .catch((error) => {
            print(error)
          })
      },
      saveMap(){
        axios.defaults.withCredentials = true;

        axios.post('http://localhost:5000/save_map', {
          jsonStr: JSON.stringify(this.map),
          withCredentials: true
        })
        .then((res) => {
          if(res.data.status == 'sucess'){
            window.alert("Mapa Salvo com Sucesso")
            location.reload();
          }
        })
        .catch (err => {
          console.log(err)
          window.alert("Não foi possível salvar o mapa. Por favor, verifique se a formatação está correta ou se já não existe um mapa com o mesmo nome.")
        })
      },
      changeMap(item){
        this.map = item
      },
      deleteMap(){
        axios.defaults.withCredentials = true;
        
        axios.post('http://localhost:5000/delete_map', {
          jsonData: JSON.stringify(this.map),
          withCredentials: true
        })
        .then((res) => {
          if(res.data.status == 'sucess'){
            window.alert("Mapa Deletado com Sucesso")
            location.reload();
          }
        })
        .catch (err => {
          console.log(err)
          window.alert("Não foi possível deletar o mapa. Verifique se sua conta tem privilégios de administrador.")
        })
      },
      displayModal(gridDisplay) {
        this.modalOpen = !this.modalOpen;

        document.querySelector('#map').style.display = gridDisplay;
        document.querySelector('.inspect').style.display = gridDisplay;
      },
      getCoords(value){
        this.coordsToGeojson = value
      }
    },

    created(){
      this.getGeojson()
    }
  }
</script>

<style scoped>
html, body {
    height: 100%;
  }

  #app {
    width: 99%;
    margin-top: 0px;
    margin: auto;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100%;
    display: grid;
    grid-auto-columns: 120vh;
    grid-auto-rows: 1fr;
    grid-gap: 1rem;
    padding: 0.5rem;
    box-sizing: border-box;
    background-color: #eeaa7b;
  }

  .cell {
    border-radius: 4px;
  }

  .side {
    font-family: sans-serif;
    color: black;
    width: 50%;
    background-color: lightgrey;
    min-height: 200px;
  }

    #side-text{
      padding: 3rem;
    }

  .map {
    grid-column: 1;
    grid-row-start: 1;
    grid-row-end: 3;
    flex-grow: 3;
  }

  .edit {
    grid-column: 2;
    grid-row: 1;
    flex-grow: 1;
  }

  .inspect {
    grid-column: 2;
    grid-row: 2;
    flex-grow: 1;
  }
</style>