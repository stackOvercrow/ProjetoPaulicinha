<template>
  <div>
    <div id="map" ref="map" />
  </div>
</template>

<script>
  import 'ol/ol.css';
  import {Map, View} from 'ol';
  import TileLayer from 'ol/layer/Tile';
  import OSM from 'ol/source/OSM';
  import {fromLonLat, transform} from 'ol/proj';
  import MousePosition from 'ol/control/MousePosition';
  import VectorLayer from 'ol/layer/Vector';
  import VectorSource from 'ol/source/Vector';
  import GeoJSON from 'ol/format/GeoJSON';
  import {createStringXY, toStringXY} from 'ol/coordinate';
  import {defaults as defaultControls} from 'ol/control';

  export default {
    name: 'OpenLayer',
    components: {},
    props: {geojson: [Object, String]},

    data: () => ({
      olMap: null,
      vectorLayer: null,
      selectedFeature: null,
      mousePositionControl: null,
      precision: 4,
      coords: null
    }),

    mounted() {
      this.mousePositionControl = new MousePosition({
        coordinateFormat: createStringXY(this.precision),
        projection: 'EPSG:4326',
      })

      this.vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: [],
        }),
      })

      this.olMap = new Map({
        controls: defaultControls().extend([this.mousePositionControl]),
        target: this.$refs['map'],
        layers: [
          new TileLayer({
            source: new OSM()
          }),
          this.vectorLayer
        ],

        view: new View({
          zoom: 12,
          center: fromLonLat([-38.4105, -12.9232]),
          constrainResolution: true
        }),
      })

      this.olMap.on('pointermove', (event) => {
        const hovered = this.olMap.forEachFeatureAtPixel(event.pixel, (feature) => feature)
        if (hovered !== this.selectedFeature) {
          this.$set(this, 'selectedFeature', hovered);
        }
      })

      this.olMap.on('singleclick', (event) => {
        this.coords = '[' + toStringXY(transform(event.coordinate, 'EPSG:3857', 'EPSG:4326'), this.precision) + ']';

        this.toGeojson(this.coords);
      })

      this.updateSource(this.geojson)
    },

    watch: {
      geojson(value){
        this.updateSource(value)
      },
      selectedFeature(value) {
        this.$emit('select', value)
      }
    },

    methods: {
      updateSource(geojson){
        try{
          const view = this.olMap.getView()
          const source = this.vectorLayer.getSource()
          const features = new GeoJSON({
            featureProjection: 'EPSG:3857'
          }).readFeatures(geojson)

          source.clear();
          source.addFeatures(features);
          view.fit(source.getExtent())
        }catch (error){
          //ignore errors in console when typing the geoJSON.
        }
      },
      toGeojson(coords) {
        this.$emit('getCoords', coords)
      }
    }
  }
</script>

<style scoped>
  body{
    background-color: #ffffff;
    color: black;
  }

  div #mouse-position{
    background-color: #b1def0;
  }

  div #map{
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

  iframe#map{
    margin-top: 15px;
  }
</style>