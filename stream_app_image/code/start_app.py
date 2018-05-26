import logging
import time
from connected_devices_scanner import ConnectedDevicesScanner
import requests

BASE_STREAM_API_URL = "http://localhost:5000/youtube_stream_api"

# These are the MAC addresses which if present at the network the streaming should stop
STOP_WHEN_PRESENT_MAC_DICT = {"00:11:22:aa:33:bb": "gabor_phone",
                              "99:12:10:aa:33:bb": "mona_phone"}

DEVICE_SCANNER = ConnectedDevicesScanner.from_arp_scan()
WAIT_TIME_BETWEEN_SCANS_IN_MINUTES = 0.5
IS_STREAM_RUNNING = False

logger = logging.getLogger('stream_app')
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('stream_app.log')
file_handler.setFormatter(logger_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logger_formatter)
logger.addHandler(console_handler)


def get_present_devices():
    """
    Checks if whitelist devices are present or not
    :return: True if there are device, False if the are not
    """
    found_macs = DEVICE_SCANNER.find_connected_device_macs()

    whitelist_macs = list(STOP_WHEN_PRESENT_MAC_DICT.keys())
    whitelist_macs = [x.lower() for x in whitelist_macs]

    present_device_macs = set(found_macs).intersection(set(whitelist_macs))
    present_device_macs_dict = {x: STOP_WHEN_PRESENT_MAC_DICT[x] for x in present_device_macs}

    if len(present_device_macs) > 0:
        return present_device_macs_dict
    return None


def start_streaming():
    global IS_STREAM_RUNNING
    if IS_STREAM_RUNNING:
        raise Exception("Can't start streaming because it's already doing it")

    url = BASE_STREAM_API_URL + "/start"
    response = requests.get(url)

    response_json = response.json()

    if response.status_code == requests.codes.ok:

        IS_STREAM_RUNNING = True
    else:
        raise Exception("There was an error when tried to start streaming via Stream API")

    return response_json


def stop_streaming():
    global IS_STREAM_RUNNING
    if not IS_STREAM_RUNNING:
        raise Exception("Can't stop streaming because it's currently not streaming")

    url = BASE_STREAM_API_URL + "/stop"
    response = requests.get(url)

    response_json = response.json()

    if response.status_code == requests.codes.ok:
        IS_STREAM_RUNNING = False
    else:
        raise Exception("There was an error when tried to stop streaming via Stream API")

    return response_json


def main():
    while True:
        present_devices_dict = get_present_devices()

        if present_devices_dict is not None:
            logger.info("Present devices: {0}".format(present_devices_dict))
            try:
                r = stop_streaming()
                logger.info("Successfully stopped streaming with Stream API")
                logger.info("Response from Stream API: {0}".format(r))
            except Exception as e:
                logger.error("Error: {0}".format(e))
        else:
            logger.info("There are no whitelisted devices, so streaming can start")
            try:
                r = start_streaming()
                logger.info("Successfully started streaming with Stream API")
                logger.info("Response from Stream API: {0}".format(r))
            except Exception as e:
                logger.error("Error: {0}".format(e))

        logger.info("*" * 30)
        time.sleep(int(WAIT_TIME_BETWEEN_SCANS_IN_MINUTES * 60))


if __name__ == "__main__":
    main()
