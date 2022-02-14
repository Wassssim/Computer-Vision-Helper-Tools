import cv2

#stream = cv2.VideoCapture('http://192.168.254.19:80/1')

# Use the next line if your camera has a username and password
stream = cv2.VideoCapture('rtsp://admin:Hardy123@196.178.97.139:554/Streaming/Channels/101')  
# rtsp://admin:admin@192.168.1.20/Streaming/Channels/101
while True:

    r, f = stream.read()
    cv2.imshow('IP Camera stream', cv2.resize(f, (1280,720)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()