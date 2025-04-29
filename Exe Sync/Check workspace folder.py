import os

# Absolute path of this script
current_file = os.path.abspath(__file__)
print("Current file:", current_file)

# Workspace folder (parent of the file)
workspace_folder = os.path.dirname(current_file)
print("Workspace folder:", workspace_folder)
