import os
import subprocess

YOUTUBE_LIVE_KEY = os.environ['YOUTUBE_LIVE_KEY']

# avconv has the same functionality as ffmpeg
STREAM_COMMAND = ["avconv", "-loglevel", "quiet", "-ar", "44100", "-ac", "2", "-f", "s16le", "-i", "/dev/zero", "-f", "video4linux2", "-s",
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

    def force_stop_stream(self):
        command = ["kill", "-KILL", str(self.process.pid)]
        subprocess.check_call(command)
        self.process = None

    def check_process_health(self):
        if not self.is_stream_alive():
            if self.process is not None:
                # If there was a return code and the process obj is not None
                # that means the process stopped (connection reset by peer, etc...) so we need to
                # "reset" the process
                self.process = None

    def is_stream_alive(self):
        if self.process is not None:
            return_code = self.process.poll()
            if return_code is not None:
                return False
            else:
                return True
        return False
