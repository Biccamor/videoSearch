from faster_whisper import WhisperModel, BatchedInferencePipeline
from transformers import AutoProcessor, AutoModel
import torch
import os
import subprocess

class SearchAudio():


    def __init__(self, file_dir: str, device: str='cpu'):
        
        self.file_dir = file_dir
        
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

        self.MIN_COUNT = 20
        self.convert_video_to_audio()


    def convert_video_to_audio(self):
        
        self.audio_path = os.path.splitext(self.file_dir)[0] + ".wav"

        if not os.path.exists(self.audio_path):
        #whisper openai uses 16000 sample rate, wav file type, and one chanell (mono)
            command = [
                "ffmpeg",
                "-i", self.file_dir, "-vn", "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-y", self.audio_path
            ]

            subprocess.run(command, check=True, capture_output=True)

    #code from https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


    def normalize_length(self):
        
        if not self.words_video: return

        self.clean_segments = []
        
        count = 0
        current_segment = ""
        current_start = None 

        for word in self.words_video:

            if current_start == None:
                current_start = word.start

            current_segment += word.word
            count += 1
             
            if count >= self.MIN_COUNT:
                

                if word.word.strip().endswith("."):   

                    new_segment = {
                        "segment": current_segment,
                        "start": current_start, 
                        "end": word.end
                    }

                    self.clean_segments.append(new_segment)
                    
                    current_segment = ""
                    current_start = None
                    count = 0


        if current_segment != "":

            new_segment = {
            "segment": current_segment,
            "start": current_start, 
            "end": word.end
            }
            
            self.clean_segments.append(new_segment)


    def transcription(self):
        
        raw_segments, _ = self.batched_model.transcribe(audio=self.audio_path, batch_size=4, vad_filter=True, word_timestamps=True)
        self.words_video = [] # words from segments with timestamtsp
        
        for segment in raw_segments:
            if segment.words:
                self.words_video.extend(segment.words)

        self.normalize_length()
        
        # for segment in raw_segments:
        #     segments.append({
        #         "start_time": segment.start,
        #         "end_time": segment.end,
        #         "text": segment.text
        #     })


    
if __name__ == "__main__":

    search = SearchAudio("familyguy.mp4")
    search.transcription()
    print(search.clean_segments)