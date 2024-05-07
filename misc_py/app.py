from flask import Flask, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/videos/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def index():
    # HTML form for uploading a video file
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Upload a video file</title>
    </head>
    <body>
        <h1>Upload a new Video</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    file = request.files.get('file')
    if not file:
        return "No file part", 400
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return redirect(url_for('play_video', filename=filename))
    return "Invalid file type", 400

@app.route('/video/<filename>')
def play_video(filename):
    video_url = url_for('static', filename=f'videos/{filename}')
    # HTML page with video player
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Play Video</title>
    </head>
    <body>
        <h1>Playing Video</h1>
        <video width="640" height="480" controls>
            <source src="{{ video_url }}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </body>
    </html>
    ''', video_url=video_url)

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
