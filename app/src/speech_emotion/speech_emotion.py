import numpy as np
import pandas as pd
import librosa

import sys
import os

from transformers import AutoProcessor, AutoModelForAudioClassification, Wav2Vec2FeatureExtractor, Wav2Vec2CTCTokenizer

from pydub import AudioSegment
from pydub.utils import make_chunks

import scipy


# model1 = AutoModelForAudioClassification.from_pretrained("ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
# feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53")

# feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")
# model1 = AutoModelForAudioClassification.from_pretrained("ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")
model1 = AutoModelForAudioClassification.from_pretrained("r-f/wav2vec-english-speech-emotion-recognition")

# id2label = {
#         0: "angry",
#         1: "calm",
#         2: "disgust",
#         3: "fearful",
#         4: "happy",
#         5: "neutral",
#         6: "sad",
#         7: "surprised"
#     }

# id2label = {
#         0: "negative",
#         1: "neutral",
#         2: "negative",
#         3: "negative",
#         4: "positive",
#         5: "neutral",
#         6: "negative",
#         7: "positive"
#     }

id2label = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

# label2id = {y:x for x, y in id2label.items()}
label2id = {
        "angry": 0,
        "neutral": 1,
        "happy": 2,
}

label2newlabel = {
        "angry": "negative",
        "neutral": "neutral",
        "happy": "positive",
}

oldid2newlabel = {
        0: "negative",        
        4: "positive",
        5: "neutral",
}

# id2newid = {
#     0: 1
# }

UPLOAD_DIR = os.path.abspath("uploads")

def ensure_sample_rate(original_sample_rate, waveform,
                    desired_sample_rate=16000):
    """Resample waveform if required."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) /
                                original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform

def speech_file_to_array_fn(filename):
    speech_array, sampling_rate = librosa.load(filename, sr=16_000)
    if sampling_rate != 16_000:
        sampling_rate, speech_array= ensure_sample_rate(sampling_rate, speech_array)
    return speech_array


def predict_emotion(wave_data):
    # sig, sr = librosa.load(audio_file)
    # wav_data = librosa.resample(sig, orig_sr=sr, target_sr=16000)

    # sound_array = np.array(wav_data.get_array_of_samples())

    input = feature_extractor(
        raw_speech=wave_data,
        sampling_rate=16000,
        padding=True,
        return_tensors="pt")

    result = model1.forward(input.input_values.float())
    # making sense of the result 

    # interp = dict(zip(id2label.values(), list(round(float(i),4) for i in result[0][0])))

    interp = {"negative": 0.0, "neutral": 0.0, "positive": 0.0}
    
    max_idx = -1
    max_val = -1.0
    for idx, val in enumerate(result[0][0].detach().numpy()):
        if idx in oldid2newlabel:
            interp[oldid2newlabel[idx]] += val
            if val > max_val:
                max_idx = idx
                max_val = val

    # pred = np.argmax(result[0][0].detach().numpy())
    pred = oldid2newlabel[max_idx]
    return pred, interp

def analyse_audio(audio):
    chunk_length_ms = 1000
    # chunk_length_ms = 16_000
    chunks = make_chunks(audio, chunk_length_ms)

    preds = []
    interps = []
    for chunk in chunks:
        if len(chunk) < 1000:
            continue
        pred, interp = predict_emotion(np.array(chunk.get_array_of_samples()))

        

        # pred, interp = predict_emotion(chunk)
        # preds.append(pred)
                    
        preds.append(pred)
        interps.append(interp)

    # preds_str = list(map(lambda x: id2label[x], preds))
    preds_str = preds
    return preds_str, interps

def analyse_audio_filename(filename):
    file, ext = filename.split(".")
    file_path = os.path.join(UPLOAD_DIR, filename)
    # print(file_path)
    if not os.path.isfile(file_path):
        print("[ERROR] Audio script: File not found")
        return 
    elif ext == "mp4":
        audio = AudioSegment.from_file(file_path, format="mp4")
    elif ext == "wav":
        audio = AudioSegment.from_file(filename, format = "wav")

    return analyse_audio(audio)

def analyse_audio_path(file_path):
    ls = file_path.split(".")
    ext = ls[-1]
    # file_path = os.path.join(UPLOAD_DIR, filename)
    # print(file_path)
    if not os.path.isfile(file_path):
        print("[ERROR] Audio script: File not found")
        return 
    elif ext == "mp4":
        audio = AudioSegment.from_file(file_path, format="mp4")
        audio = audio.set_frame_rate(16_000)
        # audio = speech_file_to_array_fn(file_path)
    # elif ext == "wav":
    #     audio = AudioSegment.from_file(file_path, format = "wav")
    
    return analyse_audio(audio)




if __name__ == "__main__":
    data_dir = os.path.join("../../../", "data", "sample_videos")
    filename = "video4.mp4"
    path = os.path.join(data_dir, filename)

    # preds, interps = analyse_audio("video1.mp4")
    # preds, interps = analyse_audio_path("video1.")
    preds, interps = analyse_audio_path(path)
    print(preds)
    print(interps)

    # print([id2label[pred_id] for pred_id in preds])
    
    

    