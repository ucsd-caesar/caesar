import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
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

START_LOCATION = [46.24, -122.18]

@st.cache_data
def load_map():
    terrain_layer = pdk.Layer(
        "TerrainLayer", 
        elevation_decoder=ELEVATION_DECODER, 
        texture=SURFACE_IMAGE, 
        elevation_data=TERRAIN_IMAGE
    )

    view_state = pdk.ViewState(latitude=START_LOCATION[0], longitude=START_LOCATION[1],
                                zoom=11.5, bearing=140, pitch=60)
    r = pdk.Deck(terrain_layer, initial_view_state=view_state)
    return r

# random dataframe displayed on map
map_data = pd.DataFrame(
np.random.randn(1000, 2) / [50, 50] + START_LOCATION,
columns=['lat', 'lon'])

# Folium map
m = folium.Map(location=START_LOCATION, zoom_start=10)
Draw(export=True).add_to(m)
output = st_folium(m, width=700, height=500)

# Pydeck map
st.pydeck_chart(load_map())
