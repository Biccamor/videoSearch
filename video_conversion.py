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
        self.frame_data = []

    def convert_video_to_audio(self, video_file_path: str):
        file_path = os.path.join(self.OUTPUT_DIR_AUDIO, "audio.wav")

        #whisper openai uses 16000 sample rate, wav file type, and one chanell (mono)


        command = [
            "ffmpeg",
            "-i", video_file_path, "-vn", "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-y", file_path
        ]

        subprocess.run(command, check=True)

    def create_directory(self):

        path = Path(self.OUTPUT_DIR)
        id_for_dir = str(uuid.uuid4())
        self.OUTPUT_DIR = path / id_for_dir
        self.OUTPUT_DIR_FRAMES = path / id_for_dir / "frames"
        self.OUTPUT_DIR_AUDIO = path / id_for_dir  / "audio"
        print(self.OUTPUT_DIR_AUDIO)

        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR_AUDIO.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR_FRAMES.mkdir(parents=True, exist_ok=True)

    
    def return_path_frames(self):
        return self.OUTPUT_DIR_FRAMES
    
    def return_path_audio(self):
        return self.OUTPUT_DIR_AUDIO

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
                save_path = os.path.join(self.OUTPUT_DIR_FRAMES, f'frame_{count}.png')
                cv2.imwrite(save_path, frame)
                count+=1
                
                self.frame_data.append({"frame_path": save_path / frame, 
                                   "timestamp": count,
                                   "vector": None})
        
            frames_count+=1

        cap.release()

if __name__ == "__main__":
    c = Conversion()

    c.create_directory()
    c.convert_video_to_audio('familyguy.mp4')