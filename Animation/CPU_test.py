import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
import os

# Verify the TORCH_HOME environment variable
HF_home = os.getenv('HF_HOME')

print(f"\nHF_HOME is set to {HF_home}\n")

pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float32, cache_dir=HF_home
) #.to("cuda")

# Check which device the model is on
#print("\nWhere model is stored:", next(pipe.model.parameters()).device)
print("Pipeline main model device:", next(pipe.unet.parameters()).device)

# image = load_image("D:\\Videos\\Animation\\image.png").resize((1024,576))
image = load_image("D:\\Videos\\Animation\\image.png").resize((160,90))

frames = pipe(image, num_frames=21).frames[0]

export_to_video(frames, "D:\\Videos\\Animation\\video.mp4", fps=7)
print("Video created successfully!")