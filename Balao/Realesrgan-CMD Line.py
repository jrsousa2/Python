# CHAMA O PACOTE VIA LINHA DE COMANDO
# O ALGORITMO BURRO DO CHAT GPT NAO SOUBE A FORMA CORRETA DE USAR
# NAO SERA MAIS NECESSARIO SE EU CONSEGUIR FAZER A CHAMADA DIRETO, AGORA QUE EU SEI COMO FUNCIONA

#def upscale_video(input_path, output_path, scale=4, model_path="D:\\Python\\Balao\\RealESRGAN_x4plus.pth"): #RealESRGAN_x4plus.pth


import subprocess
import os

def upscale_video(input_path, output_path, outscale=4, model_name="D:\\Python\\Balao\\RealESRGAN_x4plus.pth"):
    # Build the command to run the inference script
    command = [
        "C:\\Python\\MyEnv\\Scripts\\python", "inference_realesrgan_video.py",
        "--input", input_path,
        "--output", output_path,
        "--outscale", str(outscale),
        "--model_name", model_name
    ]

    subprocess.run(command, check=True)


def upscale_image(input_path, output_path, outscale=2, model_name = "RealESRGAN_x4plus_anime_6B"):
    # Build the command to run the inference script
    command = [
        "C:\\Python\\MyEnv\\Scripts\\python", "D:\\Python\\Balao\\inference_realesrgan.py",  # Path to your script
        "--input", input_path,
        "--output", output_path,
        "--model_path", "D:\\Python\\Balao\\weights\\RealESRGAN_x4plus_anime_6B.pth",
        "--model_name", model_name,
        "--outscale", str(outscale),
        "--suffix", "upscaled"
    ]

    subprocess.run(command, check=True)

    # Return the path to the upscaled image
    img_name, ext = os.path.splitext(input_path)
    upscaled_image = os.path.join(
        os.path.dirname(output_path), f"{img_name}_upscaled{ext}"
    )
    return upscaled_image

# MAIN NAME
# Run the function
#upscale_video("D:\\Python\\Balao\\Balao.mp4", "D:\\Python\\Balao\\Balao2.mp4", outscale=2)

upscale_image("D:\\Python\\Balao\\teaser.jpg", "D:\\Python\\Balao\\teaser2.jpg", outscale=2)
