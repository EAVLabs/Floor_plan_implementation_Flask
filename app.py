from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
import json

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploaded_videos/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Max upload: 50 MB
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    """ Check if the file extension is allowed. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_video(file_path, frame_data):
    """Process the video to extract its duration and potentially other metadata."""
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration  # Duration in seconds
        clip.close()
        # Additional processing logic can be based on frame_data
        return {"status": "success", "duration": duration}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/upload_video', methods=['POST'])
def upload_video():
    """ Endpoint to upload a video and process it along with JSON data. """
    if 'file' not in request.files or 'data' not in request.form:
        return jsonify({'error': 'Missing file or data'}), 400
    
    file = request.files['file']
    data = request.form['data']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        frame_data = json.loads(data)
        # print(frame_data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the video after saving, along with frame data
        result = process_video(file_path, frame_data)
        return jsonify({
            'status_code': '200',
            'message': 'File uploaded and processed successfully',
            'filename': filename,
            'result': result,
            # 'input_data': frame_data  # Echoing back the input data for verification
        }), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
