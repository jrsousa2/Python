# FRAN is face-reaging (much smaller than diffusers)

# Age values (most important)
# FRAN expects normalized ages:

# Meaning	Value
# baby	    0.05–0.15
# child	    0.2
# teen	    0.35
# adult	    0.5
# elderly	0.8–1.0

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "models", "best_unet_model.pth")

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

mtcnn = MTCNN(image_size=512, margin=20)

face = mtcnn(img)

face = transforms.ToPILImage()(face)

# transform = transforms.Compose([
#     transforms.Resize((512, 512)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5]*3, [0.5]*3)
# ])

transform = transforms.Compose([
    transforms.Resize((512,512)),
    transforms.ToTensor()
])

# AQUI ERA img -> face 
img_tensor = transform(face).unsqueeze(0).to(device)

# ------------------
# Create age channels
# ------------------
B, _, H, W = img_tensor.shape

# OUTDATED AGES
# source_age = 0.70   # older adult
# target_age = 0.10   # baby

# UPDATED AGES
source_age = 0.4
target_age = -0.8

source_map = torch.full((B,1,H,W), source_age, device=device)
target_map = torch.full((B,1,H,W), target_age, device=device)

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

output = (output.squeeze().cpu()*0.5 + 0.5).clamp(0,1)

to_pil = transforms.ToPILImage()
result = to_pil(output)

result.save("D:\\Videos\\Lula\\Baby_FRAN.png")

print("\nSaved baby_lula.png")
