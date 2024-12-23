import pkg_resources
import os

def get_package_size(package_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(package_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            total_size += os.path.getsize(file_path)
    return total_size

packages_info = []

packages = pkg_resources.working_set
for package in packages:
    package_path = os.path.join(package.location, package.project_name)
    
    if os.path.exists(package_path):
        package_size = get_package_size(package_path)
        packages_info.append((package.project_name, package_size))
    else:
        packages_info.append((package.project_name, None))  # Store None for sizes not found

# Sort packages by size in descending order, keeping 'not found' at the bottom
packages_info.sort(key=lambda x: (x[1] is None, -x[1] if x[1] is not None else 0))

# Print package sizes
for package_name, size in packages_info:
    if size is not None:
        print(f"{package_name}: {size / (1024 * 1024):.2f} MB")
    else:
        print(f"{package_name}: Directory not found.")
