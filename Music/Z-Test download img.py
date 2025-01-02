import requests

# BAIXA A IMG
def Download_img(URL):
    url = 'https://example.com/image.jpg'  # Replace with the URL of the image file you want to download
    file_name = 'image.jpg'  # Replace with the desired file name for the downloaded image

    # Download the image
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

    print(f'Image has been downloaded as {file_name}')