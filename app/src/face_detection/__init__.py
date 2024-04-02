from .face_detection import FaceDetection

import os


# print(os.getcwd())

model_dir = os.path.join(os.path.dirname(__file__), "model")
filename = "yolov8n-face.pt"
path = os.path.join(model_dir, filename)
print(path)
face_detection_model = FaceDetection(path)

