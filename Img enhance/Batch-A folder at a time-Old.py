from pywinauto import Application
from pywinauto.keyboard import send_keys
import time

FOLDER = r"F:\Videos\Pobres\Done"

# Start Picture Manager (NO image)
app = Application(backend="uia").start(
    r'"C:\Program Files\Microsoft Office\Office14\OIS.EXE" F:\Videos\Pobres\Done'
)

dlg = app.top_window()
dlg.wait('visible ready', timeout=10)
dlg.set_focus()

# Open Locate Pictures / folder navigation
# send_keys("^l")        # Ctrl+L = Locate Pictures
# time.sleep(0.5)

# Type folder path
# send_keys(FOLDER + "{ENTER}")
# time.sleep(2)          # allow thumbnails to load

# Select all images (or first 100 later)
send_keys("^a")
time.sleep(0.2)

# Auto Correct ALL selected images
send_keys("^q")
time.sleep(1)

# Save ALL
send_keys("^s")
time.sleep(1)

dlg.close()