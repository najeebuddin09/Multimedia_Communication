import socket                
import cv2
from cv2.cv2 import getWindowProperty 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
  
port = 12345                
  
s.connect(('127.0.0.1', port)) 

while True:
    cv2.imshow('Input', s.recv(90000))

    c = cv2.waitKey(1)
    
    # if window is closed or escape is pressed
    if getWindowProperty('Input',0) | (c == 27):
        break

s.close()