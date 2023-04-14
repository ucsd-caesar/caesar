import os

import streamlit as st

from django.contrib.auth import authenticate

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

    # MAIN PAGE
    # ----------------------------------------

    st.title("Hello World")

    # open and read all four video files
    video_file1 = open("videos/Oaks.mp4", "rb")
    video_bytes1 = video_file1.read()
    video_file2 = open("videos/800IC.mp4", "rb")
    video_bytes2 = video_file2.read()
    video_file3 = open("videos/Rices.mp4", "rb")
    video_bytes3 = video_file3.read()
    video_file4 = open("videos/Sierra.mp4", "rb")
    video_bytes4 = video_file4.read()

    # play the videos
    st.video(video_bytes1)
    st.video(video_bytes2)
    st.video(video_bytes3)
    st.video(video_bytes4)
