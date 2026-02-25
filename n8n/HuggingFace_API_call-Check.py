import requests

#API_URL = "https://router.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

API_URL = "https://router.huggingface.co/models/gpt2"

API_URL2 = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

headers = {"Authorization": "Bearer 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"}

data = {"inputs": "Hello world"}

response = requests.post(API_URL, headers=headers, json=data)

response2 = requests.post(API_URL2, headers=headers, json=data)

print("Response text:", response.text)

print("Response2 text:", response2.text)

# If JSON fails, print raw text
try:
    print(response.json())
except:
    print("Response text:", response.text)