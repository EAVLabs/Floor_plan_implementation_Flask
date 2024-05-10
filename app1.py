from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def is_float(value):
    """Helper function to check if a value can be converted to float."""
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

@app.route('/process_data', methods=['POST'])
def process_data():
    if 'data' not in request.form:
        return jsonify({'error': 'No data provided'}), 400
    
    data = request.form['data']
    try:
        frame_data = json.loads(data)
        valid, message = validate_camera_data(frame_data)
        if not valid:
            return jsonify({'error': 'Invalid data', 'message': message}), 422
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400

    return jsonify({
        'status_code': '200',
        'message': 'Data processed successfully',
        'result': frame_data  # Returning the processed data
    }), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
