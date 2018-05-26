FROM resin/rpi-raspbian:jessie

ADD code /code
WORKDIR /code

RUN apt-get update && apt-get upgrade -y
# libav tools (avconv) has the same functionallity as ffmpeg (so we don't need to compile it)
RUN apt-get install -y build-essential unzip wget \
         libav-tools cmake pkg-config git python3 python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code

ENTRYPOINT "python3 /code/stream_rest_api.py"
