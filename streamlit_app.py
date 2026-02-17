import streamlit as st
from engines.model import SearchEngine
from engines.video_conversion import Conversion
from engines.hearing_model import SearchAudio
import filetype 
import os
import time 
from database import Database


def load_video():
    
    st.header("Load video")
    file = st.file_uploader("Choose mp4 file", type=['mp4'])
    return file

def check_mp4(file) -> bool:

    bytes_data = file.read(2048)
    check = filetype.guess(bytes_data)
    file.seek(0)
    if check is None:
        return False
    
    if check.mime == 'video/mp4': 
        return True

    return False


def save_video(file):
    ...

def main():

    if 'init' not in st.session_state:
        st.session_state['init'] = False

    if 'video' not in st.session_state:
        st.session_state['video'] = None

    if 'path' not in st.session_state:
        st.session_state['path'] = None
        
    st.title("Video Search")

    if st.session_state['video'] is None:

        file = load_video()
        if file is not None:
            if check_mp4(file) == False:
                st.write("File is not mp4 extension, please upload file .mp4")
                time.sleep(3)
                st.rerun()

            st.session_state['video'] = file
            st.session_state['path'] = os.path.abspath(file)
            st.rerun()

    else:
        
        if st.session_state['init'] == False:

            init_audio(file=st.session_state['video'], path=st.session_state['path'])
            init_frames(file=st.session_state['video'], path=st.session_state['path'])
            st.session_state['init'] = True

        mode_selection(file=st.session_state['video'], path=st.session_state['path'])


def init_frames(file, path):
    
    db = get_database()

    frame = db.return_table(table_name="frames")
    check = frame.search().where(f"video_name ='{file}'").limit(1).to_list()

    if len(check)==0:
        with st.spinner("Conversion video to frames"):
            conversion = get_conversion()
            conversion.convert_video_to_photos(path)
            conversion.add_db_frames()

def init_audio(file, path):

    db = get_database()

    audio = db.return_table(table_name="audio")
    check = audio.search().where(f"video_name = '{file}'").limit(1).to_list()

    if len(check) == 0:
        with st.spinner("Conversion video to transcript audio"):
            search_audio = get_audio_engine(path=path)
            search_audio.text_2_vectors()
            search_audio.add_2_db()

@st.cache_resource
def get_search_engine():
    return SearchEngine()

@st.cache_resource
def get_database():
    return Database()

@st.cache_resource
def get_conversion():
    return Conversion()

@st.cache_resource(max_entries=1)   # jezeli uzytknowik zaladuje nowy film to stary jest wyrzucony z ramu
def get_audio_engine(path):
    return SearchAudio(file_dir=path)

def mode_selection(file, path):

    search_frame = get_search_engine()
    search_audio = get_audio_engine(path=path)


    mode = st.selectbox("Select which mode would you like to use",
        ("1. Search by image", "2. Search by audio", "3. Search using both", "4. Load another video"))

    mode_number = mode[0]

    if mode_number == '4':
        st.session_state['video'] = None
        st.session_state['init'] = None
        st.session_state['path'] = None
        st.rerun()
                
    user_input = st.text_input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )

    if user_input.lower() == "q":
        st.rerun()

    if mode_number == "1":
        found = search_frame.find_photo(1, user_input)
        timestamp = found['timestamp']
        st.video(data=path, start_time=timestamp)

    elif mode_number == "2":
        found = search_audio.find(1, user_input)
        start_time = found['start_time']
        end_time = found['end_time']
        st.video(data=path, start_time=start_time)


    # elif mode_number == "3":
    #     found_frames = search_frame.find_photo(1, user_input)
    #     timestamp = found['timestamp']

    #     found_audio = search_audio.find(1, user_input)
    #     start_time = found['start_time']
    #     end_time = found['end_time']


if __name__=="__main__":
    main()