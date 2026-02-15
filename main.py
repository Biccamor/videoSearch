from model import SearchEngine
from video_conversion import  Conversion
from hearing_model import SearchAudio
import gc


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

        while True:
             print("W jakim trybie chcesz użyć wyszukiwarki? \n1. Szukanie po obrazach \n2. Szukanie po dźwięku " \
                "\n 3. Oba tryby \n4. Wyjście")
             mode = input("Wpisz numer trybu: \n")
             if mode == "4" or mode not in ["1", "2", "3"]:
                 break
             
             user_input = input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )
             
             if user_input.lower() == "q":
                 break
            
             if mode == "1":
                found = self.search_frame.find_photo(3, user_input)
                print(found)

             elif mode == "2":
                found = self.search_audio.find(3, user_input)
                print(found)

             elif mode == "3":
                found_frames = self.search_frame.find_photo(3, user_input)
                print("Wyniki wyszukiwania po obrazach: \n", found_frames)

                found_audio = self.search_audio.find(3, user_input)
                print("Wyniki wyszukiwania po dźwięku: \n", found_audio)


if __name__ == "__main__":
    app = App()

    app.run()