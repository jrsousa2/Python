# IMG RESULTANTE FICOU MUITO RUIM

from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
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

print("Loading model...")
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    cache_dir=HF_home
).to("cuda")

# TENTAR SE DER PAU
# pipe.enable_attention_slicing()
# pipe.enable_sequential_cpu_offload()

# fast + SD-friendly size
img = Image.open("D:\\Videos\\Lula\\Lula.jpg").convert("RGB")  

w, h = img.size
scale = 512 / max(w, h)
new_size = (int(w * scale), int(h * scale))

init_image = img.resize(new_size, Image.LANCZOS)

print("Calling pipe...will take a while")
result = pipe(
    prompt="baby version of the same person, realistic toddler face",
    image=init_image,
    strength=0.5,
    guidance_scale=7.5
).images[0]

result.save("D:\\Videos\\Lula\\Baby_diffusers.png")

# TIME FINAL
end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time,"\n")