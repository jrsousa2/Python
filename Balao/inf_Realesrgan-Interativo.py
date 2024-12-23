# AQUI O MODELO DE AI EH LOADED APENAS UMA VEZ E APLICADO A VARIAS IMAGENS

from argparse import Namespace
import cv2
import os
#from os.path import exists
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact
from time import time, strftime, localtime
from gc import collect # Add garbage collection import at the start
import torch  # Ensure torch is imported
# import matplotlib.pyplot as plt
from sys import exit

# LIST FILES FROM FOLDER
def folder_files(folder_path, ext=None):
    # List all files in the folder, filter out directories
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(ext)]
    # Sort the files alphabetically
    files.sort()
    return files

def main():
    # Mimicking the argparse behavior by creating a Namespace object
    args = Namespace()
    args.input = "D:\\iTunes\\Balao\\Input3"
    # args.input = "C:\\Output_640x480_anime"
    # args.input = "C:\\temp2"
    args.denoise_strength = 0.5
    args.outscale = 3
    # args.model_name = "RealESRGAN_x4plus_anime_6B"
    args.model_name = "RealESRGAN_x4plus"
    args.model_path = None
    args.suffix = ""
    args.tile = 320
    args.tile_pad = 10
    args.pre_pad = 0
    args.face_enhance = True
    args.fp32 = False
    args.alpha_upsampler = "realesrgan"
    args.ext = "auto"
    args.gpu_id = 0
    # output_folder = "Output_640x480_anime"
    # output_folder = "Output_640x480_x4Plus"
    # output_folder = "Output_640x480_Face"
    # output_folder = "Output_640x480_Anime_Face"
    output_folder = "Output_final2"
    
    model_path = None
    # determine models according to model names realesrgan-x4plus
    args.model_name = args.model_name.split(".")[0]
    if args.model_name == "RealESRGAN_x4plus":  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"]
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRGAN_x4plus.pth"
    elif args.model_name == "RealESRNet_x4plus":  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth"]
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRNet_x4plus.pth"
    elif args.model_name == "RealESRGAN_x4plus_anime_6B":  # x4 RRDBNet model with 6 blocks
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"]
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRGAN_x4plus_anime_6B.pth"
    elif args.model_name == "RealESRGAN_x2plus":  # x2 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        file_url = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"]
    elif args.model_name == "realesr-animevideov3":  # x4 VGG-style model (XS size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type="prelu")
        netscale = 4
        file_url = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth"]
    elif args.model_name == "realesr-general-x4v3":  # x4 VGG-style model (S size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type="prelu")
        netscale = 4
        file_url = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth"
        ]

    # determine model paths
    if args.model_path is not None and model_path is None:
       model_path = args.model_path
    elif model_path is None:
         model_path = os.path.join("weights", args.model_name + ".pth")
         if not os.path.isfile(model_path):
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            for url in file_url:
                print("\nDownloading model...")
                # model_path will be updated
                model_path = load_file_from_url(
                    url=url, model_dir=os.path.join(ROOT_DIR, "weights"), progress=True, file_name=None)

    # use dni to control the denoise strength
    dni_weight = None
    if args.model_name == "realesr-general-x4v3" and args.denoise_strength != 1:
        wdn_model_path = model_path.replace("realesr-general-x4v3", "realesr-general-wdn-x4v3")
        model_path = [model_path, wdn_model_path]
        dni_weight = [args.denoise_strength, 1 - args.denoise_strength]

    # restorer
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=args.tile,
        tile_pad=args.tile_pad,
        pre_pad=args.pre_pad,
        half=not args.fp32,
        gpu_id=args.gpu_id)

    model_rootpath = ""
    if args.face_enhance:  # Use GFPGAN for face enhancement
        from gfpgan import GFPGANer
        face_enhancer = GFPGANer(
            # model_path="https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth",
            model_path = "D:\\iTunes\\Balao\\weights\\GFPGANv1.3.pth",
            upscale=args.outscale,
            arch="clean",
            channel_multiplier=2,
            bg_upsampler=upsampler
            )
    
    print("\nDestination folder")
    try:
        os.makedirs(rf'C:\{output_folder}', exist_ok=True)
        print("Directory created or already exists:",rf'C:\{output_folder}')
    except OSError as e:
        print(f"Error creating directory: {e}")
    #os.makedirs(args.output, exist_ok=True)

    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        # paths = sorted(glob.glob(os.path.join(args.input, "*")))
        folder_path = args.input
        paths = folder_files(folder_path, ext=".png")

    # STARTS THE ROUTINE
    nbr = len(paths)
    for idx in range(nbr):
        path = paths[idx]
        imgname, ext2 = os.path.splitext(os.path.basename(path))
        # RF (RAW FORMATTED) EH USADO PARA TRATAR \ LITERALMENTE (NAO EH CMD) E POSSIBILITA VARIAVEIS
        save_path = rf'C:\{output_folder}\{imgname}.png'
        
        if not os.path.exists(save_path):
            print("\nProcessing",idx+1,"of",nbr,":",path)
            # print("Source image:", path, "\\ Dest folder:", save_path)

            # LOADS THE IMAGE
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img_mode = "RGBA"
            else:
                img_mode = None
            # print("Image mode", img_mode)    

            # PERFORMS UPSCALE OF THE IMAGE
            try:
                if args.face_enhance:
                    print(f"\nEnhancing face in {path}...")
                    _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
                else:
                    # print(f"Upscaling image {path} by factor",args.outscale)
                    output, _ = upsampler.enhance(img, outscale=args.outscale)
            except RuntimeError as error:
                print(f"Error processing {path}: {error}")
                print("If you encounter CUDA out of memory, try to set --tile with a smaller number.")
                print("Halting...")
                exit()
            else:
                # SAVE IMG
                # save_path = rf'C:\temp\{imgname}.png'
                ret = cv2.imwrite(rf'C:\{output_folder}\{imgname}.png', output)
                if not ret:
                    print("\nOutput shape:", output.shape)
                    print("Output dtype:", output.dtype)
                    print("Output min/max values:", output.min(), output.max())
                    print(f"Memory size of the array: {output.nbytes} bytes")
                    print("\nSave failed:", save_path) 
                else:
                    print("\nSaved image to:", save_path)
                # Memory cleanup
                try:
                    del img, output  # Release the image and output variables
                    torch.cuda.empty_cache()  # Free GPU cache
                    collect()  # Run garbage collection for any remaining references
                except:
                    print("\nCan't release memory")    
        else:
            print("Skipping",save_path)

#  Record the start time
start_time = time()
fmt_start_time = strftime("%H:%M:%S", localtime(start_time))
print(f"\nStart time: {fmt_start_time}")
# CALL FUNCTION
main()
# Record the end time
end_time = time()

# Calculate the elapsed time in minutes
elapsed_time = (end_time - start_time) / 60
print(f"\nElapsed time: {elapsed_time:.2f} minutes")