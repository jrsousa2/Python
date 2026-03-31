# THIS CODE USES THE MS OFFICE PICTURE MANAGER TO APPLY AUTO CORRECT TO IMAGES
# CODE IS USED TO AUTOMATE, SINCE THERE ARE MANY PICTURES

from pywinauto import Application
from time import sleep

from os import listdir, rename

def Start_app(file):
    cmd = fr'"C:\Program Files\Microsoft Office\Office14\OIS.EXE" {file}'
    # Start OIS with the image
    app = Application(backend="uia").start(cmd)

    # Now get the main window
    dlg = app.top_window()
    dlg.wait('visible ready', timeout=10)

    # Bring window to front
    dlg.set_focus()

    # Send Ctrl+Q to trigger Auto Correct
    dlg.type_keys("^q", set_foreground=True)

    # Small delay to ensure Auto Correct completes
    sleep(0.2)

    # Save the image with Ctrl+S
    dlg.type_keys("^s", set_foreground=True)

    # Small delay to ensure Auto Correct completes
    sleep(0.2)

    # Close the main window (prompts to save if needed)
    dlg.close()

# MAIN CODE 
src_folder = r"F:\Videos\Pobres\Test"
dest_folder = r"F:\Videos\Pobres\Done"
images = [f for f in listdir(src_folder) if f.lower().endswith(".png")]

files = ""
for f in images:
    file = src_folder + "\\" + f
    files = files + " " + file

Start_app(files)
