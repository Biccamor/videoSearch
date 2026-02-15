from faster_whisper import WhisperModel, BatchedInferencePipeline
from sentence_transformers import SentenceTransformer
import os
import subprocess
import uuid
import numpy as np
from database import Database

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
        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.MIN_COUNT = 15
        self.convert_video_to_audio()
        self.audio_data = []
        self.db = Database()


    def convert_video_to_audio(self):
        
        self.audio_path = os.path.splitext(self.file_dir)[0] + ".wav"

        if not os.path.exists(self.audio_path):
        #whisper openai uses 16000 sample rate, wav file type, and one chanell (mono)
            command = [
                "ffmpeg",
                "-i", self.file_dir, "-vn", "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le", "-y", self.audio_path
            ]

            subprocess.run(command, check=True, capture_output=True)

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
                        "text": current_segment,
                        "start": current_start, 
                        "end": word.end
                    }

                    self.clean_segments.append(new_segment)
                    
                    current_segment = ""
                    current_start = None
                    count = 0


        if current_segment != "":

            new_segment = {
            "text": current_segment,
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
        
    
    def text_2_vectors(self):
        
        self.transcription()

        for segment in self.clean_segments: 
            
            embeddings = self.text_model.encode(segment["text"])
            print(embeddings.shape)

            self.audio_data.append({
                "id": str(uuid.uuid4()),
                "video_name": os.path.basename(self.file_dir),
                "start_time": segment["start"]-1,
                "end_time": segment["end"],
                "text": segment["text"],                
                "vector": embeddings.flatten().tolist()              
            }) 

    def find(self, number_of_moments: int, text: str):
        
        text_features = self.text_model.encode(text)
    
        db = self.db.return_table("audio")

        similarity = (
            db.search(text_features.flatten().astype(np.float32).tolist())
            .select(['video_name', 'start_time', 'end_time'])
            .metric("cosine")
            .limit(number_of_moments)
            .to_pandas()
        )

        self.accuracy = (100*(1-similarity['_distance']))

        return similarity[['video_name', 'start_time', 'end_time', '_distance']]

    def add_2_db(self):
        
        audio_db = self.db.return_table(table_name="audio")

        if audio_db.count_rows() == 0:
            audio_db.add(self.audio_data)

        # print(audio_db.count_rows()) 
        

    
if __name__ == "__main__":

    search = SearchAudio("familyguy.mp4")
    search.text_2_vectors()