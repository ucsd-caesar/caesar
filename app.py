import streamlit as st

st.title("Hello World")

# open and read all four video files
video_file1 = open('videos/Oaks.mp4', 'rb')
video_bytes1 = video_file1.read()
video_file2 = open('videos/800IC.mp4', 'rb')
video_bytes2 = video_file2.read()
video_file3 = open('videos/Rices.mp4', 'rb')
video_bytes3 = video_file3.read()
video_file4 = open('videos/Sierra.mp4', 'rb')
video_bytes4 = video_file4.read()

# play the videos
st.video(video_bytes1)
st.video(video_bytes2)
st.video(video_bytes3)
st.video(video_bytes4)