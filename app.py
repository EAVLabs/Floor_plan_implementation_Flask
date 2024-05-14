from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
API_KEYS_FILE = 'api_keys.json'

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

def load_api_keys():
    """Load API keys from the JSON file."""
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as file:
            return json.load(file)
    return {"master_key": "MASTER_SECRET_KEY", "keys": {}}

def save_api_keys(api_keys):
    """Save API keys to the JSON file."""
    with open(API_KEYS_FILE, 'w') as file:
        json.dump(api_keys, file, indent=4)

def get_api_keys():
    """Helper function to get the current API keys."""
    return load_api_keys()

def validate_api_key(key, endpoint):
    """Validate the API key for a specific endpoint."""
    api_keys = get_api_keys()
    if key == api_keys["master_key"]:
        return True
    return key in api_keys["keys"] and endpoint in api_keys["keys"][key]

def api_key_required(endpoint):
    """Decorator to require API key for accessing the endpoint."""
    def decorator(f):
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-KEY')
            if api_key and validate_api_key(api_key, endpoint):
                return f(*args, **kwargs)
            return jsonify({'error': 'Unauthorized access'}), 403
        return wrapper
    return decorator

@app.route('/create_key', methods=['POST'])
def create_key():
    data = request.json
    master_key = data.get('master_key')
    new_key = data.get('new_key')
    endpoints = data.get('endpoints', [])

    if not master_key or not new_key or not endpoints:
        return jsonify({'error': 'Invalid input'}), 400

    api_keys = get_api_keys()
    if master_key != api_keys['master_key']:
        return jsonify({'error': 'Invalid master key'}), 403

    api_keys['keys'][new_key] = endpoints
    save_api_keys(api_keys)

    return jsonify({'message': 'API key created successfully'}), 201

@app.route('/process_data', methods=['POST'])
@api_key_required('process_data')
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
