# FRAN is face-reaging (much smaller than diffusers)

import torch
from PIL import Image
import torchvision.transforms as transforms

from facenet_pytorch import MTCNN

import os
import sys
sys.path.insert(0, "C:\\Python\\face_reaging\\model")

from models import UNet

device = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------
# Load model
# ------------------
model = UNet().to(device)

checkpoint = torch.load(
    r"C:\Python\face_reaging\models\best_unet_model.pth",
    map_location=device
)

print("\nLoading weights...will take a while")
model.load_state_dict(checkpoint)
model.eval()

# ------------------
# Load image
# ------------------
print("\nLoading image...")

img = Image.open("D:\\Videos\\Lula\\Lula.jpg").convert("RGB")

mtcnn = MTCNN(
    image_size=512,
    margin=20,
    device=device
)

face = mtcnn(img)

if face is None:
    raise RuntimeError("No face detected")

# MTCNN output → adapt normalization to FRAN training
img_tensor = face.unsqueeze(0).to(device)
img_tensor = (img_tensor + 1.0) / 2.0     # [-1,1] → [0,1]
img_tensor = (img_tensor - 0.5) / 0.5     # → [-1,1] FRAN normalization

# ------------------
# Create age channels
# ------------------
B, _, H, W = img_tensor.shape

# normalized ages expected by FRAN
source_age = 0.65   # older adult (approx Lula photo)
target_age = 0.10   # baby

source_map = torch.full((B, 1, H, W), source_age, device=device)
target_map = torch.full((B, 1, H, W), target_age, device=device)

# concatenate → 5 channels
model_input = torch.cat(
    [img_tensor, source_map, target_map],
    dim=1
)

# ------------------
# Inference
# ------------------
print("\nInference...")

with torch.no_grad():
    output = model(model_input)

# ------------------
# Save result
# ------------------
print("\nSaving result...")

output = (output.squeeze().cpu() * 0.5 + 0.5).clamp(0, 1)

to_pil = transforms.ToPILImage()
result = to_pil(output)

result.save("D:\\Videos\\Lula\\Baby_FRAN.png")

print("\nSaved Baby_FRAN.png")