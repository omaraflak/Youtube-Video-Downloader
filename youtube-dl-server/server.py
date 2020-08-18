import os
import uuid
import threading
import youtube_dl
from flask import Flask, jsonify, request, send_file, render_template

app = Flask(__name__)

SERVER_PORT = 8080
DOWNLOAD_FOLDER = 'videos'
download_threads = {}

class DownloadThread(threading.Thread):
    def __init__(self, video_id, format_id):
        self.video_id = video_id
        self.format_id = format_id
        self.link = get_video_link(video_id)
        self.info = self.get_info({})
        self.uid = str(uuid.uuid4())
        super().__init__()

    def get_info(self, info):
        return {
            'finished': info.get('status', '') == 'finished',
            'downloaded_bytes': info.get('downloaded_bytes', 0),
            'total_bytes': info.get('total_bytes', 1),
            'speed_str': info.get('_speed_str', ''),
            'filesize_str': info.get('_total_bytes_str', '')
        }

    def progress_hook(self, info):
        self.info = self.get_info(info)
        return self.info

    def run(self):
        folder = '%s/%s' % (DOWNLOAD_FOLDER, self.uid)
        ydl_opts = {
            'outtmpl': folder + '/%(id)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'format': self.format_id,
            'quiet': True
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.download([self.link])

def get_video_link(video_id):
    return 'https://www.youtube.com/watch?v=%s' % video_id

@app.route('/')
def hello_world():
    return '''
        Three routes are available:
        <ul>
            <li><code>/info/?id=video_id</code> will fetch available formats</li>
            <li><code>/start/?id=video_id</code> will start the download and return a <code>task_id</code></li>
            <li><code>/progress/?id=task_id</code> will return the progress</li>
            <li><code>/file/?id=task_id</code> will download the file</li>
        </ul>
    '''

@app.route('/info/')
def get_info():
    video_id = request.args.get('id')
    link = get_video_link(video_id)
    ydl = youtube_dl.YoutubeDL({})
    meta = ydl.extract_info(link, download=False)
    formats = meta.get('formats', [meta])
    output = [
        {
            'id': format['format_id'],
            'ext': format['ext'],
            'format': format['format']
        }
        for format in formats
    ]
    return jsonify(output)

@app.route('/start/')
def download_video():
    video_id = request.args.get('id')
    format_id = request.args.get('format')
    thread = DownloadThread(video_id, format_id)
    download_threads[thread.uid] = thread
    thread.start()
    return {'task_id': thread.uid}

@app.route('/progress/')
def get_progress():
    task_id = request.args.get('task_id')
    if task_id in download_threads:
        thread = download_threads[task_id]
        return {'status': 'success', **thread.info}
    else:
        return {'status': 'error', 'message': 'Could not find file.'}

@app.route('/file/')
def get_file():
    task_id = request.args.get('task_id')
    if task_id in download_threads:
        thread = download_threads[task_id]
        if thread.info['finished']:
            files = os.listdir('%s/%s' % (DOWNLOAD_FOLDER, task_id))
            filename = [name for name in files if name.startswith(thread.video_id)][0]
            filepath = '%s/%s/%s' % (DOWNLOAD_FOLDER, task_id, filename)
            return send_file(filepath, as_attachment=True)
        else:
            return {'status': 'error', 'message': 'Download did not finish.'}
    else:
        return {'status': 'error', 'message': 'Could not find file.'}

@app.route('/view/')
def download_page():
    task_id = request.args.get('task_id')
    return render_template('index.html', task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=SERVER_PORT)
