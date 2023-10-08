FROM python:3.9

WORKDIR /game

COPY src src
COPY requirements.txt .

RUN apt-get update && pip install --no-cache-dir -r requirements.txt
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev

CMD ["python", "game.py"]