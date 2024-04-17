from .mood_detector import EmotionDetector

# import os

# print(os.getcwd())

# face_emotion_detector = EmotionDetector('trained_emotion.keras')

face_emotion_detector = EmotionDetector(r'src/Mood_detector/trained_emotion.keras')

# print(new_detector.get_emotion('1.jpg'))