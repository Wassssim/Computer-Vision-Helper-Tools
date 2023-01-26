import cv2

file_name = "2.mp4"
cap = cv2.VideoCapture("C:/Users/Wass/Downloads/" + file_name)
width  = int(cap.get(3))  # float `width`
height = int(cap.get(4))  # float `height`
fourcc = cv2.VideoWriter_fourcc(*'XVID')
print(width)
print(height)
out = cv2.VideoWriter( "./" + file_name, 0x7634706d, 24.0, (width, height))

while True:
    # Capture frame-by -frame
    try:
        ret, frame = cap.read()
        if not ret:
            break
    except:
        continue

    if not ret:
        break
    #cv2.imshow("test", frame)
    out.write(frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()