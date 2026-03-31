# THIS CODE USES THE MS OFFICE PICTURE MANAGER TO APPLY AUTO CORRECT TO IMAGES
# CODE IS USED TO AUTOMATE, SINCE THERE ARE MANY PICTURES
# THIS CODE IS WORKING VERY WELL 
# ADDED FUNCTION TO ENSURE AUTO-CORRECT AND SAVE 
# FINISH BEFORE MOVING TO THE NEXT BATCH

from pywinauto import Application
import os
import shutil
import time

# from time import sleep
# from datetime import datetime
# from pywinauto.keyboard import send_keys

def wait_for_proc(dlg, timeout=30):
    """Wait until Auto Correct or Save finishes processing."""
    status = dlg.child_window(control_type="StatusBar")
    start = time.time()
    while True:
        try:
            text = status.window_text()
        except Exception:
            text = ""
        # check both possible indicators
        if not any(keyword in text for keyword in ["Processing", "Saving"]):
            break
        if time.time() - start > timeout:
            raise TimeoutError("Operation taking too long")
        time.sleep(0.1)

def Start_app(src):
    cmd = fr'"C:\Program Files\Microsoft Office\Office14\OIS.EXE" {src}'
    # Start OIS with the image
    app = Application(backend="uia").start(cmd)

    # Now get the main window
    dlg = app.top_window()
    dlg.wait('visible ready', timeout=10)

    # Bring window to front
    dlg.set_focus()

    # Select all (if folder mode)
    dlg.type_keys("^a", set_foreground=True)

    # Send Ctrl+Q to trigger Auto Correct
    dlg.type_keys("^q", set_foreground=True)

    # Wait until Auto Correct finishes
    wait_for_proc(dlg)

    # Save the image with Ctrl+S
    dlg.type_keys("^s", set_foreground=True)

    # Wait until Auto Correct finishes
    wait_for_proc(dlg)

    # Close the main window (prompts to save if needed)
    dlg.close()

    # Small delay to ensure it closes
    # sleep(0.2)

# ANY FILE MODIFIED BEFORE THIS DATE WILL BE PROCESSED 
# Latest_mod_date_str = "2026-03-30_15-45-59"
# Latest_mod_date = datetime.strptime(Latest_mod_date_str, "%Y-%m-%d_%H-%M-%S")

# TS = os.path.getmtime(src_folder + "\\" + images[0])
# mod_time = datetime.fromtimestamp(TS)

# images = [f for i,f in enumerate(images) if datetime.fromtimestamp(os.path.getmtime(src_folder+"\\"+f))<=Latest_mod_date and i<100]


# MAIN CODE 
# batch_size=How many pics will be edited at the same time in Office Picture Viewer
src_folder = r"F:\Videos\Pobres\Filter"
batch_size=100

# dest_folder = r"F:\Videos\Pobres\Done"
images = [f for f in os.listdir(src_folder) if f.lower().endswith(".png")]
# SORTS LIST
images.sort

# Create a folder counter
folder_counter = 1
for i in range(0, len(images), batch_size):
    batch = images[i:i+batch_size]
    
    # Create subfolder (F1, F2, ...)
    subfolder_name = f"F{folder_counter}"
    subfolder_path = os.path.join(src_folder, subfolder_name)
    os.makedirs(subfolder_path, exist_ok=True)
    
    # Move the batch into the subfolder
    for img in batch:
        src_path = os.path.join(src_folder, img)
        dest_path = os.path.join(subfolder_path, img)
        shutil.move(src_path, dest_path)
    
    print(f"Moved {len(batch)} images to {subfolder_name}")
    folder_counter += 1
    
    # CALLS THE MACRO
    Start_app(subfolder_path)
