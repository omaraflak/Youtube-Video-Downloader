import os
import uuid
import youtube_dl
from flask import Flask, request, send_from_directory

SERVER_PORT = 8080

api = Flask(__name__)

@api.route('/')
def hello_world():
    return '''
        In order to download a video, make a request to <code>/download/?id=video_id</code></br></br>
        For instance, if the video link is: <code>https://www.youtube.com/watch?v=BaW_jenozKc</code></br>
        Then the link to download the video is: <code>/download/?id=BaW_jenozKc</code>
    '''

@api.route('/download/', methods=['GET'])
def download_video():
    video_id = request.args.get('id')
    link = 'https://www.youtube.com/watch?v=%s' % video_id
    uid = str(uuid.uuid4())
    folder = 'videos/%s' % uid
    ydl_opts = { 'outtmpl': folder + '/%(id)s.%(ext)s' }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([link])

    files = os.listdir(folder)
    filename = [name for name in files if name.startswith(video_id)][0]

    return send_from_directory(folder, filename, as_attachment=True)

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=SERVER_PORT)
