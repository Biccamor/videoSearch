import subprocess 
import cv2
import os
import uuid
from pathlib import Path
from PIL import Image
import torch
import torch.nn.functional as F
from database import Database
from transformers import AutoProcessor, AutoModel

class Conversion():

    def __init__(self, frames: int=1, device: str = 'cpu'):
        self.frames = frames
        self.OUTPUT_DIR = "data"
        self.OUTPUT_DIR_FRAMES = ""
        self.OUTPUT_DIR_AUDIO = ""
        self.frame_data = []
        self.db = Database()
        self.MODEL_IMAGE_NAME = "google/siglip2-base-patch16-224"
        self.processor = AutoProcessor.from_pretrained(self.MODEL_IMAGE_NAME, use_fast=True)
        self.model = AutoModel.from_pretrained(self.MODEL_IMAGE_NAME, dtype=torch.float32, device_map=device,
                                                 attn_implementation="sdpa")

    def convert_video_to_audio(self, video_file_path: str):
        file_path = os.path.join(self.OUTPUT_DIR_AUDIO, "audio.wav")

        #whisper openai uses 16000 sample rate, wav file type, and one chanell (mono)

        command = [
            "ffmpeg",
            "-i", video_file_path, "-vn", "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-y", file_path
        ]

        subprocess.run(command, check=True)

    def is_opened_error(self):
        if not self.cap.isOpened():
            raise Exception("Video not opened")
        
    def convert_video_to_photos(self, video_path: str):
        
        self.cap = cv2.VideoCapture(video_path)

        self.is_opened_error()
        
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        count = 0
        frames_count=0

        while True: 
            success, frame = self.cap.read()
            
            if not success: break

            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)


            if frames_count%(fps//self.frames)==0:
                count+=1

                vector = self.images_to_vectors(frame)

                vector = vector.detach().flatten().tolist()

                self.frame_data.append({
                    "id": str(uuid.uuid4()),
                    "video_name": os.path.basename(video_path),
                    "timestamp": count-1,
                    "vector": vector,
                    })
        
            frames_count+=1

        self.cap.release()


    def images_to_vectors(self, image) -> torch.Tensor:

        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)

        self.image_features = F.normalize(image_features, dim=1, p=2)

        return self.image_features

    def add_db(self):

        frames_db = self.db.return_table(table_name="frames")
        
        frames_db.add(self.frame_data)
        

if __name__ == "__main__":
    c = Conversion()

    c.convert_video_to_audio('familyguy.mp4')