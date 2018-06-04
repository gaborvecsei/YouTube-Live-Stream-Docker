FROM debian:jessie

ADD code /code
WORKDIR /code

RUN apt-get -q update && \
        apt-get install -qy \
                python3 \
                python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /code

ENTRYPOINT "python3 /code/start_app.py"