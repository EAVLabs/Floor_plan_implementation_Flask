import cv2
import torch
import torchvision.transforms as transforms
import numpy as np

# Load MiDaS model
# model_type = "DPT_Large"  # DPT_Large model for better accuracy.
# midas = torch.hub.load("intel-isl/MiDaS", model_type)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# midas.to(device)
# midas.eval()

# # Prepare the transforms
# midas_transforms = transforms.Compose([
#     transforms.ToTensor(),
#     transforms.Resize(384),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# def process_frame(frame):
#     # Convert the BGR image to RGB
#     img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     # Apply transformations
#     input_tensor = midas_transforms(img_rgb).unsqueeze(0).to(device)
    
#     # Prediction
#     with torch.no_grad():
#         depth = midas(input_tensor)
#         depth = torch.nn.functional.interpolate(
#             depth.unsqueeze(1),
#             size=img_rgb.shape[:2],
#             mode="bilinear",
#             align_corners=False,
#         ).squeeze()

#     # Normalize the depth for visualization
#     depth_normalized = cv2.normalize(depth.cpu().numpy(), None, 0, 255, cv2.NORM_MINMAX)
#     depth_normalized = depth_normalized.astype(np.uint8)
#     depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_MAGMA)
#     return depth_colormap

# Process video
cap = cv2.VideoCapture('vid2_floorplan.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # depth_map = process_frame(frame)
    cv2.imshow('Depth Map', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
