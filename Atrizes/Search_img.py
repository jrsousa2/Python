# THIS CODE WASN'T USED TO DOWNLOAD IMAGES AUTOMATICALLY DUE TO RESTRICTIONS 
# ON SEARCHING AND DOWNLOADING HIGH QUALITY IMAGES 

from selenium import webdriver
import time
import requests
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to download images
def download_images(search_query, num_images=3):
    # Setup Chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Construct search URL
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_query}"
    driver.get(search_url)

    # Give time for images to load
    time.sleep(2)

    # Click on the first few images to load the larger versions
    image_elements = driver.find_elements("tag name", "img")[:num_images]
    image_urls = []

    for img in image_elements:
        # Scroll to the image and wait for it to be clickable
        driver.execute_script("arguments[0].scrollIntoView();", img)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(img))
            img.click()
            time.sleep(1)  # Wait for the larger image to load

            # Find the larger image element
            large_image = driver.find_element("css selector", "img.n3VNCb")
            img_url = large_image.get_attribute("src")
            if img_url and img_url.startswith("http"):
                image_urls.append(img_url)
        except Exception as e:
            print(f"Could not retrieve image URL: {e}")

    # Save images locally
    os.makedirs("D:\\iTunes\\Atrizes\\images", exist_ok=True)
    for i, url in enumerate(image_urls):  # Limit to num_images
        try:
            img_data = requests.get(url).content
            with open(f"D:\\iTunes\\Atrizes\\images\\image_{i}.jpg", "wb") as file:
                file.write(img_data)
            print(f"Downloaded: {url}")  # Print the URL of the downloaded image
        except Exception as e:
            print(f"Error downloading image: {e}")
        time.sleep(1)  # Pause between downloads

    driver.quit()

# Example usage
download_images("atriz isadora Ribeiro jovem", num_images=3)
