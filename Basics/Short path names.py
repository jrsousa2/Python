# CONVERTS AN MSYS2 PATH TO WINDOWS LONG AND THEN TO WINDOWS SHORT
# USED TO AVOID ERRORS WITH PATHS THAT HAVE BLANK SPACES
import os
import win32api
import subprocess

def msys2_to_win(msys_path):
    return subprocess.check_output(["cygpath", "-w", msys_path]).decode().strip()

def win_to_msys2(win_path):
    return subprocess.check_output(["cygpath", "-u", win_path]).decode().strip()

def get_short_path(path):
    return win32api.GetShortPathName(path)

def trans(msys_path):
    win_path = msys2_to_win(msys_path)
    print("Long path:", win_path)  # Output: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7

    short_path = get_short_path(win_path)
    if os.path.exists(short_path):
        print("Short path:", short_path)
        print("Final path:", win_to_msys2(short_path),"\n")
        return win_to_msys2(short_path)
    else:
        return "Error"

# Example usage 
msys_path = "/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.7/cuda-samples"

list = msys_path.split(":")
nbr= len(list)
trans_list = []
for i in range(nbr):
    trans_list.append(trans(list[i]))

print("Final->",nbr,"folders")
joined_string = ":".join(trans_list)
print(joined_string)

