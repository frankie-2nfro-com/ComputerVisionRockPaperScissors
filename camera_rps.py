import rps
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# for bug and want to resume webcam in mac: sudo killall VDCAssistant

# Load the model
model = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)




# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
	# Capture the video frame
	# by frame
	ret, frame = vid.read()
  
	# Display the resulting frame
	cv2.imshow('frame', frame)

	# convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that 
	# the color is converted from BGR to RGB
	color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	image=Image.fromarray(color_coverted)
	#image = Image.open('./test_scissors.jpg')
	

	#resize the image to a 224x224 with the same strategy as in TM2:
	#resizing the image to be at least 224x224 and then cropping from the center
	size = (224, 224)
	image = ImageOps.fit(image, size, Image.ANTIALIAS)

	#turn the image into a numpy array
	image_array = np.asarray(image)
	# Normalize the image
	normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
	# Load the image into the array
	data[0] = normalized_image_array

	# run the inference
	prediction = model.predict(data)
	pPos = prediction[0][0]
	sPos = prediction[0][1]
	rPos = prediction[0][2]
	
	print(prediction);
	if rPos > 0.7 and rPos > pPos and rPos > sPos:
		print("R");
	elif pPos > 0.7 and pPos > rPos and pPos > sPos:
		print("P");
	elif sPos > 0.7 and sPos > rPos and sPos > pPos:
		print("S");
	else:
		print("NIL")

	# for calling when getting user input from camera
	#rps.play('R') 
	  
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

"""

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
	raise IOError("Cannot open webcam")
else:
	cap.open(0, cv2.CAP_DSHOW)
	while True:
		ret, frame = cap.read()
		if frame!=None and frame.height!=None:
			cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		
		#break


cap.release()
cv2.destroyAllWindows()
"""