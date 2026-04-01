import importlib.metadata as md
import os

def get_dist_size(dist):
    total_size = 0

    try:
        files = dist.files
        if not files:
            return None

        for file in files:
            try:
                path = dist.locate_file(file)
                if os.path.isfile(path):
                    total_size += os.path.getsize(path)
            except OSError:
                pass

        return total_size

    except Exception:
        return None


packages_info = []

for dist in md.distributions():
    size = get_dist_size(dist)
    packages_info.append((dist.metadata["Name"], size))


# Sort:
# 1) valid sizes first
# 2) descending size
packages_info.sort(
    key=lambda x: (x[1] is None, -(x[1] or 0))
)


# Print results
for name, size in packages_info:
    if size is not None:
        print(f"{name}: {size / (1024 * 1024):.2f} MB")
    else:
        print(f"{name}: Directory not found.")