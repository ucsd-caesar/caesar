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

# random dataframe displayed on map
map_data = pd.DataFrame(
    np.random.randn(5, 2) / [50, 50] + START_LOCATION,
    columns=['lat', 'lon'])

# Folium map
m = folium.Map(location=START_LOCATION, zoom_start=10)
Draw(export=True).add_to(m)

# add markers to Folium map
@st.cache_data
def add_markers(map_data):
    for i in range(0, len(map_data)):
        folium.Marker(location=[map_data.iloc[i]['lat'], map_data.iloc[i]['lon']],).add_to(m)

folium.Marker(location=START_LOCATION,).add_to(m)

# Display Folium map
output = st_folium(m, width=700, height=500)

# load Pydeck map and add markers
@st.cache_data
def load_map():
    layers = [
        pdk.Layer(
            "TerrainLayer", 
            elevation_decoder=ELEVATION_DECODER, 
            texture=SURFACE_IMAGE, 
            elevation_data=TERRAIN_IMAGE
        ),
        pdk.Layer(
            'HexagonLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        )
    ]

    view_state = pdk.ViewState(latitude=START_LOCATION[0], longitude=START_LOCATION[1],
                                zoom=11.5, bearing=140, pitch=60)
    r = pdk.Deck(layers, initial_view_state=view_state)
    return r

# Display Pydeck map
st.pydeck_chart(load_map())
