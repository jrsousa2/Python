# THIS CODE REVERSES THE FRAMES THAT WILL BE ASSEMBLED IN FFMPEG
# THAT WAY THE VIDEO WILL PLAY IN REVERVE
# GOING TO THIS TROUBLE TO MAKE FFMPEG NOT SKIP ANY FRAME (IF USING REVERSE MODE)
import os
import shutil

src_dir = r"D:\Videos\Balao2\Output_Iris"
dst_dir = r"D:\Videos\Balao2\Output_Iris_Rev"

os.makedirs(dst_dir, exist_ok=True)

# collect frames
frames = [f for f in os.listdir(src_dir) if f.startswith("frame_") and f.endswith(".png")]

# sort by number
frames.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# reverse order
frames = frames[::-1]

# rename sequentially
for i, filename in enumerate(frames, start=1):
    src_path = os.path.join(src_dir, filename)
    new_name = f"frame_{i:04d}.png"
    dst_path = os.path.join(dst_dir, new_name)

    shutil.copy2(src_path, dst_path)

    # Display a message of the progress
    if i % 100 == 0:
        print(f"{i} frames processed...")

print(f"Done. {len(frames)} frames written to {dst_dir}")