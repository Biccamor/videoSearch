CREATE TABLE Videos(
    video_id SERIAL PRIMARY KEY,
    name varchar(264)
); 

CREATE TABLE Frames(
    frame_id SERIAL PRIMARY KEY,
    video_id INT, 
    video_id FOREIGN KEY Videos(video_id)
); 