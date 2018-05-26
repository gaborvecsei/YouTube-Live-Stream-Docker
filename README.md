# Raspberry Pi Youtube Live Stream with Docker

With this dockerized app, you can use a webcam to stream live video to YouTube.

As I always forgot to turn on/turn off the stream, now it does it automatically based on the "present"
devices on your network. This is achieved with a MAC whitelist. If a MAC address is in the list, that means
if it's present at your network, the stream will shut down automatically. If it's not present then the stream goes live.

```
                +---------------------------+
                |                           +
                |                yes+---->stop
                |                ^        stream
                |                |
                +                +
start +-----> scan devices +---> is whitelisted MAC
                +                present?
                |                +
                |                |
                |                v
                |                no+----->start
                |                         stream
                |                           +
                +---------------------------+
```

## Setup

1. Install `Docker` 🐳
    - `curl -sSL https://get.docker.com | sh`
2. Install `docker-compose`
    - `sudo pip install docker-compose` OR `sudo pip3 install docker-compose`
3. Clone this repo
    - `git clone https://github.com/gaborvecsei/RaspberryPi-Youtube-Live-Stream.git`
    - go inside the folder `cd RaspberryPi-Youtube-Live-Stream`
4. Edit `docker-compose.yml`
    - Change `YOUTUBE_LIVE_KEY` to your personal youtube live stream key which you can find at `https://www.youtube.com/live_dashboard`
    - Under `devices` change the host mapping if necessary. (By default it uses the `video0`).
      - For example if you'd like to use `video1` device than change it to: `/dev/video1:/dev/video0`
5. Whitelist device MAC addresses
    - Inside `stream_app_image/code/start_app.py` edit the variable: `STOP_WHEN_PRESENT_MAC_DICT`
    - This dict is responsible for keeping safe mac addresses, so when this device is present based on
    `arp-scan` or `nmap` we know, we can shut down the stream
6. Private
    - Don't forget to set yout live stream to `private` at [YouTube Live Dashboard](https://www.youtube.com/live_dashboard)

## Start

- `sudo docker-compose up`

## Stop

- `sudo docker-compose down`

## About

Gábor Vecsei

- [LinkedIn](https://www.linkedin.com/in/gaborvecsei)
- [Twitter](https://twitter.com/GAwesomeBE)
- [Github](https://github.com/gaborvecsei)
- [Personal Blog](https://gaborvecsei.wordpress.com/)
