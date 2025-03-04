import yt_dlp

# Replace with your video URL
video_url = "https://www.youtube.com/watch?v=kOzGFJZZVe8"
# video_url = "https://youtu.be/hOnESTqThUs"

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading... {d['downloaded_bytes'] / d['total_bytes'] * 100:.2f}% complete", end="\r")

ydl_opts = {
    'outtmpl': 'D:\\Videos\\Pobres\\Praia.mp4',  # Output path
    'progress_hooks': [progress_hook],           # Hook to display progress
    'cookies': "D:\\Videos\\Pobres\\cookies.json"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])

print("\nDownload complete!")

