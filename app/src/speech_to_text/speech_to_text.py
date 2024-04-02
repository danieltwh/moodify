from transformers import pipeline

from pydub import AudioSegment
from pydub.utils import make_chunks

from scipy.io import wavfile
import scipy

import librosa

import sys
import os
import random

UPLOAD_DIR = os.path.abspath("uploads")

class SpeechToText():
    def __init__(self) -> None:
        # self.model = pipeline("automatic-speech-recognition",
		# 	   model="facebook/wav2vec2-base-960h")
        self.model = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-large-v2",
                chunk_length_s=30,
                )
        
    
    def ensure_sample_rate(self, original_sample_rate, waveform,
                       desired_sample_rate=16000):
        """Resample waveform if required."""
        if original_sample_rate != desired_sample_rate:
            desired_length = int(round(float(len(waveform)) /
                                    original_sample_rate * desired_sample_rate))
            waveform = scipy.signal.resample(waveform, desired_length)
        return desired_sample_rate, waveform

    def speech_file_to_array_fn(self, filename):
        speech_array, sampling_rate = librosa.load(filename)
        if sampling_rate != 16_000:
            sampling_rate, speech_array= self.ensure_sample_rate(sampling_rate, speech_array)
        return speech_array

    def read_file(self, file_path):
        audio = AudioSegment.from_file(file_path, format="mp4")
        return audio

    def analyse(self, session_id, video_path) -> list:
        """Cropped image faces are saved every second to the folder face_detection_results/img/crops/face .
            The image files have the name VIDEONAME_NUMBER.jpg e.g., video4_1.jpg
            
            Returns the list of image filepaths. 
        """

        if not os.path.isfile(video_path):
            print("[ERROR] Audio script: File not found")
            return None
        
        audio = self.speech_file_to_array_fn(video_path)

        pred = self.model(audio)
        # text = pred['text'].capitalize()
        text = pred['text']

        text_dir = os.path.join(UPLOAD_DIR, f"{session_id}", "text")

        if not os.path.exists(text_dir):
            os.makedirs(text_dir)
        
        path = os.path.join(text_dir, "text.txt")

        with open(path, 'w') as file:
            file.write(text)
        return text
    

if __name__ == "__main__":
    speech_to_text_model = SpeechToText()
    
    path = os.path.join("..", "..", "uploads", "test", "video.mp4")

    text = speech_to_text_model.analyse("test",path)

    print(text)


    speech_to_text_model.analyse