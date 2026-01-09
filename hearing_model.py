from faster_whisper import WhisperModel, BatchedInferencePipeline
from transformers import AutoProcessor, AutoModel
import torch
from video_conversion import Conversion
import re

class SearchAudio():


    def __init__(self, audio_dir: str, device: str='cpu'):
        
        self.audio_dir = audio_dir
        self.audio_file = self.audio_dir / "audio.wav"
        
        self.device = device
        if device=='cpu':
            self.compute_type = "int8"
        else:
            self.compute_type = "float16"
        
        self.model = WhisperModel('medium', device=self.device, compute_type=self.compute_type)
        self.batched_model = BatchedInferencePipeline(model=self.model)
        
        self.MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        self.text_model = AutoModel.from_pretrained(self.MODEL_NAME)
        self.processor =  AutoProcessor.from_pretrained(self.MODEL_NAME)
        
    #code from https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def normalize_length(segment, self):
        if len(segment.text) <= 120 or "." not in segment.text or "?" not in segment.text or "!" not in segment.text: 
            return segment

        new_segments = []

        length_of_text = len(segment.text)




    def transcription(self):
        
        segments = []

        raw_segments, _ = self.batched_model.transcribe(audio=self.audio_file, batch_size=4, vad_filter=True)
        for segment in raw_segments:
            segments.append({
                "start_time": segment.start,
                "end_time": segment.end,
                "text": segment.text
            })
    

        
if __name__ == "__main__":

    search = SearchAudio()

    search.transcription()