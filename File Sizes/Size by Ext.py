import os
from collections import defaultdict

def get_size_by_extension(directory):
    extension_sizes = defaultdict(int)
    
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1] or "No Extension"
            file_path = os.path.join(root, file)
            try:
                extension_sizes[ext] += os.path.getsize(file_path)
            except OSError as e:
                print(f"Error reading file {file_path}: {e}")
    
    # Sort by size in descending order and print
    sorted_extensions = sorted(extension_sizes.items(), key=lambda x: x[1], reverse=True)
    for ext, size in sorted_extensions:
        print(f"{ext}: {size / (1024 * 1024):.2f} MB")

# Change the path below to the folder you want to analyze
#folder_path = r"D:\iTunes"
folder_path = r"D:\SAS"
get_size_by_extension(folder_path)
