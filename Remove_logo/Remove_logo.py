import cv2

# Load the image
image = cv2.imread('image.jpg')

# Coordinates of the logo/text to remove (x, y, width, height)
x, y, w, h = 100, 50, 200, 50

# Blur or fill the area
image[y:y+h, x:x+w] = cv2.GaussianBlur(image[y:y+h, x:x+w], (51, 51), 0)

# Save the result
cv2.imwrite('output.jpg', image)
