from model import SearchEngine
from video_conversion import  Conversion
from hearing_model import SearchAudio
from database import Database


#TODO:
# zrob normalizacje dlugosci dzwieku w hearing modelu
# uzyj semantci search by znalezc najbardziej podobny do zapytania wektor
# polacz database z modelem do szukania obrazu / trzeba wrzucic do video conversion funckej 
# ktora jest w model.py -> zamienia obraz na wektor inaczej ciezko wrzucic do bazy danych
# polacz database z modelem do szukania dzwieku / trzeb wrzucic do video conversion zamiane transkrycpji na wektor
# fastapi ?
# stworz ui 

class App():

    def __init__(self):
        self.conversion = Conversion() 
        self.db = Database()
        self.conversion.create_directory()
        self.audio_directory = self.conversion.return_path_audio()
        self.framed_directory = self.conversion.return_path_frames()
        self.search_frame = SearchEngine(image_dir=self.framed_directory, device='cpu')
        self.search_audio = SearchAudio(audio_dir=self.audio_directory)

    def get_file(self):
        
        self.file = input("Wpisz nazwe pliku wideo do wczytania: \n")
        self.conversion.convert_video_to_photos(self.file)
        self.conversion.convert_video_to_audio(self.file)

    def run(self):

        self.search_audio.transcription()

        # search.get_image_features()

        # while True:
            
        #     user_input = input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )
        #     if user_input == 'q':
        #         break

        #     found = search.find_photo(number_of_photos=3, text=user_input)
        #     print(found)


if __name__ == "__main__":
    app = App()

    app.get_file()
    app.run()