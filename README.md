# **Video Processing API**

This Flask-based API accepts video uploads and associated JSON metadata for processing. The current implementation processes the video to extract its duration and returns this information along with the input metadata.

**Features**
1. Upload video files with accompanying JSON metadata.
2. Validate video file types (supports mp4, avi, and mov).
3. Extract video duration and return it with the original metadata.
4. Echo back the input JSON data for verification.

**Prerequisites**
Before you can run this API, you need to have Python installed on your system. This project was built using Python 3.8, but it should work with any Python 3.x version. Additionally, you need to install the required Python libraries:

- Flask
- Werkzeug (usually installed with Flask)

**Running the Application**

To start the server, run the following command in the root directory of the project:

```bash
python app.py
```
The Flask server will start running on http://localhost:5000.


## API Endpoints
### Upload Video
POST /upload_video

This endpoint allows users to upload a video file along with JSON metadata. The server processes the video to extract its duration and returns this information along with the echoed metadata.

**Request:**
multipart/form-data containing:
- file: The video file (must be .mp4, .avi, or .mov).
- data: A JSON string containing metadata.

**Response:**
- 200 OK on success:

```json
{
  "status_code": "200",
  "message": "File uploaded and processed successfully",
  "filename": "uploaded_filename.mp4",
  "result": {
    "status": "success",
    "duration": 120
  },
  "input_data": {
    "user_id": "123",
    "location_id": "456",
    "frames": [
      {
        "frame_id": "frame1",
        "url": "url_for_image_frame",
        "meta_data": {
          "timestamp": "timestamp",
          "camera_position": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
          },
          "camera_orientation": {
            "q1": 0.0,
            "q2": 0.0,
            "q3": 0.0,
            "q4": 1.0
          }
        }
      }
    ]
  }
}

```

- 400 Bad Request if there is a problem with the input data.
- 415 Unsupported Media Type if the file type is not allowed.
