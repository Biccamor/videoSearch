import torch
from PIL import Image
from transformers import AutoProcessor, AutoModel
import os
from deep_translator import GoogleTranslator
import torch.nn.functional as F
from database import Database

class SearchEngine():


    def __init__(self, device: str='cpu'):
        self.MODEL_NAME = "google/siglip2-base-patch16-224"
        self.device = device
        self.model = AutoModel.from_pretrained(self.MODEL_NAME, 
                                               dtype=torch.float32, device_map=device,
                                                 attn_implementation="sdpa")
        self.processor = AutoProcessor.from_pretrained(self.MODEL_NAME, use_fast=True)
        self.translator = GoogleTranslator(source='pl', target="en")
        self.db = Database()
        self.list_images = []
        self.file_names = []
        self.image_features: torch.Tensor = None


    def get_text_vector(self, text_input: str) -> torch.Tensor:
        
        if text_input == None or text_input == "":
            raise Exception("The query wasn't typed in")

        text_input_en = self.translator.translate(text_input)

        text_input_en = f"A photo of a {text_input_en}"
        input_token = self.processor(text=text_input_en, padding="max_length", return_tensors="pt")


        with torch.no_grad():
            text_features = self.model.get_text_features(**input_token)
        
        text_features_normalized = F.normalize(text_features, dim=1, p=2)

        return text_features_normalized
    

    def find_photo(self, number_of_photos: int, text: str):
        
        text_features = self.get_text_vector(text)
            
        frames_db = self.db.return_table("frames")

        similarity = (
            frames_db.search(text_features.detach().cpu().tolist())
            .select(['video_name', 'timestamp'])
            .distance_type("cosine")
            .limit(number_of_photos)
            .to_pandas()
        )

        self.accuracy = 100*similarity['_distance']

        return similarity[['video_name', 'timestamp','_distance']]
    
    def acc(self):
        return f"Model is {self.accuracy}% sure that it found the right moment of video by sight"