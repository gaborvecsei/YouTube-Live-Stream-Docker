import logging

from flask import Flask, jsonify

from connected_devices_scanner import ConnectedDevicesScanner

app = Flask(__name__)

file_handler = logging.FileHandler('device_scan_rest_api.log')
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(logger_formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

device_scanner = ConnectedDevicesScanner.from_arp_scan()


def response(status_code, msg):
    message = {
        'status_code': status_code,
        'message': msg
    }
    resp = jsonify(message)

    resp.status_code = status_code
    return resp


@app.route("/device_scan_api", methods=["GET", "POST"])
def index():
    app.logger.info("Is this the real life? Or is this just fantasy?")
    return "Device Scan API"


@app.route("/device_scan_api/scan", methods=["GET", "POST"])
def start_stream():
    app.logger.info("Scanning for devices")
    try:
        found_macs = device_scanner.find_connected_device_macs()
        response_dict = {"device_macs": found_macs}
        resp = jsonify(response_dict)
        resp.status_code = 200
        return resp
    except Exception as e:
        app.logger.error("Error when scanning devices: {0}".format(e))
        return response(404, "Error: {0}".format(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8887, debug=True, threaded=True)
