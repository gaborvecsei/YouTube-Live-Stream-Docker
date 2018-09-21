#!/bin/bash

# This script is only used when we would like to start streaming, when the Raspberry Pi (or other device)
# is turned on. This feature has it's own docker-compose.yml file

VIDEO_DEVICE=${1:-video0}

avconv -loglevel info -ar 44100 -ac 2 -f s16le -i /dev/zero \
        -f video4linux2 -s 640x480 -r 10 -i /dev/${VIDEO_DEVICE} \
        -vf "drawtext=fontfile=/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf:text='%{localtime\:%T}': fontcolor=white@0.8: x=0: y=0" \
        -qscale:v 2 -f flv rtmp://a.rtmp.youtube.com/live2/${YOUTUBE_LIVE_KEY}
