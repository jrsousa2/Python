import os
import re

folder = r"F:\Videos\Pobres\Output_Filter"

# matches: frame_1234.png
pattern = re.compile(r"^(frame_)(\d{1,4})(\.png)$", re.IGNORECASE)

for filename in os.listdir(folder):
    match = pattern.match(filename)
    if not match:
        continue

    prefix, number_str, ext = match.groups()
    number = int(number_str)

    # rename only <= 9999
    if number <= 9999:
        new_name = f"{prefix}{number:05d}{ext}"

        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)

        # avoid overwriting existing files
        if not os.path.exists(new_path):
            print(f"{filename} -> {new_name}")
            os.rename(old_path, new_path)
        else:
            print(f"Skipped (exists): {new_name}")

print("Done.")