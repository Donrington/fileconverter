import os
from flask import *
from amanigo import *
from flask_wtf.csrf import CSRFProtect, generate_csrf
from PIL import Image
import io
from moviepy.editor import VideoFileClip


@app.route('/')
def index():
    # Manually generate CSRF token and pass to template
    csrf_token = generate_csrf()
    return render_template('index.html', csrf_token=csrf_token)

@app.route('/convert-to-webp', methods=['POST'])
def convert_to_webp():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    try:
        image = Image.open(file.stream)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='WEBP', quality=50)
        img_byte_arr.seek(0)
        return send_file(
            img_byte_arr,
            mimetype='image/webp',
            as_attachment=True,
            download_name='converted_image.webp'
        )
    except Exception as e:
        return str(e), 500


@app.route('/convert-to-webm', methods=['POST'])
def convert_to_webm():
    if 'video' not in request.files:
        return "No video part in the request", 400

    video_file = request.files['video']
    if video_file.filename == '':
        return "No selected video", 400

    temp_video_path = "temp_video.webm"  # Temporary file with .webm extension

    # Save the uploaded video to a temporary file
    video_file.save(temp_video_path)

    try:
        # Process the video file to convert it to WebM format
        video_clip = VideoFileClip(temp_video_path)
        video_clip.write_videofile(temp_video_path, codec='libvpx', fps=video_clip.fps, preset='good' ,bitrate="5000k", threads='4')  # Output directly to a .webm file
        video_clip.close()

        # Read the converted file back into a BytesIO stream for transmission
        with open(temp_video_path, 'rb') as f:
            video_byte_arr = io.BytesIO(f.read())
        
        return send_file(
            video_byte_arr,
            mimetype='video/webm',
            as_attachment=True,
            download_name='converted_video.webm'
        )
    except Exception as e:
        return str(e), 500
    finally:
        video_clip.close()
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)