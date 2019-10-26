import socket  
import cv2             
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
print ("Socket successfully created")
  
port = 12345                
  
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
  
s.listen(5)      
print ("socket is listening")  

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")
  

c, addr = s.accept()      
print ('Got connection from', addr) 
 
while True: 
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)

    reten, buf = cv2.imencode(".jpg", frame)
    
    c.send(frame)

c.close()
s.close()