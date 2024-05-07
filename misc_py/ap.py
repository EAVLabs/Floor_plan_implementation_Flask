import os
from flask import Flask, render_template, request, Response
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the uploaded video file
        video_file = request.files['video']
        
        # Save the video file to disk
        video_path = os.path.join('static', video_file.filename)
        video_file.save(video_path)
        
        # Process the video and get the processed frames
        processed_frames = process_video(video_path)
        
        # Render the template with the processed frames
        return render_template('index.html', video_path=video_file.filename, processed_frames=processed_frames)
    
    return render_template('index.html')

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    processed_frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Encode the grayscale frame as JPEG
        _, encoded_frame = cv2.imencode('.jpg', gray_frame)
        processed_frames.append(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')
    
    cap.release()
    return b''.join(processed_frames)

@app.route('/processed_video')
def processed_video():
    video_path = os.path.join('static', request.args.get('video_path'))
    processed_frames = process_video(video_path)
    return Response(processed_frames, mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)