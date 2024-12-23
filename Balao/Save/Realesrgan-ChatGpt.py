# NAO FUNCIONA PQ O MODEL NAO ESTA CONSTRUIDO 
# SUGERIDO POR CHAT GPT

from realesrgan import RealESRGANer
import cv2

def upscale_video(input_path, output_path, scale=4, model_path="D:\\iTunes\\Balao\\RealESRGAN_x4plus.pth"): #RealESRGAN_x4plus.pth
    # Initialize the RealESRGAN model
    model = RealESRGANer(model_path=model_path, scale=scale)
    #model = RealESRGANer(scale=4, model=model, model_path=model_path)

    # Open input video
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Upscale each frame
        upscaled_frame = model.enhance(frame)
        out.write(upscaled_frame)

    # Release video resources
    cap.release()
    out.release()

# Run the function
upscale_video("D:\\iTunes\\Balao\\Balao.mp4", "D:\\iTunes\\Balao\\Balao2.mp4", scale=2)
