import subprocess 
import cv2
import os
import uuid
from pathlib import Path

class Conversion():

    def __init__(self, frames: int=1):
        self.frames = frames
        self.OUTPUT_DIR = "data"
        self.OUTPUT_DIR_FRAMES = ""
        self.OUTPUT_DIR_AUDIO = ""
        
    def convert_video_to_audio(self, video_file_path: str):
        """" nie skonczone """
        command = f"ffmpeg -i {video_file_path} -vn -ar 16000 -ac 1 -acodec -b:a 192k {self.OUTPUT_DIR_AUDIO}"
        subprocess.call(command, shell=False)

    def create_directory(self):

        path = Path(self.OUTPUT_DIR)
        id_for_dir = str(uuid.uuid4())
        self.OUTPUT_DIR = path / id_for_dir
        self.OUTPUT_DIR_FRAMES = self.OUTPUT_DIR / "frames"
        self.OUTPUT_DIR_AUDIO = self.OUTPUT_DIR / "audio"

        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR_AUDIO.mkdir(parents=False, exist_ok=True)
        self.OUTPUT_DIR_FRAMES.mkdir(parents=False, exist_ok=True)

    def convert_video_to_photos(self, video_path: str):
        
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise Exception("Video not opened")
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        count = 0
        frames_count=0
        
        while True: 
            success, frame = cap.read()
            
            if not success: break

            if frames_count%(fps//self.frames)==0:
                save_path = os.path.join(self.OUTPUT_DIR, f'frame_{count}.png')
                cv2.imwrite(save_path, frame)
                count+=1
        
            frames_count+=1

        cap.release()