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
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_video(file_path, frame_data):
    """Process the video to extract its duration and potentially other metadata."""
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration  # Duration in seconds
        clip.close()
        return {"status": "success", "duration": duration}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_camera_data(frame_data):
    """Validate camera position and orientation to ensure all are float values."""
    for frame in frame_data.get('frames', []):
        camera_position = frame['meta_data'].get('camera_position', {})
        camera_orientation = frame['meta_data'].get('camera_orientation', {})
        
        # Check all required camera position and orientation fields
        for key in ['x', 'y', 'z']:
            if not is_float(camera_position.get(key)):
                return False, f"Camera position {key} is not a float"
        
        for key in ['q1', 'q2', 'q3', 'q4']:
            if not is_float(camera_orientation.get(key)):
                return False, f"Camera orientation {key} is not a float"
    
    return True, "Validation successful"

@app.route('/upload_video', methods=['POST'])
def upload_video():
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
        valid, message = validate_camera_data(frame_data)
        if not valid:
            return jsonify({'error': 'Invalid data', 'message': message}), 422
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
            'input_data': frame_data  # Returning the input data
        }), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
