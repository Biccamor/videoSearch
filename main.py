from model import SearchEngine
from video_conversion import  Conversion
from hearing_model import SearchAudio

#TODO:
# zrob normalizacje dlugosci dzwieku w hearing modelu
# uzyj semantci search by znalezc najbardziej podobny do zapytania wektor
# polacz database z modelem do szukania dzwieku / trzeb wrzucic do video conversion zamiane transkrycpji na wektor
# gui

class App():

    def __init__(self):
        self.conversion = Conversion() 
        self.search_frame = SearchEngine(device='cpu')
        # self.search_audio = SearchAudio(audio_dir=self.audio_directory)

    def get_file(self):
        
        # self.file = input("Wpisz nazwe pliku wideo do wczytania: \n")
        self.file = "familyguy.mp4"
        self.conversion.convert_video_to_photos(self.file)
        # self.conversion.convert_video_to_audio(self.file)

    def run(self):
        
        self.conversion.add_db()
        # self.search_audio.transcription()

        while True:
            
             user_input = input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )
             if user_input == 'q':
                 break

             found = self.search_frame.find_photo(number_of_photos=3, text=user_input)
             print(found)


if __name__ == "__main__":
    app = App()

    app.get_file()
    app.run()