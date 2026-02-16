import streamlit as st
from engines.model import SearchEngine
from engines.video_conversion import  Conversion
from engines.hearing_model import SearchAudio
import filetype 
import os
import time 


def load_video() -> st.UploadedFile | None:
    
    st.header("Load video")
    file = st.file_uploader("Choose mp4 file", type=['mp4'])
    return file

def check_mp4(file):
    bytes_data = file.read(2048)
    check = filetype.guess(bytes_data)
    
    while check.mime is not "audio/mp4":
        st.write("Wrong extension")
        time.sleep(3)
        load_video()

def main():

    if st.session_state['video'] is None:

        file = load_video()
        check_mp4(file)

        st.session_state['video'] = file
        st.session_state['path'] = os.path.abspath(file)
        st.rerun()

    else:
        mode_selection(path=st.session_state['path'])

def init():
    


def mode_selection(path):

    search_frame = SearchEngine()
    search_audio = SearchAudio(file_dir = path)

    mode = st.selectbox("Select which mode would you like to use"
        ("1. Search by image", "2. Search by audio", "3. Search using both", "4. Load another video"))

    mode_number = mode[0]

    # Pobieramy dane z pamięci
                
    user_input = st.text_input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )

    if user_input.lower() == "q":
        st.rerun()

    if mode_number == "1":
        found = search_frame.find_photo(1, user_input)
        print(found)

    elif mode_number == "2":
        found = search_audio.find(1, user_input)
        print(found)

    elif mode_number == "3":
        found_frames = search_frame.find_photo(1, user_input)
        print("Wyniki wyszukiwania po obrazach: \n", found_frames)

        found_audio = search_audio.find(1, user_input)
        print("Wyniki wyszukiwania po dźwięku: \n", found_audio)

    



if __name__=="__main__":
    st.title("Video Search")