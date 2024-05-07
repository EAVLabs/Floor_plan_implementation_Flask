import torch
import cv2
import torchvision.transforms as T
from PIL import Image
import numpy as np

# Check if CUDA is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the MiDaS v3 model
model = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
model.to(device)
model.eval()

# Transformer for input image
transform = T.Compose([
    T.ToTensor(),
    T.Resize(384),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def prepare_image(img):
    """Prepare an image for depth estimation."""
    img = transform(img).unsqueeze(0).to(device)
    return img

def predict_depth(image):
    """Predict the depth map of the input image using MiDaS."""
    with torch.no_grad():
        prediction = model(image)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=image.shape[2:],
            mode="bilinear",
            align_corners=False,
        ).squeeze()
    return prediction

# Open a video file
cap = cv2.VideoCapture('vid2_floorplan.mp4')
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if there are no frames to read

    # Convert the frame to RGB and PIL format for processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(frame_rgb)

    # Prepare the image and predict the depth
    input_tensor = prepare_image(pil_img)
    depth = predict_depth(input_tensor)

    # Normalize the depth map for display
    depth_normalized = cv2.normalize(depth.cpu().numpy(), None, 0, 255, cv2.NORM_MINMAX)
    depth_colormap = cv2.applyColorMap(depth_normalized.astype(np.uint8), cv2.COLORMAP_MAGMA)

    # Show the depth map
    cv2.imshow('Depth Map', depth_colormap)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
