FROM debian:jessie

RUN apt-get -q update && \
        apt-get install -y \
            python3 \
            python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT "/bin/bash"
