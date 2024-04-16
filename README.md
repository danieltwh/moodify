# Moodify
## Table of Contents
- [Moodify](#MedWatch)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#Requirements)
  - [Project Structure](#project-structure)
  - [Notes](#notes)
  <!-- - [Installation](#installation-/-usage) -->
  - [Installation](#installation)
  - [Usage](#usage)
  - [Docker](#docker)

## Requirements
1. Python 3.9.18
2. Docker installed on your system
3. Docker-compose installed on your system

## Project Structure
```
.
├── app                     <- Moodify web app
│   ├── Dockerfile          <- for dockerising app
│   ├── main.py
│   ├── src
│   │   ├── face_emotion    <- for detecting emotions from facial expression
│   │   ├── speech_emotion  <- for detecting emotions in speech 
│   │   └── XXX
│   └── sql                 <- contains sql scripts
├── data                    <- contains datasets for training and testing
│   ├── facial_emotion_data
│   ├── sample_videos
│   └── xxx
├── notebooks
│   ├── speech_emotion      
│   └── XXX
├── requirments.txt         <- required Python packages
├── xxx
└── docker-compose          <- docker compose file for MedWatch
```

## Notes

## Installation
1. Create virtual environment
    ```bash
    conda create -n moodify python=3.9.18
    ```
2. Activate the virutal environment
    ```bash
    conda activate moodify
    ```
3. Install required packages
    ```bash
    pip install -r requirements.txt
    ```
## Usage
1. Enter the app directory
    ```bash
    cd app
    ```
2. Start the Moodify application
    ```bash
    python main.py
    ```

## Docker
1. Activate the virutal environment
    ```bash
    docker-compose up -d --build 
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
    docker-compose down
    ```

<!-- 3. Backend API available at `localhost:5050` -->

<!-- 4. Frontend available at `localhost:80` -->


