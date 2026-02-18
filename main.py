import streamlit as st
from engines.model import SearchEngine
from engines.video_conversion import Conversion
from engines.hearing_model import SearchAudio
import filetype 
import os
import time 
from database import Database
import shutil

TEMP_DIR = "temp_videos"

def load_video():

    """
    Function for loading video (mp4)

    Return: returns st.UploadedFile (file that users upload)
    """
    
    st.header("Load video")
    file = st.file_uploader("Choose mp4 file", type=['mp4'])
    return file

def check_mp4(file) -> bool:

    """
    checking if file is mp4 with mime types
    
    :param file: st.UploadedFile
    :return: bool: True if file is really mp4, false if not
    :rtype: bool
    """

    bytes_data = file.read(2048)
    check = filetype.guess(bytes_data)
    file.seek(0)
    if check is None:
        return False
    
    if check.mime == 'video/mp4': 
        return True

    return False


def save_video(uploaded_file):
    
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    for filename in os.listdir(TEMP_DIR):
        filepath = os.path.join(TEMP_DIR, filename)
        
        try:
            if filepath is not None:
                os.remove(filepath)
        except Exception as e:
            return e


    path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(path, 'wb') as file: 
        shutil.copyfileobj(uploaded_file,file)

    return path


def main():
    
    # create all session_states
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

            path = save_video(file)

            st.session_state['video'] = file
            st.session_state['path'] = path
            st.rerun()

    else:
        
        if st.session_state['init'] == False:

            init_audio(file=st.session_state['video'], path=st.session_state['path'])
            init_frames(file=st.session_state['video'], path=st.session_state['path'])
            st.session_state['init'] = True

        mode_selection(path=st.session_state['path'])


def init_frames(file, path):
    """
    Initialize all essenstial for searching frames
    
    :param file: st.UploadedFile
    :param path: string (path to file on tmp)
    """
    
    db = get_database()

    frame = db.return_table(table_name="frames")
    #check if file is already in database if it is not then we use conversion 
    check = frame.search().where(f"video_name ='{file.name}'").limit(1).to_list()

    if len(check)==0:
        with st.spinner("Conversion video to frames"):
            conversion = get_conversion()
            conversion.convert_video_to_photos(path)
            conversion.add_db_frames()

def init_audio(file, path):

    """
    Initialize all essenstial for searching through audio
    
    :param file: st.UploadedFile
    :param path: string (path to file on tmp)
    """

    db = get_database()

    audio = db.return_table(table_name="audio")
    #check if file is already in database if it is not then we use conversion 
    check = audio.search().where(f"video_name = '{file.name}'").limit(1).to_list()

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

@st.cache_resource(max_entries=1)   #if new file is loaded then the previous file is deleted from ram
def get_audio_engine(path):
    return SearchAudio(file_dir=path)

def mode_text(path: str, user_input: str, search_frame):
    found = search_frame.find_photo(1, user_input)
    timestamp = found['timestamp']-1
    st.video(data=path, start_time=timestamp)

def mode_audio(path: str, user_input: str, search_audio):
    found = search_audio.find(1, user_input)
    start_time = found['start_time']-1
    st.video(data=path, start_time=start_time)

def both_modes(path: str, user_input: str, search_audiop, search_frame):
    ...



def mode_selection(path: str):
    """
    Function for choosing mode and showing results
    
    :param path: str path to file 
    """

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

    ask_query = "Write what you are looking for in a video"

    user_input = st.text_input(ask_query, "")
    if user_input != "":
        if user_input.lower() == "q":
            st.rerun()

        if mode_number == "1":
            mode_text(path=path, user_input=user_input, search_frame=search_frame)

        elif mode_number == "2":
            mode_audio(path=path, user_input=user_input, search_audio=search_audio)

    # elif mode_number == "3":
    #     found_frames = search_frame.find_photo(1, user_input)
    #     timestamp = found['timestamp']

    #     found_audio = search_audio.find(1, user_input)
    #     start_time = found['start_time']
    #     end_time = found['end_time']


if __name__=="__main__":
    main()