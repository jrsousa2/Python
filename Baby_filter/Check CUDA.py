import dlib
print(dlib.DLIB_USE_CUDA)  # Should return True
print(dlib.cuda.get_num_devices())  # Should show your GPU count