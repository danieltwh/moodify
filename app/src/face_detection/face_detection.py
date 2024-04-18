from ultralytics import YOLO
import cv2
import os
import math

from moviepy.editor import VideoFileClip, CompositeAudioClip, AudioFileClip

UPLOAD_DIR = os.path.abspath("uploads")

class FaceDetection():
    def __init__(self, model_path) -> None:
        # self.model = YOLO("./model/yolov8n-face.pt")
        self.model = YOLO(model_path)
        # self.video_path = video_path
        
        
    def save_cropped_faces(self, session_id, video_path) -> list:
        """Cropped image faces are saved every second to the folder face_detection_results/img/crops/face .
            The image files have the name VIDEONAME_NUMBER.jpg e.g., video4_1.jpg
            
            Returns the list of image filepaths. 
        """
        # Open the video file
        video_capture = cv2.VideoCapture(video_path)

        # Get the video's FPS
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        totalNoFrames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        noSeconds = math.floor(totalNoFrames / fps)
        
        results = self.model.predict(source=video_path, save=False, save_crop=True, vid_stride=fps, project=f"uploads/{session_id}", name="img")
        # results = self.model.predict(source=video_path, save=True, save_crop=True, vid_stride=fps, project=f"uploads/{session_id}", name="img")
        
        img_paths = []
        
        video_name = video_path.split("/")[-1].split(".")[0]
        
        path = UPLOAD_DIR + f"/{session_id}/img/crops/face/" + video_name + "_"
        
        for i in range(1, noSeconds + 1):
            img_paths.append(path + str(i) + ".jpg")
        
        return img_paths
    
    def video_with_box(self, session_id, video_path) -> str:
        """Cropped image faces are saved every second to the folder face_detection_results/video .
           video file name is e.g., video4.mp4
           
           REturns the video filepath. 
        """
        results = self.model.predict(source=video_path, save=True, vid_stride=1, save_crop=False, project=f"uploads/{session_id}", name="video")
        
        video_filename = video_path.split("/")[-1]
        
        return UPLOAD_DIR + "/face_detection_results/video/" + video_filename
    

    def draw_face_box_on_video(self, session_id, video_name):
        video_dir = os.path.join(UPLOAD_DIR, session_id)
        video_path = os.path.join(video_dir, video_name)

        # temp_file_name = video_path.split("/")[-2]


        VideoFileClip(video_path).audio.write_audiofile(
            os.path.join(video_dir, f"audio.mp3")
        )

        self.model.predict(
            source=video_path,
            save=True,
            vid_stride=1,
            save_crop=False,
            project=video_dir,
            name="face_box",
        )

        video_with_box = VideoFileClip(os.path.join(video_dir, "face_box", video_name))
        new_audio_clip = AudioFileClip(os.path.join(video_dir, f"audio.mp3"))

        video_with_box.audio = CompositeAudioClip([new_audio_clip])

        # input_path = input_path.replace(video_name, "video_with_face_box")

        video_name_without_ext, file_ext = video_name.split('.')

        # print("here")
        output_path = os.path.join(video_dir, f"{video_name_without_ext}_with_face_box.{file_ext}")
        video_with_box.write_videofile(output_path)

        new_audio_clip.close()
        video_with_box.close()

        # os.remove(f"./{temp_file_name}.mp3")
        # os.remove(f"./face_detection_results/{temp_file_name}/video.avi")
        # os.rmdir(f"./face_detection_results/{temp_file_name}")
