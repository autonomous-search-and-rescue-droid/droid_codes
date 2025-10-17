import cv2

# This URL must be an active video stream on your network
url = 'http://192.168.1.73:8080/video' 
cap = cv2.VideoCapture(url)

# Correctly initialize the A-KAZE detector from OpenCV
# The line from pyslam is removed
detector = cv2.AKAZE_create() 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Check the video stream.")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use the detector to find keypoints
    # The .detect() method is correct
    kpts = detector.detect(gray, None) 
    
    # Draw the keypoints on the original frame
    out = cv2.drawKeypoints(frame, kpts, None, color=(0,255,0))
    
    cv2.imshow('Features', out)
    
    # Press 'ESC' to exit
    if cv2.waitKey(1) == 27: 
        break

cap.release()
cv2.destroyAllWindows()