import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from os import getenv
from sys import exit

# Verify the TORCH_HOME environment variable
HF_home = getenv('HF_HOME')
print(f"\nHF_HOME is set to {HF_home}\n")

# Load pipeline with CPU initially
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,  # float16 for GPU
    cache_dir=HF_home,
)

# Enable automatic CPU offload
pipe.enable_model_cpu_offload()
# pipe.set_max_memory({ "cuda": "2GB", "cpu": "8GB" })

# Try moving main UNet to GPU
# try:
#     # UNet on GPU (float16)
#     pipe.unet.to("cuda", dtype=torch.float16)
#     # pipe.unet.to("cuda")
#     # Offload large modules to CPU to avoid VRAM overflow
#     pipe.vae.to("cpu")
#     # THE BELOW DON'T EXIST! REMOVED
#     # pipe.text_encoder.to("cpu")
#     # pipe.prompt_encoder.to("cpu")
#     device = "cuda"
# except RuntimeError as e:
#     print("GPU memory insufficient, falling back to CPU.")
#     device = "cpu"
#     exit()

# print("\nPipeline ready. Main UNet device:", next(pipe.unet.parameters()).device)
# print("VAE device:", next(pipe.vae.parameters()).device)
# print("Text encoder device:", next(pipe.text_encoder.parameters()).device)

# Load and resize image to 320x180 (LD)
image = load_image("D:\\Videos\\Animation\\image.png").resize((160, 90))

# Generate short video (3 sec × 7 fps = 21 frames)
frames = pipe(image, num_frames=21).frames[0]

# Export video
export_to_video(frames, "D:\\Videos\\Animation\\video_short_gpu.mp4", fps=7)
print("Video created successfully!")