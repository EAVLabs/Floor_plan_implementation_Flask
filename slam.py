import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_frames(video_path):
    """ Extract frames from a video file """
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def detect_features(frames):
    """ Apply feature detection on each frame """
    orb = cv2.ORB_create()
    feature_frames = []
    for frame in frames:
        keypoints, descriptors = orb.detectAndCompute(frame, None)
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color=(0, 255, 0), flags=0)
        feature_frames.append(frame_with_keypoints)
    return feature_frames

def plot_frames(frames):
    """ Plot the frames with detected features """
    plt.figure(figsize=(10, 8))
    for i, frame in enumerate(frames[:5]):  # show first 5 frames
        plt.subplot(2, 3, i + 1)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.title(f"Frame {i}")
        plt.axis('on')
    plt.show()

# Use the functions
video_path = 'vid2_floorplan.mp4'
frames = extract_frames(video_path)
feature_frames = detect_features(frames)
plot_frames(feature_frames)
