from model import SearchEngine
from video_conversion import  Conversion
from hearing_model import SearchAudio

#TODO:
# gui
# dekompozycja convert_video_to_photos w video_conversion.py

class App():

    def __init__(self):
        self.conversion = Conversion() 
        self.search_frame = SearchEngine(device='cpu')
        self.file = "familyguy.mp4"

        self.search_audio = SearchAudio(file_dir=self.file)

    def get_file(self):
        
        # self.file = input("Wpisz nazwe pliku wideo do wczytania: \n")
        self.conversion.convert_video_to_photos(self.file)
        self.search_audio.text_2_vectors()

    def run(self):
        
        self.conversion.add_db_frames()
        self.search_audio.add_2_db()
        # self.search_audio.transcription()

        while True:
            
             user_input = input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )
             if user_input == 'q':
                 break

             found = self.search_frame.find_photo(number_of_photos=3, text=user_input, table="audio")
             print(found)


if __name__ == "__main__":
    app = App()

    app.get_file()
    app.run()