# import the necessary packages
import cv2
import numpy as np

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
rectangles=[]
refPt = []
ratioPt=[]
cropping = False

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping,ratioPt
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt.append((x, y))
		#ratioPt.append((x/width,y/height))
		print((x,y))
		#print(refPt)
		cropping = True



frame=None
image=None

input_video="F:/plates/tes3.mp4"
cap=cv2.VideoCapture(input_video) 
cnt=0
while(True):
    ret,frame = cap.read()
    image=frame
    cnt=cnt+1
    if cnt>100:
        break

destination_dim=(1440,1024)
input_dim=(1248,736)
image = cv2.resize(image,input_dim, interpolation = cv2.INTER_AREA)
(H,W)=image.shape[:2]
print((W,H))
scale=100
W=int((W*scale)/100)
H=int((H*scale)/100)
image=cv2.resize(image,(W,H))
#image=cv2.imread("./chessboard.png")
clone = image.copy()
frame=clone.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
flag=0
# keep looping until the 'q' key is pressed
prev=0
ROI_CORNERS=[]
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	if (len(refPt) % 4) > 1:
		cv2.line(image, refPt[-1], refPt[-2],(255,0,0),2)
	
	if (len(refPt) % 4) == 0 and len(refPt) > 0:
		roi_corners=refPt[-4:]          
		if not flag:
			print(roi_corners)
                
		#roi_corners[0],roi_corners[1]=roi_corners[1],roi_corners[0]
		src = np.float32(roi_corners)
		pts = np.array(src, np.int32)
		pts = pts.reshape((-1,1,2))
		cv2.polylines(image,[pts],True,(255,0,0),1) # Red in RGB; width: 10
		if ((len(refPt)/4)%2)==0:
			cv2.fillPoly(image, [pts], (255,0,0),lineType=cv2.LINE_AA)
		else:
			cv2.fillPoly(image, [pts], (0,255,0),lineType=cv2.LINE_AA)
		if (len(refPt)/4)!=prev:
			prev=(len(refPt))/4
			rectangles.append(roi_corners)
		if not flag:
			print("hjhhhhhhhhhhhhhhhhhh")
			
			print(roi_corners)
			flag=1
		cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		print("we finished!!!!!!!")
		print(rectangles)
		image = clone.copy()
		frame=clone.copy()
		flag=0
		refPt=[]
		rectangles=[]
	# if the 'c' key is pressed, break from the loop
	elif key == ord("q"):
		break
print("we finished")
print(rectangles)
for l in range(len(rectangles)):
		for i in range(len(rectangles[l])):
				x=int((rectangles[l][i][0]*destination_dim[0])/input_dim[0])
				y=int((rectangles[l][i][1]*destination_dim[1])/input_dim[1])
				rectangles[l][i]=(x,y)
print(rectangles)
cv2.destroyAllWindows()





