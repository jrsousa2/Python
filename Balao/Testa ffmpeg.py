# import ffmpeg
import shutil

def test_ffmpeg_path():
    # Check if ffmpeg is in the system's PATH
    ffmpeg_path = shutil.which('ffmpeg')
    
    if ffmpeg_path:
        print(f"FFmpeg is found at: {ffmpeg_path}")
    else:
        print("FFmpeg is not found in the system PATH.")

# Run the test
test_ffmpeg_path()
