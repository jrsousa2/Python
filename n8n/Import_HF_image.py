# THIS CODE TAKES THE BINARY FILE CREATED BY THE HF API
# USED THIS TO CONVERT BINARY FILE TO IMG 
# HF WAS SENDING FILE AS APPLICATION/JSON BASE64 INSTEAD OF IMAGE/PNG
# AFTER A NEW TOKEN WAS CREATED, IT STARTED TO WORK AS SUPPOSED (SAVING AS IMAGE)
import base64

input_dir = r"D:\Python\n8n\FLUX.1-schnell"

#input_dir = r"D:\Downloads_Chrome\FLUX.1-schnell"

output_dir = r"D:\Downloads_Chrome\\FLUX2.png"

#output= r"D:\Python\n8n\FLUX.png"

# Read the file as text (not binary)
with open(input_dir, "r") as f:
    b64data = f.read()

# Decode base64 to bytes
img_bytes = base64.b64decode(b64data)

# Save as PNG
with open(output_dir, "wb") as f:
    f.write(img_bytes)