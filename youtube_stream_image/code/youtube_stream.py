import os
import subprocess

YOUTUBE_LIVE_KEY = os.environ['YOUTUBE_LIVE_KEY']

# avconv has the same functionality as ffmpeg
STREAM_COMMAND = ["avconv", "-ar", "44100", "-ac", "2", "-f", "s16le", "-i", "/dev/zero", "-f", "video4linux2", "-s",
                  "640x360", "-r", "10", "-i", "/dev/video0", "-f", "flv",
                  "rtmp://a.rtmp.youtube.com/live2/{0}".format(YOUTUBE_LIVE_KEY)]


class YoutubeStream:
    def __init__(self):
        self.process = None

    def start_stream(self):
        if self.process is not None:
            raise ValueError("Streaming is in progress")
        self.process = subprocess.Popen(STREAM_COMMAND)

    def stop_stream(self):
        if self.process is None:
            raise ValueError("Streaming is not in progress")
        self.process.kill()
        self.process = None

    def get_process_info(self):
        _status_key = "status"
        _pid_key = "pid"

        status_dict = {_status_key: "not running", _pid_key: "-1"}
        if self.process is None:
            return status_dict

        status_dict[_status_key] = "running"
        status_dict[_pid_key] = self.process.pid

        return status_dict
