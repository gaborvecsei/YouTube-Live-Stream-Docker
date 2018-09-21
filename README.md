# Youtube Live Stream with Docker

![logo](art/live_stream_youtube_docker_logo.png)

With this dockerized app, you can use a webcam to stream live video to YouTube

- [Simple Mode](#simple-mode)
    - [Setup Simple Mode](#setup-simple-mode)
- [Advanced Mode](#advanced-mode)
    - [Setup Advanved Mode](#setup-advanced-mode)

----------------------------------

*It was developer for Raspberry Pi, but of course it works with any type of HW as long as it supports Docker.*

## Base Setup

### Install Docker & Clone Repo:

1. Install `Docker` 🐳
    - `curl -sSL https://get.docker.com | sh`
2. Install `docker-compose`
    - `sudo pip install docker-compose` OR `sudo pip3 install docker-compose`
3. Clone this repo
    - `git clone https://github.com/gaborvecsei/YouTube-Live-Stream-Docker.git`
    - go inside the folder `cd Youtube-Live-Stream-Docker`

## Simple Mode

With this "mode", the streaming starts when your device boots up and shuts down only when you turn off your device or
stop the docker container. It can be useful when you have a dedicated device, only for this purpose what your only want
to turn on and off without using ssh and entering commands to the terminal. This method handles these automatically.

I use this mode, so I can have a "secret eye" :eyes: on my puppy, when I leave :heart:.

### Setup Simple Mode

1. `cd base_docker_image` then `sudo ./build_base.sh` to build the base image for the other Docker images
2. Edit `docker-compose.yml`
    - Change `YOUTUBE_LIVE_KEY` to your personal youtube live stream key which you can find at `https://www.youtube.com/live_dashboard`
    - Under `devices` change the host mapping if necessary. (By default it uses the `video0`).
        - For example if you'd like to use `video1` device than change it to: `/dev/video1:/dev/video0`

### Start Simple Mode :ok_hand:

- Go to the `youtube_stream_image` folder and then run command:
    - `sudo docker-compose up -d`

### Stop Simple Mode :x:

- Go to the `youtube_stream_image` folder and then run command:
    - `sudo docker-compose down`

----------------------------------

## Advanced Mode

As I always forgot to turn on/off the stream, now it does it automatically based on the connected
devices on your network :sparkles:.

This is achieved with a *MAC whitelist*. If a MAC address is in the list, that means
if it's present at your network, the stream will shut down automatically (so you don't have to worry about being
streamed, even if it's private). If it's not present then the stream goes live.

```
                +---------------------------+
                |                           +
                |                yes+---->stop
                |                ^        stream
                |                |
                v                +
start +-----> scan devices +---> is whitelisted MAC
                ^                present?
                |                +
                |                |
                |                v
                |                no+----->start
                |                         stream
                |                           +
                +---------------------------+
```

### Setup Advanced Mode

1. Perform the same as in [Setup Simple Mode](#setup-simple-mode)
2. Whitelist device MAC addresses
    - Edit `master_app_image/code/whitelisted_devices.csv`
      - This file is responsible for keeping safe MAC addresses, so when this device is present based on `arp-scan` or `nmap` we know, we can shut down the stream
3. YouTube Private Settings
    - Don't forget to set yout live stream to `private` at [YouTube Live Dashboard](https://www.youtube.com/live_dashboard)

### Start Advanced Mode :ok_hand:

- `sudo docker-compose up -d`

(For logs you can use `sudo docker-compose logs` or inside the `code` folders you can find the log files)

### Stop Advanced Mode :x:

- `sudo docker-compose down`

### Services (Containers)

- **Device Scanner** :computer:
    - Responsible to scan the devices in the local network (*localhost*)
    - Rest Api:
        ```
        GET, POST - localhost:8887/device_scan_api/scan
        result: {"device_macs": ["00:11:22:33:44:55", ...}
        ```
- **YouTube Stream** :camera:
    - With this we can start or stop a live stream
    - Rest Api:
        ```
        GET, POST - localhost:8888/youtube_stream_api/start
        GET, POST - localhost:8888/youtube_stream_api/stop
        GET, POST - localhost:8888/youtube_stream_api/check_health
        GET, POST - localhost:8888/youtube_stream_api/alive
        ```
- **Master App** :crown:
    - This is the main container which uses the above services to detect whitelisted devices and decide to start or
    stop the live streaming

----------------------------------

## todo

- [x] device scanning for automatic streamin
- [x] master - feature architecture
- [x] create base Dockerfile
- [ ] logging to DB when was the stream live, which device, etc...
- [x] easily switch to "basic mode". When there is no device scan, it streams when I start it.
- [x] easily editable `csv` for whitelisting
- [ ] comments
- [ ] send (Slack, Gmail, etc...) message when stream started/stopped

----------------------------------

## About

Gábor Vecsei

- [Website](https://gaborvecsei.com)
- [LinkedIn](https://www.linkedin.com/in/gaborvecsei)
- [Twitter](https://twitter.com/GAwesomeBE)
- [Github](https://github.com/gaborvecsei)
- [Personal Blog](https://gaborvecsei.wordpress.com/)
