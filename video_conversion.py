import subprocess 
import cv2
import os

def convert_video_to_audio(video_file_path: str, audio_file_path: str):
    """" nie skonczone """
    command = f"ffmpeg -i {video_file_path} -vn -ar 16000 -ac 1 -acodec -b:a 192k {audio_file_path}"
    subprocess.call(command, shell=False)


# def delete_files(directory: str='frames'):

#     for file in os.listdir(directory):
#         file_path = os.path.join(directory, file) 
#         if os.path.isfile(file_path): 
#             os.remove(file_path)

def convert_video_to_photos(video_path: str):
    cap = cv2.VideoCapture(video_path)
    OUTPUT_DIR = "frames"

    if os.path.exists(OUTPUT_DIR) == False: 
        os.makedirs(OUTPUT_DIR)

    # else:
    #     if len(os.listdir(OUTPUT_DIR)) > 0:
    #         delete_files(OUTPUT_DIR)

    if not cap.isOpened():
        raise Exception("Video not opened")
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    count = 0
    frames_count=0
    
    while True: 
        success, frame = cap.read()
        
        if not success: break

        if frames_count%fps==0:
            save_path = os.path.join(OUTPUT_DIR, f'frame_{count}.png')
            cv2.imwrite(save_path, frame)
            count+=1
    
        frames_count+=1

    cap.release()


convert_video_to_photos("Family Guy _Every Pizza Place Salad_.mp4")