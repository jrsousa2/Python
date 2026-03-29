from PIL import Image, ImageOps
import pathlib

input_folder = r"F:\Images\Input"
output_folder = r"F:\Images\Output"
pathlib.Path(output_folder).mkdir(exist_ok=True)

for img_path in pathlib.Path(input_folder).glob("*.png"):  # or *.jpg
    img = Image.open(img_path)
    img = ImageOps.autocontrast(img)  # simple auto-correct
    img.save(pathlib.Path(output_folder) / img_path.name)