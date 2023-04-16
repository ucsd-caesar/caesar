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

    # open and read all four video files
    video_file1 = open("videos/Oaks.mp4", "rb")
    video_bytes1 = video_file1.read()
    video_file2 = open("videos/800IC.mp4", "rb")
    video_bytes2 = video_file2.read()
    video_file3 = open("videos/Rices.mp4", "rb")
    video_bytes3 = video_file3.read()
    video_file4 = open("videos/Sierra.mp4", "rb")
    video_bytes4 = video_file4.read()
    video_file5 = open("videos/fakeVideo.mp4", "rb")
    video_bytes5 = video_file5.read()
    left_column, right_column = st.columns(2)
    botLeft, botMid, botRight = st.columns(3)

    # You can use a column just like st.sidebar
    # Or even better, call Streamlit functions inside a "with" block:
#    with right_column:
#        chosen = st.radio(
#            'Available Feeds',
#            ("Feed 1", "Feed 2", "Feed 3", "Feed 4", "Feed 5"))
#        st.write(f"You are in {chosen}")

    # Add sidebar with checkbox to show/hide videos:

    with st.sidebar:
        st.write('### Controls')

        checkbox1 = st.checkbox('Show Video 1', key = 'a')
        checkbox2 = st.checkbox('Show Video 2', key = 'b')
        checkbox3 = st.checkbox('Show Video 3', key = 'c')
        checkbox4 = st.checkbox('Show Video 4', key = 'd')
        checkbox5 = st.checkbox('Show Video 5', key = 'e')

        st.write('### ')
        def select_callback():
            st.session_state.a = st.session_state.sel
            st.session_state.b = st.session_state.sel
            st.session_state.c = st.session_state.sel
            st.session_state.d = st.session_state.sel
            st.session_state.e = st.session_state.sel

        def deselect_callback():
            st.session_state.a = False
            st.session_state.b = False
            st.session_state.c = False
            st.session_state.d = False
            st.session_state.e = False
        st.button('Select All', key='sel', on_click = select_callback)
        st.button('Deselect All', on_click = deselect_callback)

        box_list = [checkbox1, checkbox2, checkbox3, checkbox4, checkbox5]
        if checkbox1:
            left_column.video(video_bytes1)
        if checkbox2:
            right_column.video(video_bytes2)
        if checkbox3:
            botLeft.video(video_bytes3)
        if checkbox4:
            botMid.video(video_bytes4)
        if checkbox5:
            botRight.video(video_bytes5)
       

