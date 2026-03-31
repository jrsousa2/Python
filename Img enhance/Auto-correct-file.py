# THIS CODE USES THE MS OFFICE PICTURE MANAGER TO APPLY AUTO CORRECT TO IMAGES
# CODE IS USED TO AUTOMATE, SINCE THERE ARE MANY PICTURES

from pywinauto import Application
import time

# Start OIS with the image
# BELOW IS OPENING TO A FOLDERn
app = Application(backend="uia").start(r'"C:\Program Files\Microsoft Office\Office14\OIS.EXE" F:\Videos\Pobres\Done')

# Get the process ID
pid = app.process

# Attach to the same process with a new Application object
app2 = Application(backend="uia").connect(process=pid)

# Now get the main window
dlg = app2.top_window()
dlg.wait('visible ready', timeout=10)

# Bring window to front
dlg.set_focus()

# Small delay to ensure image fully loaded
# time.sleep(1)

# Send Ctrl+Q to trigger Auto Correct
dlg.type_keys("^q", set_foreground=True)

# Small delay to ensure Auto Correct completes
time.sleep(0.1)

# Save the image with Ctrl+S
dlg.type_keys("^s", set_foreground=True)

# Close the main window (prompts to save if needed)
dlg.close()
