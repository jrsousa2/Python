# BACK-UP FILES FROM E:\MP3 TO MICROSD CARD (G:\MP3)
# DELETE FILES WHOSE NAMES DON'T MATCH 
# COPY FILES IF MODIFIED DATE IS NEWER

import os
from shutil import copy2
from send2trash import send2trash
from random import sample

import sys
sys.path.insert(0, "D:\\Python\\iTunes\Modules")

from Files import get_Win_files, Set_diff, Set_common

# DOES BINARY COMPARISON
def comp_binary(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        data1 = f1.read()
        data2 = f2.read()
    comp = data1 == data2    
    return comp


Source = r"E:\MP3"
Dest = r"G:\MP3"

print("Building source file list")
Source_tuple = get_Win_files(Source, ".mp3")
Source_list = [x[6:] for (x,y) in Source_tuple]
nbr_files = len(Source_list)
print("Source file list has",nbr_files,"\n")

print("Building destination file list")
Dest_tuple = get_Win_files(Dest, ".mp3", Progress=True, Ref_total = nbr_files)
Dest_list = [x[6:] for (x,y) in Dest_tuple]
print("Destination file list has",len(Dest_list),"\n")

# NON-COMMON FILES THAT NEED TO BE COPIED
nc_files_to_copy = list(Set_diff(Source_list, Dest_list))
nbr_nc_to_copy = len(nc_files_to_copy)
print("There are",nbr_nc_to_copy,"non-common files to be copied to", Dest, "\n")

# COPYING NON-COMMON FILES
for i in range(nbr_nc_to_copy):
    src_file = Source + nc_files_to_copy[i]
    dst_file = Dest + nc_files_to_copy[i]
    print(f"Copying non-common file {i+1} of {nbr_nc_to_copy} to {Dest}: {src_file}")
    copy2(src_file, dst_file)

# BELOW COMPARISON IS CASE-INSENSITIVE
print("Building list of files in common\n")
common_files = Set_common(Source_list, Dest_list)

nbr_comm_files = len(common_files)
print("There are",nbr_comm_files,"files in common\n")

# Map back to original-case items from orig_set
# THESE ARE THE FILES TO BE COMPARED
print("Building list of source common files\n")
files_src = [x for (x,y) in Source_tuple if x[6:] in common_files]

# TAKES FILES IN THE SAME ORDER THAT THEY OCCUR IN THE SOURCE (NO NEED TO SORT ANYMORE)
print("Building list of destination common files\n")
files_dest = [Dest + x[6:] for (x,y) in Source_tuple if x[6:] in common_files]

# print("Building list of files for binary comparison\n")
# files_to_comp = [i for i in range(nbr_comm_files) if os.path.getmtime(files_src[i])==os.path.getmtime(files_dest[i])]
# # RANDOM SAMPLES TO CHECK IF FINE
# nbr_rand = 100
# files_to_comp2 = sample(files_to_comp, nbr_rand)

# print("Comparing",nbr_rand,"random samples of files with the same datestamp\n")
# files_comp = [i for i in range(nbr_rand) if not comp_binary(files_src[i],files_dest[i])]

# print("Random files compared",nbr_rand, "with",len(files_comp),"different\n")

print("Building list of common files to be copied")
files_to_copy = [i for i in range(nbr_comm_files) if os.path.getmtime(files_src[i]) > os.path.getmtime(files_dest[i])]

nbr_to_copy = len(files_to_copy)
print("There are",nbr_to_copy,"files to be copied to",Dest,"\n")

# COPIES THE FILES THAT DIFFER AT MODIFIED DATE
for i in range(nbr_to_copy):
    pos = files_to_copy[i]
    src_file = files_src[pos]
    dst_file = files_dest[pos]
    if os.path.getmtime(src_file) > os.path.getmtime(dst_file):
       print(f"Copying file {i+1} of {nbr_to_copy}: {src_file} to {Dest}")
       # before_copy = comp_binary(src_file,dst_file)
       # PRESERVES TIMESTAMP
       copy2(src_file, dst_file)
       # print("File comparison -- Before:", before_copy, " -- After:",comp_binary(src_file,dst_file),"\n")

# DELETE FILES THAT ARE NOT IN SOURCE FOLDER
# BELOW COMPARISON IS CASE-INSENSITIVE
files_to_del = list(Set_diff(Dest_list, Source_list))
nbr_to_del = len(files_to_del)
print("\nThere are",nbr_to_del,"files to be deleted from", Dest, "\n")

# DELETING FILES
for i in range(10): #range(nbr_to_del):
    dst_file = Dest + files_to_del[i]
    print(f"Deleting file {i+1} of {nbr_to_del}: {dst_file} (Len={1})")
    send2trash(dst_file)
