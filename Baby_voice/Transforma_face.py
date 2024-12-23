import cv2
import numpy as np

# Load the pre-trained model
model = cv2.dnn.readNetFromONNX('face_transformation_model.onnx')

# Load an image
image = cv2.imread("D:\\iTunes\\Baby\\Lula.jpg")
blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(256, 256), mean=(0, 0, 0), swapRB=True, crop=False)

# Perform the transformation
model.setInput(blob)
output = model.forward()

# Post-process the output
output = output.squeeze().transpose(1, 2, 0)
output = np.clip(output, 0, 255).astype(np.uint8)

# Show the result
cv2.imshow('Transformed Image', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
