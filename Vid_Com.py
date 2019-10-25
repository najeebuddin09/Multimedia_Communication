import cv2
from cv2.cv2 import getWindowProperty

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")


while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    
    # if escape is pressed
    if c == 27:
        break
    
    # if window is closed
    if getWindowProperty('Input',0):
        break

cap.release()
cv2.destroyAllWindows()