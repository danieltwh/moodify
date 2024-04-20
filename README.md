<div align="center">
  <p>
    <a href="https://github.com/danieltwh/moodify/" target="_blank">
      <img width="65%" src="https://raw.githubusercontent.com/danieltwh/moodify/main/frontend/public/logo.png">
    </a>
  </p>
</div>
<a href="https://github.com/danieltwh/moodify/" target="_blank">Moodify</a> is a machine learning powered solution that transforms subtle facial expressions and vocal nuances into clear, actionable insights, enabling you to gauge and respond effectively to your audience sentiments during presentations or helping you analyse your pitch for improvements before your high-stakes meetings. 
<br></br>
Please check out the latest application at <a href="https://github.com/danieltwh/moodify/">https://github.com/danieltwh/moodify</a> and start gaining insights into your meetings.
<br></br>

# <div align="center"> Moodify 😊😐☹️ </div>
## Table of Contents
- [Moodify](#moodify)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Project Structure](#project-structure)
  - [Notes](#notes)
  <!-- - [Installation](#installation-/-usage) -->
  - [Installation](#installation)
  - [Additional Setup Instructions](#additional-setup-instructions)
  - [Usage](#usage)
  - [Docker](#docker)

## Requirements
1. Python 3.10.7
2. Docker installed on your system
3. Docker-compose installed on your system
4. FFmpeg
    - To check if FFmpeg is install, run the following in terminal
    ```bash
    ffmpeg -version
    ```
    If you see a version number, that means ffmpeg is installed. Otherwise, please follow the next step to install it.
    - Download and install FFmpeg from [FFmpeg](https://ffmpeg.org/download.html)
      - For windows, you may find a guide on [PhoenixNap](https://phoenixnap.com/kb/ffmpeg-windows)

## Project Structure
```
.
├── app                     <- Moodify web app (backend)
│   ├── Dockerfile          <- for dockerising app
│   ├── main.py
│   ├── src
│   │   ├── face_detection  <- for detecting faces in videos
│   │   ├── Mood_detector   <- for detecting emotions from facial expression
│   │   ├── speech_emotion  <- for detecting emotions in speech 
│   │   └── speech_to_text  <- for transcription service
│   └── sql                 <- contains sql scripts
├── data                    <- contains datasets for training and testing
│   ├── Webcam Images       <- contains the latest facial data for training and testing the model
│   ├── Webcam Images (Augmented) <- contains augmented facial data 
│   ├── sample_videos       <- contains sample data for testing the application
├── frontend                <- Moodify web app (frontend)
│   ├── app                 <- main frontend app
│   └── components          <- frontend components
├── notebooks
│   ├── Classical Learning  <- notebooks for training classical ML for facial sentiment prediction
│   ├── Neural Networks     <- notebooks for training classical ML for facial sentiment prediction
│   ├── speech_emotion      <- notebooks for testing speech emotion model
│   ├── data_augmentation   <- notebooks for data augmentation of images data collected
│   └── XXX
├── postgres
│   ├── create_tables.sql   <- SQL file for creating the PostgreSQL tables
│   └── insert_values.sql   <- SQL file for inserting the pre-loaded data in PostgreSQL 
├── requirments.txt         <- required Python packages
├── xxx
└── docker-compose          <- docker compose file for Moodify
```

## Notes
To use the Moodify application, please follow the instructions in [Installation](#installation), [Additional Setup Instructions](#additional-setup-instructions)
and [Usage](#usage) sections.

## Installation
1. Create virtual environment
    ```bash
    conda create -n moodify python=3.10.7
    ```
2. Activate the virutal environment
    ```bash
    conda activate moodify
    ```
3. Install required packages
    - If you are using Windows, run  
    ```bash
    pip install -r requirements.txt
    ```
    - If you are using Mac, please switch to Windows. We do not gaurantee that the app will run without errors if you choose to run this on Mac due to Tensorflow incompatbilities on Apple silicon. 

   
## Additional Setup Instructions
As the ML model files are too big to be committed to Github, please follow the instructions below to obtain the model files before running the application:
1. Go to [Moodify Google Drive](https://drive.google.com/drive/folders/1i5fGPW_7CUtVyNmIXWhzFma4mWEo8MYH?usp=sharing) to access all the model files
2. Download the Face Detection weights:
    - In the [Moodify Google Drive](https://drive.google.com/drive/folders/1i5fGPW_7CUtVyNmIXWhzFma4mWEo8MYH?usp=sharing), go to the `face_detection` folder and download the `yolov8n-face.pt` file into the `app/src/face_detection` directory
3. Download the Mood Detector model:
    - In the [Moodify Google Drive](https://drive.google.com/drive/folders/1i5fGPW_7CUtVyNmIXWhzFma4mWEo8MYH?usp=sharing), go to the `Mood_detector` folder and download the `trained_emotion.keras` file into the `app/src/Mood_detector` directory

## Usage
1. Start the PostgreSQL and RabbitMQ docker. In the root directory of the repository, run the following in terminal:
    ```bash
    docker-compose up -d 
    ```

2. In another terminal, activate the virtaul environment and start the Moodify backend application
    ```bash
    cd app
    ```
    ```bash
    conda activate moodify
    ```
    ```bash
    python main.py
    ```
3. In another terminal, install and start the Moodify frontend application
    ```bash
    cd frontend
    ```
    ```bash
    npm i
    ```
    ```bash
    npm run dev
    ```
4. In another terminal, activate the virtual environment and start the Moodify video_analyser
    ```bash
    cd app
    ```
    ```bash
    conda activate moodify
    ```
    ```bash
    python video_analyser.py
    ```
    If the vdeo_analyser.py stops running / face issues, repeat this step to re-run the script in the terminal.
5. Access the Moodify application at `http://localhost:3000/`
    - Open your webbrowser
    - Enter the following url: `http://localhost:3000/`
    - You may use the videos found in `data/sample_videos` to test the application

## Docker
Below are the details and instructions specific for the docker containers set-up. You need not run this to use the application.
1. Start the docker containers. In the root directory of the repository, run the following in terminal:
    ```bash
    docker-compose up -d
    ```

2. Connect to Postgres on PGAdmin
    - Host: localhost
    - Port: 5455
    - User: user
    - Password: password
    Keep the other settings as default
    DB available at `localhost:5455`

3. RabbitMQ available at `localhost:5672`. RabbitMQ Web UI available at `localhost:15672`

4. To shutdown the application, run the following command.
    ```bash
    docker-compose down -v
    ```


