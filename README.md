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

### 2. Install the Chrome Extension

```
zip youtube-downloader.zip -r youtube-dl-extension
```

1. Open Chrome at the following address: `chrome://extensions/`
2. Toggle `Developer mode` on the top-right corner
3. Click `Load unpacked` then select the zip file `youtube-downloader.zip`

### 3. Browse a Youtube video and enjoy the Download button.

[!image](art/screenshot.png)
