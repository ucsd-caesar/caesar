import streamlit as st
import pydeck as pdk
import os
import folium
from folium.plugins import Draw

from streamlit_folium import st_folium

st.set_page_config(page_title="Map", layout="wide", initial_sidebar_state="expanded")

# Import Mapbox API Key from environment
MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
# AWS Open Data Terrain Tiles
TERRAIN_IMAGE = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}
SURFACE_IMAGE = f"https://api.mapbox.com/v4/mapbox.satellite/{{z}}/{{x}}/{{y}}@2x.png?access_token={MAPBOX_API_KEY}"

@st.cache_data
def load_map():
    terrain_layer = pdk.Layer(
        "TerrainLayer", 
        elevation_decoder=ELEVATION_DECODER, 
        texture=SURFACE_IMAGE, 
        elevation_data=TERRAIN_IMAGE
    )

    view_state = pdk.ViewState(latitude=46.24, longitude=-122.18, zoom=11.5, bearing=140, pitch=60)
    r = pdk.Deck(terrain_layer, initial_view_state=view_state)
    return r

# Folium map
m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw(export=True).add_to(m)
output = st_folium(m, width=700, height=500)

# Pydeck map
st.pydeck_chart(load_map())
