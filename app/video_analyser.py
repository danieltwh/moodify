import os
import shutil
import sys
import subprocess
import re
import time
from datetime import datetime
import json
import logging

import models

import pika
import asyncio

# Load the db and rabbitmq connectors
from extensions import init_postgres, open_rabbitmq_connection

# Load the db modesl
import models

# Load the models
from src.Mood_detector import face_emotion_detector
from src import speech_emotion
from src.face_detection import face_detection_model
from src.speech_to_text import speech_to_text_model



formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
handler = logging.FileHandler(filename="logs/video-analyser.log", mode="w")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

UPLOAD_DIR = "uploads"


async def analyse_video(video_id, video_name):
    path = os.path.join(UPLOAD_DIR, video_id, video_name)
    face_detection_model.save_cropped_faces(video_id, path)

    path_to_cropped_face = os.path.join(UPLOAD_DIR, video_id, "img/crops/face")

    preds, interps = face_emotion_detector.analyse_emotion(path_to_cropped_face)

    print("here: analyse video")
    return preds, interps
    # return None, None


async def analyse_speech(path):
    preds, interps = speech_emotion.analyse_audio_path(path)
    print("here: analyse speech")
    return preds, interps


async def speech_to_text(video_id, video_name):
    path = os.path.join(UPLOAD_DIR, video_id, video_name)
    text = speech_to_text_model.analyse(video_id, path)

    print("here: speech to text")
    return text


async def main():
    while True:
        with open_rabbitmq_connection() as channel:
            method_frame, header_frame, body = channel.basic_get(
                queue="analyse-video-queue"
            )

            if method_frame != None and method_frame.NAME == "Basic.GetOk":
                # print(method_frame)

                try:
                    with init_postgres() as postgres:
                        data = json.loads(body)

                        video_id = data["video_id"]

                        video = (
                            postgres.query(models.Videos)
                            .filter(models.Videos.video_id == video_id)
                            .first()
                        )

                        if not video:
                            logger.error(f"Failed: Video {video_id} not found in DB")
                            break

                        video_name = video.video_name

                        path = os.path.join(UPLOAD_DIR, video_id, video_name)
                        # Process Video
                        print(video_id)

                        task_ls = []

                        if os.path.isdir(os.path.join(UPLOAD_DIR, video_id, "img")):
                            shutil.rmtree(os.path.join(UPLOAD_DIR, video_id, "img"))

                        task_ls.append(
                            asyncio.create_task(analyse_video(video_id, video_name))
                        )

                        task_ls.append(asyncio.create_task(analyse_speech(path)))

                        if os.path.isdir(os.path.join(UPLOAD_DIR, video_id, "txt")):
                            shutil.rmtree(os.path.join(UPLOAD_DIR, video_id, "txt"))
                        task_ls.append(
                            asyncio.create_task(
                                speech_to_text(video_id, video_name)
                            )
                        )

                        # Retrieve the results
                        results = await asyncio.gather(*task_ls)

                        speech_preds, speech_interps = results[1]
                        text = results[2]
                        face_preds, face_interps = results[0]

                        overall_speech_preds = None
                        overall_speech_interps = None
                        if speech_preds and speech_interps:
                            overall_speech_preds = max(set(speech_preds), key=speech_preds.count)
                            overall_speech_interps = {k: sum(d[k] for d in speech_interps) / len(speech_interps) for k in speech_interps[0]}

                        overall_face_preds = None
                        overall_face_interps = None
                        if face_preds and face_interps:
                            overall_face_preds = max(set(face_preds), key=face_preds.count)
                            overall_face_interps = {k: sum(d[k] for d in face_interps) / len(face_interps) for k in face_interps[0]}

                        body = {
                            "aggregates": {
                                "speech_data": {
                                    "preds_str": [overall_speech_preds],
                                    "interps": [overall_speech_interps],
                                }, 
                                "face_emotion": {
                                    "preds_str": [overall_face_preds],
                                    "interps": [overall_face_interps],
                                }
                            },
                            "speech_data": {
                                "preds_str": speech_preds,
                                "interps": speech_interps,
                            },
                            "text": text,
                            'face_emotion': {
                                "preds_str": face_preds, 
                                "interps": face_interps,
                            }
                        }

                        
                        print("HERE 1")

                        print(body)

                        # body = {
                        #      "abc": 2
                        # }
                        # Update video details
                        video.predictions = json.dumps(body, default=int)
                        video.video_status = "completed"
                        # video.predictions = "abc"
                        # video.predictions = 'abc'

                        print("HERE 2")
                        postgres.commit()

                        print("HERE 3")
                    
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    print("Done", video_id, video_name)
                    

                except Exception as err:
                    # print("[ERROR] Failed to process message")
                    # print(body)
                    # print(err)
                    logger.error(f"Failed to process message: {body}")
                    logger.exception(err)

                    # channel.basic_publish(exchange="amq.direct", routing_key="analyse-video-queue",
                    #     body = body
                    # )

            else:
                logger.info("No message")
        time.sleep(3)


if __name__ == "__main__":
    # main()
    asyncio.run(main())
