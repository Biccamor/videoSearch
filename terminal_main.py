from engines.model import SearchEngine
from engines.video_conversion import  Conversion
from engines.hearing_model import SearchAudio
from database import Database
import filetype

class App():

    def __init__(self, file: str):
        self.conversion = Conversion() 
        self.search_frame = SearchEngine(device='cpu')
        self.file = file

        self.search_audio = SearchAudio(file_dir=self.file)

    def check_file(self):
        
        bytes_data = self.file.read(2048)
        check = filetype.guess(bytes_data)
        self.file.seek(0)
        if check is None:
            return False
        
        if check.mime == 'video/mp4': 
            return True

        return False


    def get_file(self):
        
        db = Database()
        frame = db.return_table(table_name="frames")

        check = frame.search().where(f"video_name ='{self.file}'").limit(1).to_list()

        if len(check)==0: 
            self.conversion.convert_video_to_photos(self.file)
            self.search_audio.text_2_vectors()


    def run(self):
        
        self.conversion.add_db_frames()
        self.search_audio.add_2_db()

        while True:
             print("------------------------------------------------------------------------------------\n")
             print("Choose mode \n1. Frame Searching \n2. Audio Searching " \
                "\n3. Both Modes \n4. Exit")
             print("------------------------------------------------------------------------------------\n")
             mode = input("Wpisz numer trybu: \n")
             if mode == "4" or mode not in ["1", "2", "3"]:
                 break
             
             user_input = input("What are you looking for in a video? to exit click q: " )
             
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
                print("Search for frames \n", found_frames)

                found_audio = self.search_audio.find(3, user_input)
                print("Search for sound \n", found_audio)


if __name__ == "__main__":
    file_name = input("Type name of your file .mp4 (first put in the folder)")
    app = App()

    if app.check_file() == True:
        app.get_file()
        app.run()
    else: 
        raise "The File is not mp4"