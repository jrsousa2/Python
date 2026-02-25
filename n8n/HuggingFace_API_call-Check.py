import requests
import os

#API_URL = "https://router.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

API_URL2 = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

HF_Token = os.getenv("HF_TOKEN")

headers = {"Authorization": "Bearer " + HF_Token}

data = {"inputs": "Hello world"}

response = requests.post(API_URL, headers=headers, json=data)

response2 = requests.post(API_URL2, headers=headers, json=data)

print("1st Try: Status code:", response.status_code)
print("1st Try: Status description:", response.reason,"\n")
#print("Response text:", response.text)

print("2nd URL: Status code:", response2.status_code)
print("2nd URL: Status description:", response2.reason)
if response2.reason != 'OK':
   print("Response text:", response2.text)

# If JSON fails, print raw text
# try:
#     print(response.json())
# except:
#     print("Response text:", response.text)