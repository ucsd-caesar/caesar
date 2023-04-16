import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import os
import videos
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
# Surface data for terrain color
SURFACE_IMAGE = f"https://api.mapbox.com/v4/mapbox.satellite/{{z}}/{{x}}/{{y}}@2x.png?access_token={MAPBOX_API_KEY}"
# Icon image URL for pydeck markers
ICON_URL = "https://cdn1.iconfinder.com/data/icons/social-messaging-ui-color/254000/66-512.png"
# Icon data for pydeck markers
ICON_DATA = { "url": ICON_URL, "width": 242, "height": 242, "anchorY": 442,}
# Default location for map views
START_LOCATION = [46.24, -122.18]

# Create Folium map
m = folium.Map(location=START_LOCATION, zoom_start=10)
fg = folium.FeatureGroup(name="Video Sources")

# load video data
video_file1 = open("videos/Oaks.mp4", "rb")
stream1 = video_file1.read()
video_file2 = open("videos/800IC.mp4", "rb")
stream2 = video_file2.read()
video_file3 = open("videos/Rices.mp4", "rb")
stream3 = video_file3.read()
video_file4 = open("videos/Sierra.mp4", "rb")
stream4 = video_file4.read()
video_file5 = open("videos/fakeVideo.mp4", "rb")
stream5 = video_file5.read()

streams = [stream1, stream2, stream3, stream4, stream5]

def get_marker_locations():
    return pd.read_csv("map_data.csv")

def add_markers(data):
    """Add markers to folium map"""
    for location in data.itertuples():
        fg.add_child(
            folium.Marker(
                location=[location.lat, location.lon],
                icon=folium.Icon(color='blue'),
                tooltip=location.name)
        )

def add_icon_data(data):
    """Add icon column to dataframe for pydeck markers"""
    data["icon_data"] = None
    for i in data.index:
        data["icon_data"][i] = ICON_DATA

@st.cache_data
def get_video_stream(str):
    """get video stream from last clicked marker"""
    id = int(str[6])
    return streams[id-1]

@st.cache_data
def load_map():
    """Load map data and return a pydeck deck object"""
    
    map_data = get_marker_locations()
    add_icon_data(map_data)

    layers = [
        pdk.Layer(
            "TerrainLayer", 
            elevation_decoder=ELEVATION_DECODER, 
            texture=SURFACE_IMAGE, 
            elevation_data=TERRAIN_IMAGE
        ),
        pdk.Layer(
            type="IconLayer",
            data=map_data,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True,
        )
    ]

    view_state = pdk.ViewState(latitude=START_LOCATION[0], longitude=START_LOCATION[1],
                                zoom=11.5, bearing=0, pitch=60)
    r = pdk.Deck(layers, initial_view_state=view_state)
    return r

# read map data and add markers
add_markers(get_marker_locations())

top_row = st.empty() # Create empty container for map display and video player

# Display Folium map
with top_row.container():
    c1, c2 = st.columns(2)

    with c1:
        Draw(export=True).add_to(m)
        output = st_folium(
            m, 
            feature_group_to_add=fg,
            width = 800, 
            height=400
        )
    with c2:
        stream_name = output["last_object_clicked_tooltip"]
        if stream_name:
            st.video(get_video_stream(stream_name))
            
        

# Display Pydeck map
st.pydeck_chart(load_map())
