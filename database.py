import lancedb
import pyarrow as pa
import os 

class Database:

    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.db_path = os.path.join(self.home_dir, "videoSearch", "data")
        os.makedirs(self.db_path, exist_ok=True)
        self.db = lancedb.connect(self.db_path)

        #Tabela dla klatek filmow

        self.frames_schema = pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("video_name", pa.string()),
            pa.field("timestamp", pa.float32()),
            pa.field("vector", pa.list_(pa.float32(), 768)),
        ]
        )

        # Tabela dla audio

        self.audio_schema = pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("video_name", pa.string()),
            pa.field("start_time", pa.float32()),
            pa.field("end_time", pa.float32()),
            pa.field("timestamp", pa.float32()),
            pa.field("text", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 384))
        ]
        )

        self.init_database()

    def init_database(self):

        if "frames" not in self.db.table_names():
            self.db.create_table(name="frames", schema=self.frames_schema)

        if "audio" not in self.db.table_names():
            self.db.create_table(name="audio", schema=self.audio_schema)

    def return_table(self, table_name):
        return self.db.open_table(name=table_name)

    def return_db(self):
        return self.db

    def return_path(self):
        return self.db_path
        
    def is_frames_new(self) -> bool:
        return self.is_frames_created

    def is_audio_new(self) -> bool:
        return self.is_audio_created
