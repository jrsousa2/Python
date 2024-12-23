import cv2
import ffmpeg
from realesrgan import RealESRGAN
from PIL import Image
import os

# Load the Real-ESRGAN model
model = RealESRGAN.from_pretrained('RealESRGAN_x4plus')

# Define paths
input_video_path = "D:\\iTunes\\Balao\\Balao.mp4"
output_video_path = "D:\\iTunes\\Balao\\Balao2.mp4"
frames_dir = "D:\\iTunes\\Balao\\temp_frames\\"

# Create directory for frames
os.makedirs(frames_dir, exist_ok=True)

# Step 1: Extract frames from the video
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_rate = cap.get(cv2.CAP_PROP_FPS)
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Save each frame as an image file
    frame_path = os.path.join(frames_dir, f"frame_{count:05d}.png")
    Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(frame_path)
    count += 1
cap.release()

# Step 2: Upscale each frame using Real-ESRGAN
for filename in sorted(os.listdir(frames_dir)):
    frame_path = os.path.join(frames_dir, filename)
    img = Image.open(frame_path)
    
    # Ensure the model is ready and processing the image
    upscaled_img = model.predict(img)
    
    # Save the upscaled frame
    upscaled_img.save(frame_path)  # Overwrite with upscaled frame

# Step 3: Reassemble the frames into a video
ffmpeg.input(os.path.join(frames_dir, 'frame_%05d.png'), framerate=frame_rate).output(output_video_path).run()

# Clean up
for file in os.listdir(frames_dir):
    os.remove(os.path.join(frames_dir, file))
os.rmdir(frames_dir)

print("Upscaling complete! Check:", output_video_path)
