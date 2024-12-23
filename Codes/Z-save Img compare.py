def pattern_exists1(image_path, template_path, threshold=0.8):
    img = cv2.imread(image_path, 0)  # Load the image as grayscale
    template = cv2.imread(template_path, 0)  # Load the template as grayscale

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    Is_vinyl = False
    if max_val >= threshold:
       Is_vinyl = True
    return Is_vinyl

def pattern_exists2(image_data, template_data, threshold=0.8):
    img = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)  # Convert image to grayscale
    #template = cv2.imread(template_path, 0)  # Load the template as grayscale

    result = cv2.matchTemplate(img, template_data, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    Is_vinyl = False
    if max_val >= threshold:
       Is_vinyl = True
    return Is_vinyl

#         mp3_file = ID3(Arq[i])
#         # Get the image information
#         if "APIC:" in mp3_file:
#             image_data = mp3_file.get('APIC:').data
#             template_data = cv2.imread("D:\\Z-Covers\\Vinyl\\template.jpg", 0)
#             match = pattern_exists2(image_data, template_data)

# 1) Example usage
# image_path = 'path/to/image.jpg'  # Replace with the path to your image
# template_path = 'path/to/template_image.jpg'  # Replace with the path to your template image

# pattern_present = pattern_exists(image_path, template_path)
# print(pattern_present)

# 2) Example usage
# image_data = cv2.imread('path/to/image.jpg')  # Replace with your image data
# template_path = 'path/to/template_image.jpg'  # Replace with the path to your template image

# pattern_present = pattern_exists(image_data, template_path)
# print(pattern_present)