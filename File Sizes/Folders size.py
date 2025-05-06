import os

def get_folder_sizes_in_mb(folder_path):
    folder_sizes = []

    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        if os.path.isdir(subfolder_path):
            total_size = sum(
                os.path.getsize(os.path.join(subfolder_path, f))
                for f in os.listdir(subfolder_path)
                if os.path.isfile(os.path.join(subfolder_path, f))
            )
            folder_sizes.append((subfolder, total_size / (1024 * 1024)))  # Size in MB

    # Sort by size in descending order
    folder_sizes.sort(key=lambda x: x[1], reverse=True)

    for folder_name, size in folder_sizes:
        print(f"Folder: {folder_name}: {size:.2f} MB")

# Example usage:
get_folder_sizes_in_mb(r"C:\Python\Python3.9-v1\Lib\site-packages")
