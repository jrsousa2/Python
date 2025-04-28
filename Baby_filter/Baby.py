import cv2
import dlib

# Check if CUDA is available
if dlib.DLIB_USE_CUDA:
   print("CUDA is available! Using GPU.")
else:
   print("CUDA is not available. Using CPU.")

# Load the pre-trained face detector and facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\\Python\\Baby_filter\\shape_predictor_68_face_landmarks.dat")
#detector.set_gpu(0)

def apply_baby_filter(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = detector(gray)
    
    for face in faces:
        # Get the landmarks for the face
        landmarks = predictor(gray, face)
        
        # Example: Smoothing the skin (apply a Gaussian blur)
        roi = image[face.top():face.bottom(), face.left():face.right()]
        blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
        image[face.top():face.bottom(), face.left():face.right()] = blurred_roi

        # Additional features like enlarging eyes or reshaping facial features can be added here
        
    # Save or display the modified image
    cv2.imwrite("baby_filtered_image.jpg", image)
    cv2.imshow("Baby Filtered Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

apply_baby_filter("D:\\Python\\Baby_filter\\Lula.jpg")
