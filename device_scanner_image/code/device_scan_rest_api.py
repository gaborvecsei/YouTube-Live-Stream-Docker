import logging

from flask import Flask, jsonify

from connected_devices_scanner import ConnectedDevicesScanner
from youtube_stream import YoutubeStream

app = Flask(__name__)

file_handler = logging.FileHandler('stream_rest_api.log')
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(logger_formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# These are the MAC addresses which if present at the network the streaming should stop
STOP_WHEN_PRESENT_MAC_DICT = {"00:11:22:aa:33:bb": "gabor_phone",
                              "99:12:10:aa:33:bb": "mona_phone"}
WHITELIST_MACS = list(STOP_WHEN_PRESENT_MAC_DICT.keys())
WHITELIST_MACS = [x.lower() for x in WHITELIST_MACS]

DEVICE_SCANNER = ConnectedDevicesScanner.from_arp_scan()
WAIT_TIME_BETWEEN_SCANS_IN_MINUTES = 0.5
IS_STREAM_RUNNING = False


def response(status_code, msg):
    message = {
        'status_code': status_code,
        'message': msg
    }
    resp = jsonify(message)
    resp.status_code = status_code
    return resp


def get_present_devices():
    """
    Checks if whitelist devices are present or not
    :return: True if there are device, False if the are not
    """
    found_macs = DEVICE_SCANNER.find_connected_device_macs()

    present_device_macs = set(found_macs).intersection(set(WHITELIST_MACS))
    present_device_macs_dict = {x: STOP_WHEN_PRESENT_MAC_DICT[x] for x in present_device_macs}

    if len(present_device_macs) > 0:
        return present_device_macs_dict

    return None


@app.route("/device_scan_api", methods=["GET", "POST"])
def index():
    app.logger.info("Is this the real life? Or is this just fantasy?")
    return "Device Scan API"


@app.route("/device_scan_api/scan", methods=["GET", "POST"])
def start_stream():
    app.logger.info("Scanning for devices")
    try:
        found_devices = get_present_devices()
        response_dict = {"devices": found_devices}
        resp = jsonify(response_dict)
        resp.status_code = 200
        return resp
    except Exception as e:
        app.logger.error("Error when scanning devices: {0}".format(e))
        return response(404, "Error: {0}".format(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
