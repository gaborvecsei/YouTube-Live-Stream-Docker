ffmpeg -ar 44100 -ac 2 -f s16le -i /dev/zero -f video4linux2 -s 640x360 -r 10 -i /dev/video0 -vf "eq=brightness=0.5:saturation=2" -f flv "rtmp://a.rtmp.youtube.com/live2/$1"
