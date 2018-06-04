FROM debian:jessie

ADD code /code
WORKDIR /code

RUN apt-get -q update && \
        apt-get install -y \
            python3 \
            python3-pip \
            nmap \
            arp-scan

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT "python3 /code/start_app.py"
