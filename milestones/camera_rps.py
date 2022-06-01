import milestones.rps as rps
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import milestones.rps as rps;

# for bug and want to resume webcam in mac: sudo killall VDCAssistant



# Load the model
model = load_model('./assets/models/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

select_options = {"R":"Rock", "P":"Paper", "S":"Scissors", "NIL":"Nil"};


# define a video capture object
vid = cv2.VideoCapture(0)
  
counter = 50
choice = "NIL"
lastChoice = "NIL"
winner = "";
lastChoiceImage = None;
lastResult = [];
playing_round = 0;

game_over = False
user_mark = 0
computer_mark = 0

while(True):
	# Capture the video frame
	# by frame
	ret, frame = vid.read()


	if not game_over:
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
	
		#print(prediction);
		if sPos > 0.5:		# and sPos > rPos
			#print("S")
			choice = "S"
		elif rPos > 0.7 and rPos > pPos and rPos > sPos:
			#print("R");
			choice = "R"
		elif pPos > 0.7 and pPos > rPos and pPos > sPos:
			#print("P")
			choice = "P"
		#else:
			#print("NIL")

		computer_choice = rps.get_computer_choice();

	#if lastChoice!="NIL" and lastChoice!=choice:
	#	lastChoiceImage = ImageOps.fit(frame, (224, 224), Image.ANTIALIAS)

	if not game_over:
		cv2.putText(img=frame, text='Timer: ' + str(counter) + '?!', org=(50, 50), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 255, 0),thickness=3)
	
	if not game_over:
		cv2.putText(img=frame, text='You are ' + select_options[choice], org=(100, 150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 255),thickness=3)
		cv2.putText(img=frame, text='Computer are ' + select_options[computer_choice], org=(100, 350), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 255),thickness=3)
	else:
		if user_mark > computer_mark:
			cv2.putText(img=frame, text='User is winner!', org=(100, 300), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 255),thickness=3)
		else:
			cv2.putText(img=frame, text='Computer is winner!', org=(100, 300), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 255),thickness=3)

	if not game_over:
		cv2.putText(img=frame, text='Press "q" to quit', org=(100, 650), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=3)
	else:
		cv2.putText(img=frame, text='Press "q" to quit; "r" to replay', org=(100, 650), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0),thickness=3)

	if not game_over:
		counter = counter - 1;
		if counter<=0:
			counter = 50;
			winner = rps.get_winner(computer_choice, choice);
			if winner != "Draw":
				lastResult.append('Round #' + str(playing_round+1) + '> User:' + select_options[choice] + ' vs Com:' + select_options[computer_choice] + ' ----> Winner: ' + winner);
				playing_round = playing_round + 1;
				if winner == "User": 
					user_mark = user_mark + 1;
				elif winner == "Computer":
					computer_mark = computer_mark + 1;
			

	if winner == "Draw":
		cv2.putText(img=frame, text="Draw! replay...", org=(600, 420), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 100, 255),thickness=3)

	if len(lastResult)>=1:
		cv2.putText(img=frame, text=lastResult[0], org=(100, 480), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 100, 255),thickness=3)
	if len(lastResult)>=2:
		cv2.putText(img=frame, text=lastResult[1], org=(100, 520), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 100, 255),thickness=3)
	if len(lastResult)>=3:
		cv2.putText(img=frame, text=lastResult[2], org=(100, 560), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 100, 255),thickness=3)
		game_over = True;

	lastChoice = choice;
  
	# Display the resulting frame
	cv2.imshow('Computer Vision Rock-Paper-Scissors Game', frame)		


	# for calling when getting user input from camera
	#rps.play('R') 
	  
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	waitkey = cv2.waitKey(1);
	if waitkey & 0xFF == ord('q'):
		break
	if waitkey & 0xFF == ord('r') and game_over:
		game_over = False;
		counter = 50
		choice = "NIL"
		lastChoice = "NIL"
		winner = "";
		lastChoiceImage = None;
		lastResult = [];
		playing_round = 0;
		user_mark = 0
		computer_mark = 0
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()