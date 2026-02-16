import lancedb
import pyarrow as pa
import os 

class Database:

    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "data")
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
            pa.field("text", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 384)),
        ]
        )

        self.init_database()

    def init_database(self):

        if "frames" not in self.db.table_names():
            self.db.create_table(name="frames", schema=self.frames_schema)

        if "audio" not in self.db.table_names():
            self.db.create_table(name="audio", schema=self.audio_schema)
    
        # self.db.create_table(name="frames", schema=self.frames_schema, mode="overwrite")

        # self.db.create_table(name="audio", schema=self.audio_schema, mode="overwrite")

    def return_table(self, table_name: str):
        return self.db.open_table(name=table_name)

    def return_db(self) -> lancedb.DBConnection:
        return self.db

    def return_path(self) -> str:
        return self.db_path
        
    def is_frames_new(self) -> bool:
        return self.is_frames_created

    def is_audio_new(self) -> bool:
        return self.is_audio_created


if __name__ == "__main__":
    db = Database().return_db()
    print(db.table_names())
    tbl = db.open_table(name="audio")
    print(tbl.schema)

    tbl_frames = db.open_table(name="frames")
    print(tbl_frames.schema)
