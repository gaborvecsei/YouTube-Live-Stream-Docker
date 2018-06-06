import requests
import logging
import time
import pandas as pd

BASE_STREAM_API_URL = "http://localhost:8888/youtube_stream_api"
BASE_DEVICE_SCANNER_API_URL = "http://localhost:8887/device_scan_api"

WHITELISTED_DEVICES_CSV_PATH = "whitelisted_devices.csv"

WAIT_TIME_BETWEEN_SCANS_IN_MINUTES = 5

logger = logging.getLogger('master_app')
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('master_app.log')
file_handler.setFormatter(logger_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logger_formatter)
logger.addHandler(console_handler)


def get_whitelisted_devices_dict():
    df = pd.read_csv(WHITELISTED_DEVICES_CSV_PATH, header=0)
    device_names = df["name"].values
    device_macs = [x.lower() for x in df["mac"].values]
    return {m: n for m, n in zip(device_macs, device_names)}


def scan_for_whitelisted_devices():
    url = BASE_DEVICE_SCANNER_API_URL + "/scan"
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        raise Exception("Scanning not worked")

    response_json = response.json()

    # The file can be update at any time so we need to perform this at every scanning
    whitelist_device_dict = get_whitelisted_devices_dict()
    whitelist_device_MACs = list(whitelist_device_dict.keys())

    found_device_MACs = list(response_json["device_macs"])
    present_whitelist_device_MACs = set(found_device_MACs).intersection(set(whitelist_device_MACs))

    if len(present_whitelist_device_MACs) <= 0:
        # There are no whitelisted devices
        return None

    present_device_macs_dict = {x: whitelist_device_dict[x] for x in present_whitelist_device_MACs}
    return present_device_macs_dict


def check_if_stream_is_alive():
    url = BASE_STREAM_API_URL + "/alive"
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        raise Exception("Could not check if stream is alive")

    response_json = response.json()
    is_alive = response_json["alive"]

    return is_alive


def check_and_fix_stream_health():
    url = BASE_STREAM_API_URL + "/check_health"
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        raise Exception("Could not check stream health")

    response_json = response.json()

    return response_json


def start_streaming():
    url = BASE_STREAM_API_URL + "/start"
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        raise Exception("There was an error when tried to START streaming via Stream API")

    return response.json()


def stop_streaming():
    url = BASE_STREAM_API_URL + "/stop"
    response = requests.get(url)

    if response.status_code != requests.codes.ok:
        raise Exception("There was an error when tried to STOP streaming via Stream API")

    return response.json()


def main():
    # Streaming will start if this many scans there were no whitelisted devices
    no_whitelisted_devices_scan_tolerance = 2

    # This variable is increased when there are no whitelisted devices found
    no_whitelisted_devices_scan_number = 0

    while True:
        present_whitelisted_devices = scan_for_whitelisted_devices()

        check_and_fix_stream_health()
        is_stream_alive = check_if_stream_is_alive()
        logger.info("Stream is alive: {0}".format(is_stream_alive))

        if present_whitelisted_devices is not None:
            logger.info("Present whitelisted devices: {0}".format(present_whitelisted_devices))

            if is_stream_alive:
                try:
                    r = stop_streaming()
                    logger.info("Successfully stopped streaming with Stream API")
                    logger.info("Response from Stream API: {0}".format(r))
                except Exception as e:
                    logger.error("Error: {0}".format(e))
            else:
                logger.info("Streaming is stopped already")
        else:
            logger.info("There are no whitelisted devices")

            no_whitelisted_devices_scan_number += 1
            logger.info("Current scans without whitelisted device: {0}".format(no_whitelisted_devices_scan_number))

            if no_whitelisted_devices_scan_number >= no_whitelisted_devices_scan_tolerance:
                logger.info("Scan number without whitelisted devices reached the tolerance. Streaming starts.")

                # reset the counter
                no_whitelisted_devices_scan_number = 0

                if not is_stream_alive:
                    try:
                        r = start_streaming()
                        logger.info("Successfully started streaming with Stream API")
                        logger.info("Response from Stream API: {0}".format(r))
                    except Exception as e:
                        logger.error("Error: {0}".format(e))
                else:
                    logger.info("Already streaming")

        logger.info("Now waiting for {0} minutes".format(WAIT_TIME_BETWEEN_SCANS_IN_MINUTES))
        time.sleep(int(WAIT_TIME_BETWEEN_SCANS_IN_MINUTES * 60))


if __name__ == "__main__":
    main()
