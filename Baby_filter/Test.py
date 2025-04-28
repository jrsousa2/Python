import cv2
import dlib
import numpy as np

# Check if CUDA is available
if dlib.DLIB_USE_CUDA:
    print("CUDA is available! Using GPU.")
else:
    print("CUDA is not available. Using CPU.")

# Load the pre-trained face detector and facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\\Python\\Baby_filter\\shape_predictor_68_face_landmarks.dat")

def apply_baby_filter(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = detector(gray)
    
    for face in faces:
        # Get the landmarks for the face
        landmarks = predictor(gray, face)
        
        # Extract the face region
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        roi = image[y:y+h, x:x+w]
        
        # Apply skin smoothing (bilateral filter for edge preservation)
        smooth_face = cv2.bilateralFilter(roi, d=15, sigmaColor=75, sigmaSpace=75)
        
        # Increase brightness and contrast for a youthful look
        brightened = cv2.convertScaleAbs(smooth_face, alpha=1.2, beta=20)
        
        # Replace the face region with the rejuvenated version
        image[y:y+h, x:x+w] = brightened

    # Save or display the modified image
    cv2.imwrite("baby_filtered_image2.jpg", image)
    cv2.imshow("Baby Filtered Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

apply_baby_filter("D:\\Python\\Baby_filter\\Lula.jpg")
