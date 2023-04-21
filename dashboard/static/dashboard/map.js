
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [32.8785655,-117.2330362],
    zoom: 14
})
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const container = document.getElementById('deck-container');
const jsonInput = {
"initialViewState": {
"bearing": 140,
"latitude": 46.24,
"longitude": -122.18,
"pitch": 60,
"zoom": 11.5
},
"layers": [
{
  "@@type": "TerrainLayer",
  "elevationData": "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png",
  "elevationDecoder": {
    "bScaler": 0.00390625,
    "gScaler": 1,
    "offset": -32768,
    "rScaler": 256
  },
  "id": "d391d7ad-ee47-4331-89de-3ce9a0e598d5",
  "texture": "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token="
}
],
"mapProvider": "carto",
"mapStyle": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
"mapboxKey": "",
"views": [
{
  "@@type": "MapView",
  "controller": true
}
]
};
const tooltip = true;
const customLibraries = null;
const configuration = null;

const deckInstance = createDeck({
              container,
  jsonInput,
  tooltip,
  customLibraries,
  configuration
});