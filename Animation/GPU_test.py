import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from os import getenv

from timeit import default_timer
from datetime import datetime
#from sys import exit

elapsed_time = 0
start_time = default_timer()

start_time_act = datetime.now()
print("\nStart time:", start_time_act)

# Verify the TORCH_HOME environment variable
HF_home = getenv('HF_HOME')
print(f"\nHF_HOME is set to {HF_home}\n")

# Load pipeline with CPU initially
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float32,  # float16 for GPU
    cache_dir=HF_home,
) #.to("cuda")

# Progress bar
pipe.set_progress_bar_config(disable=False)
#pipe.set_max_memory({ "cuda": "2GB", "cpu": "9.5GB" })
# Enable automatic CPU offload
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
# pipe.set_max_memory({ "cuda": "2GB", "cpu": "8GB" })

# Load and resize image to 320x180 (LD)
image = load_image("D:\\Videos\\Animation\\image.png").resize((160, 90))

# Generate short video (3 sec × 3 fps = 9 frames)
frames = pipe(image, num_frames=14).frames[0]

# Export video
export_to_video(frames, "D:\\Videos\\Animation\\video_short_gpu.mp4", fps=3)
print("Video created successfully!")

# TIME FINAL
end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time,"\n")