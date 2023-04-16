import os
import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
from django.contrib.auth import authenticate

st.set_page_config(page_title="Videos", layout="wide", initial_sidebar_state="expanded")

# django wsgi.py
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

# Login Functions using Django WSGI backend for authentication
def check_password():
    """Returns True if the password is correct, False otherwise."""

    def password_entered():
        """Checks that the password entered is correct."""
        user = authenticate(username=st.session_state.username, password=st.session_state.password)
        if user is not None:
            st.session_state.password_correct = True
            del st.session_state.password
            del st.session_state.username
        else:
            st.session_state.password_correct = False

    # Password has not been entered yet
    if "password_correct" not in st.session_state:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", on_change=password_entered, key="password", type="password")
        return False
    # Password was entered, but was incorrect
    elif not st.session_state.password_correct:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input("Password", on_change=password_entered, key="password", type="password")
        st.error("Incorrect password")
        return False
    # Password was entered and was correct
    else:
        return True

if check_password():

    # Open and read all five video files
    video_file1 = open("videos/Oaks.mp4", "rb")
    video_bytes1 = video_file1.read()
    video_file2 = open("videos/800IC.mp4", "rb")
    video_bytes2 = video_file2.read()
    video_file3 = open("videos/Rices.mp4", "rb")
    video_bytes3 = video_file3.read()
    video_file4 = open("videos/Sierra.mp4", "rb")
    video_bytes4 = video_file4.read()
    video_file5 = open("videos/FakeVideo.mp4", "rb")
    video_bytes5 = video_file5.read()

    # Save videos to a list
    videos = [video_bytes1, video_bytes2, video_bytes3, video_bytes4, video_bytes5]

    # Set the display
    upperLeftColumn, upperRightColumn = st.columns(2)
    bottomLeft, bottomMid, bottomRight = st.columns(3)
    columns = [upperLeftColumn, upperRightColumn, bottomLeft, bottomMid, bottomRight]

    if 'count' not in st.session_state:
        st.session_state.count = 0

    def increment():
        st.session_state.count += 1

    # Add sidebar with a button to add videos:
    with st.sidebar:
        if st.button('Add a Video'):
            for i in range(st.session_state.count + 1):
                columns[i % 5].video(videos[i % 5])
            increment()