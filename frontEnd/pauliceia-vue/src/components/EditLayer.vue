<template>
  <textarea v-model="geojsonEdit"></textarea>
</template>

<script>
  export default {
    name: 'EditLayer',
    props: {
      geojson: [Object, String],
      coords: String,
      author: String
    },

    data: () => ({
      side: 0
    }),

    computed: {
      geojsonEdit: {
        set(value) {
          this.$emit('change', JSON.parse(value))
        },
        get() {
          return JSON.stringify(this.geojson, null, ' ')
        }
      },
    },

    watch: {
      coords: function(){
        let json

        json = JSON.parse(this.geojsonEdit)
        json['geometry']['coordinates'][0][this.side][0] = JSON.parse(this.coords)[0]
        json['geometry']['coordinates'][0][this.side][1] = JSON.parse(this.coords)[1]

        if(this.side == 0){
          json['geometry']['coordinates'][0][4][0] = JSON.parse(this.coords)[0]
          json['geometry']['coordinates'][0][4][1] = JSON.parse(this.coords)[1]
        }

        this.side++;

        if(this.side > 3){
          this.side = 0
        }
        json['properties']['Autor'] = this.author;
        this.geojsonEdit = JSON.stringify(json)
      }
    }
  }
</script>

<style>
  textarea {
    width: 100%;
    height: 100%;
    resize: none;
  }
</style>