var mapChoiceSelect = document.getElementById('map-type');
var mapChoice = mapChoiceSelect.options[mapChoiceSelect.selectedIndex].value;

var map = L.map('map').setView([32.8785655,-117.2330362], 14);
var tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

document.getElementById('map-type').addEventListener('change', function() {
  var selectedMapType = this.value;
  switch (selectedMapType) {
    case 'osm':
      tileLayer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
      tileLayer.setAttribution('Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors');
      break;
    case 'mapbox-streets':
      tileLayer.setUrl('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken);
      tileLayer.setAttribution('Map data &copy; <a href="https://www.mapbox.com/">Mapbox</a> contributors');
      tileLayer.options.id = 'mapbox/streets-v11';
      break;
    case 'mapbox-satellite':
      tileLayer.setUrl('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken);
      tileLayer.setAttribution('Map data &copy; <a href="https://www.mapbox.com/">Mapbox</a> contributors');
      tileLayer.options.id = 'mapbox/satellite-v9';
      break;
    case 'esri-worldimagery':
      tileLayer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
      tileLayer.setAttribution('Map data &copy; <a href="https://www.esri.com/en-us/home">Esri</a>');
      break;
  }
});