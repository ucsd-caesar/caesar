const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

var mapChoiceSelect = document.getElementById('map-type');
var mapChoice = mapChoiceSelect.options[mapChoiceSelect.selectedIndex].value;

const basemaps = {
  OpenStreetMap: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',   {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),
  EsriWorldImagery: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {attribution: '&copy; <a href="https://www.esri.com/en-us/home">Esri</a>'}),
};

var map = L.map('map', {drawControl: true});
basemaps.OpenStreetMap.addTo(map); // initial map set to OSM
L.control.layers(basemaps).addTo(map); // add layer control to map (top right coner)

// set map to user's location if found, otherwise set to UCSD
map.locate()
  .on("locationfound", (e) => map.setView(e.latlng, 14))
  .on("locationerror", (e) => map.setView([32.8785655,-117.2330362], 14));

// asynchronously load markers from database
async function loadMarkers() {
  const markers_url = `/api/markers/?in_bbox=${map
    .getBounds()
    .toBBoxString()}`;
  const response = await fetch(markers_url);
  const geojson = await response.json();
  return geojson;
}

// asynchronously render markers on the map
async function renderMarkers() {
  const markers = await loadMarkers();
  L.geoJSON(markers)
    .bindPopup((layer) => layer.feature.properties.name)
    .addTo(map);
}

// render markers when the user stops moving on the map
map.on("moveend", () => renderMarkers());

// POST data to database
async function postData(url = "", data = {}) {
  $.ajax({
    url: url,
    data: data,
    contentType: 'application/json;',
    dataType: 'Feature',
    type: 'POST',
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (data) {
      console.log(data);
    },
    failure: function(errMsg) {
      alert(errMsg);
    }
  });
}

var numMarkers = 0;
// when a drawing is created, add to map and save to database
map.on(L.Draw.Event.CREATED, function (e) {
  var type = e.layerType,
      layer = e.layer;

  var data = layer.toGeoJSON();
  numMarkers++;
  data.id = 3;
  data.properties.name = "Test";

  var jsonStr = '{"type":"FeatureCollection","features":[]}';
  var obj = JSON.parse(jsonStr);
  obj.features.push(data);
  console.log(obj);
  geojson = loadMarkers();
  console.log(geojson);
  layer.addTo(map);
  postData("/api/markers/", obj);
});