from model import SearchEngine
from video_conversion import  Conversion

search = SearchEngine(image_dir='frames', device='cpu')

conversion = Conversion()

conversion.create_directory()

file = input("Wpisz nazwe pliku wideo do wczytania: \n")
conversion.convert_video_to_photos(file)
conversion.convert_video_to_audio(file)

search.get_image_features()

while True:
    
    user_input = input("Napisz czego szukasz dokladnie w filmie przesłanym przykładowe zapytanie: żeby wyjśc kliknij q: " )
    if user_input == 'q':
        break

    found = search.find_photo(number_of_photos=3, text=user_input)
    print(found)