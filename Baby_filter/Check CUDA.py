import dlib

# import os
# os.add_dll_directory(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin')
# os.add_dll_directory(r'C:\Program Files\NVIDIA\CUDNN\v9.6\bin\11.8')


print(dlib.__version__)

print(dlib.DLIB_USE_CUDA)  # Should return True
print(dlib.cuda.get_num_devices())  # Should show your GPU count