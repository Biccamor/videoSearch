from faster_whisper import WhisperModel, BatchedInferencePipeline
from transformers import AutoProcessor, AutoModel
import torch

class SearchAudio():

    def __init__(self, audio_path: str, device: str='cpu'):
        self.audio_path = audio_path
        self.device = device
        if device=='cpu':
            self.compute_type = "int8"
        else:
            self.compute_type = "float16"
        
        self.model = WhisperModel('medium', device=self.device, compute_type=self.compute_type)
        self.batched_model = BatchedInferencePipeline(model=self.model)
        
        self.MODEL_NAME = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        self.text_model = AutoModel.from_pretrained(self.text_model)
        self.processor =  AutoProcessor.from_pretrained(self.text_model)

    #code from https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def transcription(self):
        
        segments, info = self.batched_model.transcribe(audio=self.audio_path, batch_size=4)
        for segment in segments:
            print(segment)

        
if __name__ == "__main__":

    search = SearchAudio()

    search.transcription()