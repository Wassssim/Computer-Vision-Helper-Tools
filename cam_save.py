import cv2

#stream = cv2.VideoCapture('http://192.168.254.19:80/1')

# Use the next line if your camera has a username and password
name = "out.avi"
stream = cv2.VideoCapture('rtsp://admin:Hardy123@192.168.254.19/Streaming/channels/101?udp')
fourcc = cv2.VideoWriter_fourcc(*"X264")
try:
    writer = cv2.VideoWriter("./{}".format(name), fourcc, 25, (int(stream.get(3)), int(stream.get(4))), True)
except Exception as e:
    print(e)
# rtsp://admin:admin@192.168.1.20/Streaming/Channels/101
while True:

    r, f = stream.read()
    if f is None:
        break
    cv2.imshow('IP Camera stream', cv2.resize(f, (1280,720)))
    writer.write(f)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

writer.release()
stream.release()
cv2.destroyAllWindows()