# Raspberry Pi Youtube Live Stream with Docker

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
      
## Start Streaming

- `sudo docker-compose up`

## Stop the Stream

- `sudo docker-compose down`

## About

Gábor Vecsei

- [Personal Blog](https://gaborvecsei.wordpress.com/)
- [LinkedIn](https://www.linkedin.com/in/gaborvecsei)
- [Twitter](https://twitter.com/GAwesomeBE)
- [Github](https://github.com/gaborvecsei)
