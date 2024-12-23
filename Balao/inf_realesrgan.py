import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact
#from sys import exit
from time import time, strftime, localtime
import matplotlib.pyplot as plt
from gc import collect # Add garbage collection import at the start
import torch  # Ensure torch is imported

# LIST FILES FROM FOLDER
def folder_files(folder_path, ext=None):
    # List all files in the folder, filter out directories
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(ext)]
    # Sort the files alphabetically
    files.sort()
    return files

def main():
    """Inference demo for Real-ESRGAN.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default='inputs', help='Input image or folder')
    parser.add_argument(
        '-n',
        '--model_name',
        type=str,
        default='RealESRGAN_x4plus',
        help=('Model names: RealESRGAN_x4plus | RealESRNet_x4plus | RealESRGAN_x4plus_anime_6B | RealESRGAN_x2plus | '
              'realesr-animevideov3 | realesr-general-x4v3'))
    parser.add_argument('-o', '--output', type=str, default='results', help='Output folder')
    parser.add_argument(
        '-dn',
        '--denoise_strength',
        type=float,
        default=0.5,
        help=('Denoise strength. 0 for weak denoise (keep noise), 1 for strong denoise ability. '
              'Only used for the realesr-general-x4v3 model'))
    parser.add_argument('-s', '--outscale', type=float, default=4, help='The final upsampling scale of the image')
    parser.add_argument(
        '--model_path', type=str, default=None, help='[Option] Model path. Usually, you do not need to specify it')
    parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored image')
    parser.add_argument('-t', '--tile', type=int, default=0, help='Tile size, 0 for no tile during testing')
    parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding')
    parser.add_argument('--pre_pad', type=int, default=0, help='Pre padding size at each border')
    parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN to enhance face')
    parser.add_argument(
        '--fp32', action='store_true', help='Use fp32 precision during inference. Default: fp16 (half precision).')
    parser.add_argument(
        '--alpha_upsampler',
        type=str,
        default='realesrgan',
        help='The upsampler for the alpha channels. Options: realesrgan | bicubic')
    parser.add_argument(
        '--ext',
        type=str,
        default='auto',
        help='Image extension. Options: auto | jpg | png, auto means using the same extension as inputs')
    parser.add_argument(
        '-g', '--gpu-id', type=int, default=None, help='gpu device to use (default=None) can be 0,1,2 for multi-gpu')

    args = parser.parse_args()
    
    # determine models according to model names
    model_path = None
    args.model_name = args.model_name.split('.')[0]
    if args.model_name == 'RealESRGAN_x4plus':  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRGAN_x4plus.pth"
    elif args.model_name == 'RealESRNet_x4plus':  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth']
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRNet_x4plus.pth"
    elif args.model_name == 'RealESRGAN_x4plus_anime_6B':  # x4 RRDBNet model with 6 blocks
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']
        model_path = "D:\\iTunes\\Balao\\weights\\RealESRGAN_x4plus_anime_6B.pth"
    elif args.model_name == 'RealESRGAN_x2plus':  # x2 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth']
    elif args.model_name == 'realesr-animevideov3':  # x4 VGG-style model (XS size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
    elif args.model_name == 'realesr-general-x4v3':  # x4 VGG-style model (S size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
        netscale = 4
        file_url = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth',
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth'
        ]

    # CHECK WHAT THE PMTS ARE
    print("\nArgs are", vars(args))
    print("\nModel path arg:",args.model_path)
    print("Model path:",model_path)
    print("URL:",file_url)
    print("URL is only used if model path is None\n")
    print("\nOutput",args.output)
    # inputvar = input("\nPres a key to continue...")
    # determine model paths
    if args.model_path is not None and model_path is None:
        model_path = args.model_path
    elif model_path is None:
         model_path = os.path.join('weights', args.model_name + '.pth')
         print("\nModel path variable:",model_path)
         print("Model file is found:",os.path.isfile(model_path))
         if not os.path.isfile(model_path):
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            print("Downloading model...DIR:",ROOT_DIR)
            for url in file_url:
                # model_path will be updated
                model_path = load_file_from_url(
                    url=url, model_dir=os.path.join(ROOT_DIR, 'weights'), progress=True, file_name=None)

    # use dni to control the denoise strength
    dni_weight = None
    if args.model_name == 'realesr-general-x4v3' and args.denoise_strength != 1:
        wdn_model_path = model_path.replace('realesr-general-x4v3', 'realesr-general-wdn-x4v3')
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

    if args.face_enhance:  # Use GFPGAN for face enhancement
        from gfpgan import GFPGANer
        face_enhancer = GFPGANer(
            # IF THIS ONE IS COMMENTED OUT, IT WILL DOWNLOAD FROM THE INTERNET (DESABILITAR)
            # model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
            model_path = "D:\\iTunes\\Balao\\weights\\GFPGANv1.3.pth",
            upscale=args.outscale,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=upsampler)
    
    
    os.makedirs(args.output, exist_ok=True)

    # CREATES LIST OF FILES TO BE PROCESSED
    if os.path.isfile(args.input):
       paths = [args.input]
    else:
        # paths = sorted(glob.glob(os.path.join(args.input, '*')))
        folder_path = args.input
        paths = folder_files(folder_path, ext=".png")
    
    # Test
    #print("\nGlob paths:",paths)
    
    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print("\nProcessing",idx+1,"of",len(paths),":",path)
        print("Output Dir:",args.output, "Image:", imgname, "Suff:", args.suffix, "Ext:", extension)
        if args.ext == "auto":
           extension = extension[1:]
        else:
           extension = args.ext
        # RF (RAW FORMATTED) EH USADO PARA TRATAR \ LITERALMENTE (NAO EH CMD) E POSSIBILITA VARIAVEIS
        output_folder = "iTunes\\Balao\\Input2"
        if args.suffix == '':
            # save_path = os.path.join(args.output, f'{imgname}.{extension}')
            save_path = rf'D:\{output_folder}\{imgname}.png'
        else:
            # save_path = os.path.join(args.output, f'{imgname}_{args.suffix}.{extension}')
            save_path = rf'D:\{output_folder}\{imgname}_{args.suffix}.{extension}'
        
        # DISPLAY MSG
        print("Will save output to",save_path)
        if not os.path.exists(save_path):
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img_mode = 'RGBA'
            else:
                img_mode = None
            #print('Image mode', img_mode)    

            # stop program
            # exit()
            try:
                if args.face_enhance:
                    print(f"\nEnhancing face in {path}...\n")
                    _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
                    #print(f"Face enhancement completed for {imgname}.")
                else:
                    print(f"\nUpscaling image {path} by",args.outscale)
                    output, _ = upsampler.enhance(img, outscale=args.outscale)
                    print("Output shape:", output.shape)
                    print("Output dtype:", output.dtype)
                    print("Output min/max values:", output.min(), output.max())
                    #array_size = output.nbytes
                    print(f"Memory size of the array: {output.nbytes} bytes")
                    # Assuming 'output' is the image array
                    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct display
                    #plt.axis('off')  # Hide axis
                    plt.show()
                    #print(f"Upscaling completed for {imgname}.")
                    x = input("Press a key")
            except RuntimeError as error:
                print(f"Error processing {path}: {error}")
                print('Error', error)
                print('If you encounter CUDA out of memory, try to set --tile with a smaller number.')
            else:
                if img_mode == 'RGBA':  # RGBA images should be saved in png format
                   extension = 'png'
                # ret = cv2.imwrite(save_path, output)
                # TRIES TO OUTPUT TO D:\
                # ret = cv2.imwrite(r'D:\iTunes\Balao\Input2\test.png', output)
                ret = cv2.imwrite(r'C:\temp\test.png', output)
                print("\nSaving image to:", save_path, "RC:", ret)
                # Memory cleanup
                try:
                    del img, output  # Release the image and output variables
                    torch.cuda.empty_cache()  # Free GPU cache
                    collect()  # Run garbage collection for any remaining references
                except:
                    print("Can't release memory") 


if __name__ == '__main__':
    # Record the start time
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