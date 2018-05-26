FROM resin/rpi-raspbian:jessie

ADD code /code
WORKDIR /code

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential unzip wget \
        cmake pkg-config git python3 python3-pip \
        nmap arp-scan

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT "python3 /code/start_app.py"
