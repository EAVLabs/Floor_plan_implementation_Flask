from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploaded_videos/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Max upload: 50 MB
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        try:
            processed_file_path = convert_to_grayscale(file_path)
            return jsonify({'message': 'File uploaded and processed successfully', 'processed_file_path': processed_file_path}), 201
        except Exception as e:
            return jsonify({'error': 'Failed to process video', 'message': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

def convert_to_grayscale(input_path):
    # Define the output file path
    output_path = input_path.rsplit('.', 1)[0] + '_grayscale.avi'
    # Open the video file
    cap = cv2.VideoCapture(input_path)
    # Define the codec and create VideoWriter object to save the file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))), isColor=False)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Write the frame into the file
        out.write(gray)
    
    # Release everything if job is finished
    cap.release()
    out.release()
    return output_path

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure upload folder exists
    app.run(debug=True, host='0.0.0.0', port=5000)
