CREATE TABLE Videos(
    video_id SERIAL PRIMARY KEY,
    name varchar(264),
    created_at TIMESTAMPZ,
    duration INT,
); 


id, nazwa, stworzenie, dlugosc w sekundach

CREATE TABLE Frames(
    frame_id SERIAL PRIMARY KEY,
    video_id INT, 
    video_id FOREIGN KEY Videos(video_id) ON DELETE CASCADE
    frame_path varchar(264),
    time_stamp FLOAT
    vektor VECTOR()
); 
