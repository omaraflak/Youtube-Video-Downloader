import os
import uuid
import threading
import youtube_dl
from flask import Flask, request, send_file, send_from_directory

SERVER_PORT = 8080

app = Flask(__name__)

download_threads = {}

class DownloadThread(threading.Thread):
    def __init__(self, video_id):
        self.video_id = video_id
        self.link = 'https://www.youtube.com/watch?v=%s' % video_id
        self.info = {}
        self.uid = str(uuid.uuid4())
        super().__init__()

    def progress_hook(self, info):
        # {
        #     'status': 'downloading',
        #     'downloaded_bytes': 1024,
        #     'total_bytes': 228109154,
        #     'tmpfilename': 'videos/3f2f86fc-7442-47e4-95ad-7e7f1993c338/OU55PWXm2rg.f137.mp4.part',
        #     'filename': 'videos/3f2f86fc-7442-47e4-95ad-7e7f1993c338/OU55PWXm2rg.f137.mp4',
        #     'eta': 4016,
        #     'speed': 56863.63606995803,
        #     'elapsed': 1.0482261180877686,
        #     '_eta_str': '01:06:56',
        #     '_percent_str': '  0.0%',
        #     '_speed_str': '55.53KiB/s',
        #     '_total_bytes_str': '217.54MiB'
        # }
        info['finished'] = info['status'] == 'finished'
        self.info = info
        return self.info

    def run(self):
        folder = 'videos/%s' % self.uid
        ydl_opts = {
            'outtmpl': folder + '/%(id)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'quiet': True
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ydl.download([self.link])

@app.route('/')
def hello_world():
    return '''
        Three routes are available:
        <ul>
            <li><code>/start/?id=video_id</code> will start the download and return a <code>task_id</code></li>
            <li><code>/progress/?id=task_id</code> will return the progress</li>
            <li><code>/file/?id=task_id</code> will download the file</li>
        </ul>
    '''

@app.route('/start/')
def download_video():
    video_id = request.args.get('id')
    thread = DownloadThread(video_id)
    download_threads[thread.uid] = thread
    thread.start()
    return {'task_id': thread.uid}

@app.route('/progress/')
def get_progress():
    thread_id = request.args.get('task_id')
    if thread_id in download_threads:
        thread = download_threads[thread_id]
        return {'status': 'success', **thread.info}
    else:
        return {'status': 'error'}

@app.route('/file/')
def get_file():
    thread_id = request.args.get('task_id')
    if thread_id in download_threads:
        thread = download_threads[thread_id]
        if thread.info['finished']:
            files = os.listdir('videos/%s' % thread_id)
            filename = [name for name in files if name.startswith(thread.video_id)][0]
            filepath = 'videos/%s/%s' % (thread_id, filename)
            return send_file(filepath, as_attachment=True)
        else:
            return {'status': 'error', 'message': 'Download did not finish.'}
    else:
        return {'status': 'error', 'message': 'Could not find file.'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=SERVER_PORT)
