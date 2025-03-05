from pytube import YouTube

# Define a progress function
def progress_function(stream, chunk, bytes_remaining):
    # Calculate the download progress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100
    print(f"Downloading... {percent:.2f}% complete", end="\r")

# Replace with your video URL
video_url = "https://www.youtube.com/watch?v=kOzGFJZZVe8&t=1095s&pp=ygUVb3MgcG9icmVzIHZhbyBhIHByYWlh"

# Create YouTube object
yt = YouTube(video_url, on_progress_callback=progress_function)

# Select highest resolution stream
video = yt.streams.get_highest_resolution()

# Download the video
video.download(output_path="D:\\Videos\\Pobres", filename="Praia.mp4")

print("\nDownload complete!")
