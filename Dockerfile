FROM resin/rpi-raspbian:jessie

RUN apt-get update

ADD ./code /code
WORKDIR /code
RUN chmod +x /code/stream_to_youtube.sh

RUN apt-get -qy install build-essential git

WORKDIR /root
RUN git clone https://github.com/FFmpeg/FFmpeg.git
workdir /root/FFmpeg
RUN apt-get install -qy libomxil-bellagio-dev
RUN ./configure --arch=armel --target-os=linux --enable-gpl --enable-omx --enable-omx-rpi --enable-nonfree
RUN make
RUN make install

RUN apt-get -qy install libraspberrypi-bin && rm -rf /var/lib/apt/lists/*

WORKDIR /code
RUN rm -rf /root/FFmpeg

ENTRYPOINT /code/stream_to_youtube.sh
