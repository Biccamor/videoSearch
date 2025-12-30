import torch
from PIL import Image
from transformers import AutoProcessor, AutoModel, AutoTokenizer
import os
from deep_translator import GoogleTranslator
import torch.nn.functional as F


class SearchEngine():


    def __init__(self, image_dir: str, device: str='cpu'):
        self.MODEL_NAME = "google/siglip2-base-patch16-224"
        self.device = device
        self.model = AutoModel.from_pretrained(self.MODEL_NAME, 
                                               dtype=torch.float32, device_map=device,
                                                 attn_implementation="sdpa")
        self.processor = AutoProcessor.from_pretrained(self.MODEL_NAME, use_fast=True)
        self.translator = GoogleTranslator(source='pl', target="en")
        self.image_dir = image_dir
        self.list_images = []
        self.file_names = []
        self.image_features: torch.Tensor = None

    def get_image_features(self): 

        self.list_images = []
        self.file_names = []
        self.image_features = None

        images = os.listdir(self.image_dir)
        for file_path in images:
            path = os.path.join(self.image_dir, file_path)

            try: 
                image = Image.open(path)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                inputs = self.processor(images=image, return_tensors="pt")

                with torch.no_grad():
                    image_features = self.model.get_image_features(**inputs)
                self.list_images.append(image_features)
                self.file_names.append(file_path)
            except Exception as e:
                print(f"Pominięto {file_path}: {e}")

        vector_images = torch.cat(self.list_images, dim=0)

        self.image_features = F.normalize(vector_images, dim=1, p=2)


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

        if self.image_features == None:
            raise Exception("The function get_image_features should be called first")

        text_features_normalized = self.get_text_vector(text)

        similarity = text_features_normalized @ self.image_features.T

        probs = torch.sigmoid((similarity * self.model.logit_scale.exp()) + self.model.logit_bias)

        score, idx = torch.topk(probs, k=number_of_photos)
        top_indices = idx[0].tolist()
        top_probs = score[0].tolist()

        best_finds = []

        for i in range(len(top_indices)):
            idx_act = top_indices[i]
            # score_act = top_probs[i] * 100 # Zamiana n
                
            path_top_file = self.file_names[idx_act]
            path_of_file = os.path.join(self.image_dir, path_top_file)
            best_finds.append({"path": path_of_file, "score": top_probs[i]})

        return best_finds
