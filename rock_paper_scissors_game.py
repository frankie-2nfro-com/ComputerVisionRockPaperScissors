import random
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
from camera_game_engine import GameraGameEngine

class RockPaperScissorsGame(GameraGameEngine):
	def __init__(self, camera_id=0):
		# this game attributes
		self.addContent = False;
		self.computer_choice = "NIL";
		self.user_choice = "NIL";
		
		self.countDownShowing = None;

		# Load the model
		self.model = load_model('keras_model.h5')

		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
		self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

		self.select_options = {"R":"Rock", "P":"Paper", "S":"Scissors", "NIL":"Nil"};

		GameraGameEngine.__init__(self, camera_id, 'Computer Vision Rock-Paper-Scissors')

	def keyInToggle(self):
		# logic to handle keyboard press 
		if self.detectKey & 0xFF == ord('q'):
			self.terminateFlag = True;
		elif self.detectKey & 0xFF == ord('a'):
			self.setTimeout(10, "TRY_COUNT_DOWN0")
			self.addContent = True;
		elif self.detectKey & 0xFF == ord('d'):
			self.addContent = False;
			self.setTimeout(0, "SHOW3")
			self.setTimeout(1, "SHOW2")
			self.setTimeout(2, "SHOW1")
			self.setTimeout(3, "SHOW0")

	def update(self):
		# game logic update the content dictionary by state of the game
		self.user_choice = self.userChoiceByGesture()
		if self.user_choice != None and self.countDownShowing!=None:
			self.content["USER_CHOICE"] = {"type":"text","message":"User is " + self.select_options[self.user_choice],"x":100,"y":100,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(200, 100, 255), "thickness":3, "animate":"shake"}
		else:
			if "USER_CHOICE" in self.content:
				del self.content["USER_CHOICE"]

		self.computer_choice = self.get_computer_choice()
		if self.computer_choice != None and self.countDownShowing!=None:
			self.content["COMP_CHOICE"] = {"type":"text","message":"Computer is " + self.select_options[self.computer_choice],"x":100,"y":200,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":3, "animate":"jump"}
		else:
			if "COMP_CHOICE" in self.content:
				del self.content["COMP_CHOICE"]

		if self.addContent:
			self.content["k"] = {"type":"text","message":"dddddd","x":100,"y":100,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":3}
		else:
			if "k" in self.content:
				del self.content["k"]

		if self.countDownShowing!=None:
			self.content["COUNTDOWN"] = {"type":"text","message":self.countDownShowing[-1:],"x":360,"y":360,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":5, "color":(100, 100, 255), "thickness":3, "animate":"jump"}
		else:
			if "COUNTDOWN" in self.content:
				del self.content["COUNTDOWN"]

		self.content["Q_TO_QUIT"] = {"type":"text","message":"Press 'q' to quit","x":100,"y":650,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

	def afterRender(self):
		if self.countDownShowing == "SHOW0":
			self.countDownShowing = None;

	# Will randomly pick an option between "Rock", "Paper", and "Scissors" and return the choice.
	def get_computer_choice(self):
		return ['R', 'P', 'S'][random.randint(0,2)];

	def userChoiceByGesture(self):
		# convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that 
		# the color is converted from BGR to RGB
		color_coverted = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
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
		self.data[0] = normalized_image_array

		# run the inference
		prediction = self.model.predict(self.data)

		pPos = prediction[0][0]
		sPos = prediction[0][1]
		rPos = prediction[0][2]

		# logic to determine the result
		choice = self.user_choice;
		if sPos > 0.5:		# and sPos > rPos
			choice = "S"
		elif rPos > 0.7 and rPos > pPos and rPos > sPos:
			choice = "R"
		elif pPos > 0.7 and pPos > rPos and pPos > sPos:
			choice = "P"

		return choice;

	def timeoutCallback(self, name):
		print("Timtout toggle! name=" + name);
		if name == "SHOW3" or name == "SHOW2" or name == "SHOW1" or name == "SHOW0":
			self.countDownShowing = name;
		elif name == "TRY_COUNT_DOWN0":
			self.addContent = False;


ge = RockPaperScissorsGame(0)