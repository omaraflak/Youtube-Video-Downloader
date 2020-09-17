# Youtube Video Downloader

### Dependencies

You only Docker installed on your machine.

### 1. Start server in Docker container

This will start a local Python server exposing `youtube-dl` api through `Flask`.

```sh
cd youtube-dl-server
make
make run
```

### Run cron task at boot (optional)

```
crontab -e
```

Append at the end: `@reboot make run -f /path/to/Youtube-Video-Downloader/youtube-dl-server/Makefile`

### 2. Install the Chrome Extension

1. Open Chrome at the following address: `chrome://extensions`
2. Toggle `Developer mode` in the top-right corner
3. Click `Load unpacked` then select the folder `youtube-dl-extension`

### 3. Browse a Youtube video and enjoy the Download button.

![image](art/screenshot.png)
