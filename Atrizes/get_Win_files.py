from os.path import exists
import os
from re import sub
from unidecode import unidecode
# This module obtains the MP3 ID3 tags indirectly
import eyed3
from tinytag import TinyTag
from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3

# Example: extensions provided as a list
extensions = ['.jpg', '.png', '.gif']

# Check if the file ends with any of the extensions
if file.endswith(tuple(extensions)):  # Convert list to tuple
    print("File has a valid extension!")

    # SCANS A WINDOWS FOLDER FOR FILES 
# CLEANS-UP THE RESULTS FOR OPTIMAL SEARCH AND RETURNS A LIST OF TUPLES
def get_Win_files(dir, ext):

    total_files = sum(len(files) for _, _, files in os.walk(dir))
    process_files = 0

    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            # PROGRESS
            # process_files += 1
            # if process_files % 4000==1:
            #     progress_perc = (process_files / total_files) * 100
            #     print(f"Progress: {progress_perc:.0f}%")
            
            # ADDS FILE TO LIST ONLY IF MP3 (OR EXT PROVIDED)
            if file.endswith(ext):
               file_list.append(os.path.join(root, file))

    # NORMALIZE FILE LIST FOR SEARCHES IGNORING CASE AND ACCENTS
    normal_filelist = [(file, unidecode(file_wo_ext(file.lower()))) for file in file_list]           
    return normal_filelist

