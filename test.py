from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/model', methods=['POST'])
def model_endpoint():
    # Check if the incoming request contains JSON
    if request.is_json:
        # Parse the JSON into a Python dictionary
        input_data = request.get_json()
        response = process_model(input_data)
        return jsonify(response), 200
    # Check if the incoming request contains files
    elif 'file' in request.files:
        file = request.files['file']
        # Process the file (example assumes the file is an image)
        result = process_file(file)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

def process_model(data):
    # Placeholder function to handle JSON data
    # Replace this with actual model logic
    print("Processing JSON data...")
    return {"status": "Processed", "data": data}

def process_file(file):
    # Placeholder function to handle file input
    # Replace this with actual file processing/model inference logic
    print("Processing file...")
    return {"status": "File processed", "file_name": file.filename}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
