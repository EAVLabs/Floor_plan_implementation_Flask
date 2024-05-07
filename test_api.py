from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploaded_videos/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Max upload: 50 MB
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_video(file_path):
    """Process the video to extract its duration."""
    try:
        # print(file_path)
        #TODO: Call the Algorithm function to process the video.
        
        clip = VideoFileClip(file_path)
        duration = clip.duration  # Duration in seconds
        clip.close()
        return {"status": "success", "duration": duration}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Process the video after saving
        result = process_video(file_path)
        return jsonify({'message': 'File uploaded and processed successfully', 'filename': filename, 'result': result, 'floorplan':'Algorithm under Development'}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create upload folder if it doesn't exist
    app.run(debug=True, host='0.0.0.0', port=5000)
