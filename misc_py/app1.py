from flask import Flask, render_template_string, Response, request
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_to_grayscale(frame):
    """ Convert the frame to grayscale to create a black and white video effect. """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def frame_generator(video_path):
    """
    Generates frames from the video and yields each frame in JPEG format.
    Yields both original and grayscale frames for two different streams.
    """
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Process the frame to black and white
        gray_frame = convert_to_grayscale(frame)
        # Encode original frame as JPEG
        _, orig_buffer = cv2.imencode('.jpg', frame)
        # Encode grayscale frame as JPEG
        _, gray_buffer = cv2.imencode('.jpg', gray_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + orig_buffer.tobytes() + b'\r\n'
               b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + gray_buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template_string('''
    <!doctype html>
    <title>Upload Video</title>
    <h1>Upload video for live processing</h1>
    <form method=post enctype=multipart/form-data action="/upload">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return render_template_string('''
        <!doctype html>
        <title>Video Streams</title>
        <h1>Original and Grayscale Video Streams</h1>
        <img src="/video_feed/original/{{ filename }}" style="float:left; width:45%; margin-right:5%;">
        <img src="/video_feed/grayscale/{{ filename }}" style="float:left; width:45%;">
        ''', filename=filename)
    return "Invalid file type", 400

@app.route('/video_feed/<mode>/<filename>')
def video_feed(mode, filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return Response(frame_generator(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)