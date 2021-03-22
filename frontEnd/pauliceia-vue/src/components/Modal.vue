<template>
  <div class="modal" v-show="value">
    <div class="container">
      <div class="modal_title">Lista de Mapas</div>
      
      <li v-for="item in geojson" :key="item.properties.Nome">
        Nome: {{ item.properties.Nome }}
        /
        Descrição: {{ item.properties.Descrição }}
        /
        <button v-on:click="changeMap(item)">Ativar</button>
      </li>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Modal',
    props: {
        value: {
            required: true
        },
        geojson: {
          required: true
        }
    },
      methods: {
        changeMap(item){
          this.$emit("changeMap", item)
        },
    }
};
</script>

<style scoped>
  .modal {
    background-color: white;
    border-style: solid;
  }

  .modal_title{
    border-bottom: solid;
  }

  .container{
    overflow: scroll;
    max-height: 400px;
  }

  li{
    list-style: none;
    border-bottom: dashed;
    border-color: grey;
    margin-bottom: 5px;
  }
</style>