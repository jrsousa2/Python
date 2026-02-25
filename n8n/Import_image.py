# THIS CODE TAKES THE BINARY FILE CREATED BY THE HUGGING FACE API
import base64

# Read the file as text (not binary)
with open(r"D:\Python\n8n\FLUX.1-schnell", "r") as f:
    b64data = f.read()

# Decode base64 to bytes
img_bytes = base64.b64decode(b64data)

# Save as PNG
with open(r"D:\Python\n8n\FLUX.png", "wb") as f:
    f.write(img_bytes)