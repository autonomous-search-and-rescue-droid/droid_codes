import cv2


url = 'http://192.168.1.73:8080/video'

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow('IP Webcam', frame)
    if cv2.waitKey(1) == 27:  
        break

cap.release()
cv2.destroyAllWindows()
