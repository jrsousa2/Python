from PIL import Image, ImageOps
import pathlib
# from pathlib import Path

# DO IMG 10209 AS WELL
img_path = r"F:\Videos\Pobres\Output_Iris\frame_0048.png"
output_folder = r"F:\Videos\Pobres\Save"
filename = pathlib.Path(img_path).name

test = pathlib.Path(output_folder) / filename

img = Image.open(img_path)
img = ImageOps.autocontrast(img)  # simple auto-correct
img.save(pathlib.Path(output_folder) / filename)

