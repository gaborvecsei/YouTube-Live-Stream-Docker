import logging

from flask import Flask, jsonify

from youtube_stream import YoutubeStream

app = Flask(__name__)

file_handler = logging.FileHandler('stream_rest_api.log')
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(logger_formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

youtube_stream = YoutubeStream()


def response(code, msg):
    status_code = code
    message = {
        'status_code': status_code,
        'message': msg
    }
    resp = jsonify(message)
    resp.status_code = status_code
    return resp


@app.route("/youtube_stream_api", methods=["GET", "POST"])
def index():
    app.logger.info("Is this the real life? Or is this just fantasy?")
    return "Youtube Strem API"


@app.route("/youtube_stream_api/start", methods=["GET", "POST"])
def start_stream():
    app.logger.info("Starting youtube stream")
    try:
        youtube_stream.start_stream()
    except Exception as e:
        app.logger.error("Error when starting stream: {0}".format(e))
        return response(404, "Error: {0}".format(e))
    return response(200, "Streaming successfully started")


@app.route("/youtube_stream_api/stop", methods=["GET", "POST"])
def stop_stream():
    app.logger.info("Stopping youtube stream")
    try:
        youtube_stream.stop_stream()
    except Exception as e:
        app.logger.error("Error when stopping stream: {0}".format(e))
        return response(404, "Error: {0}".format(e))
    return response(200, "Streaming successfully stopped")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
