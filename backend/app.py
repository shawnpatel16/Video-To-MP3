from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
import re
app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/convert', methods=['POST'])
def convert_video():
    video_url = ''
    data = request.get_json()
    video_url = data['youtubeLink']
    timestamps = data['timestamps']
    timestamps_in_seconds = []
    for timestamp in timestamps:
        timestamps_in_seconds.append(convert_to_seconds(timestamp['start'], timestamp['end']))
    file_path,video_title = download_video(video_url)
    audio_path, video_title = edit_video(file_path,timestamps_in_seconds,video_title)
    return send_file(audio_path,mimetype='audio/mpeg',as_attachment=True, download_name=f"{video_title}")

def download_video(url):
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    file_path = video.download('./sample_videos')
    print("great success")
    return file_path, youtube.title

def convert_to_seconds(start,end):
    start_minutes, start_seconds = map(int, start.split(":"))
    total_start_seconds = start_minutes * 60 + start_seconds
    end_minutes, end_seconds = map(int, end.split(":"))
    total_end_seconds = end_minutes * 60 + end_seconds
    return [total_start_seconds,total_end_seconds]

def edit_video(video_path, timestamps, video_title):
    video_title = re.sub(r'[\/:*?"<>|]', '', video_title)
    clip = VideoFileClip(video_path)

    subclips = []

    for timestamp in timestamps:
        start_time = timestamp[0]
        end_time = timestamp[1]

        subclip = clip.subclip(start_time, end_time)
        subclips.append(subclip)

    final_clip = concatenate_videoclips(subclips)
    final_audio_clip = final_clip.audio
    final_audio_clip.fps = 44100
    audio_path = f"./sample_videos/{video_title}.mp3"
    final_audio_clip.write_audiofile(audio_path)
    return audio_path, video_title
    print("another great success")

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
