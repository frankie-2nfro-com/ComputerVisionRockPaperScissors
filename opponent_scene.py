from camera_game_engine import CameraGameScene
import cv2
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

class OpponentScene(CameraGameScene):
	def setup(self):
		# Load the model
		self.model = load_model('keras_model.h5')

		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
		self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

		self.reset();
			
	def reset(self):
		self.user_choice = "NIL";
		self.stage.setCapture(True);

	def keyInToggle(self, key):
		# logic to handle keyboard press 
		if key & 0xFF == ord('p'):
			self.setGameGlobalData("OPPENENT", self.user_choice)
			self.jumpScene("PLAYING")
		elif key & 0xFF == ord('q'):
			self.jumpScene("INTRO")

	def update(self):
		self.user_choice = self.userChoiceByGesture()

		self.elements["BG"] = { "type":"jpg", "file":"./assets/images/opponent_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text", "message":"Press 'p' to play; 'q' to go back","x":30,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}

		if self.user_choice == 'S':
			o1_color = (0, 200, 0)
			self.elements["O1"] = { "type":"jpg", "file":"./assets/images/opponent_1.jpg", "x":75, "y":20, "w":340, "h":520}
			self.elements["O1_BOX"] = { "type":"box", "x":75, "y":20, "w":340, "h":520, "color": o1_color, "thickness":3 }
		else:
			o1_color = (0, 0, 0)
			self.elements["O1"] = { "type":"jpg", "file":"./assets/images/opponent_1.jpg", "x":95, "y":40, "w":300, "h":480}
			self.elements["O1_BOX"] = { "type":"box",  "x":95, "y":40, "w":300, "h":480, "color": o1_color, "thickness":3 }

		if self.user_choice == 'R':
			o2_color = (0, 200, 0)
			self.elements["O2"] = { "type":"jpg", "file":"./assets/images/opponent_2.jpg", "x":470, "y":20, "w":340, "h":520}
			self.elements["O2_BOX"] = { "type":"box",  "x":470, "y":20, "w":340, "h":520, "color": o2_color, "thickness":3 }
		else:
			o2_color = (0, 0, 0)
			self.elements["O2"] = { "type":"jpg", "file":"./assets/images/opponent_2.jpg", "x":490, "y":40, "w":300, "h":480}
			self.elements["O2_BOX"] = { "type":"box",  "x":490, "y":40, "w":300, "h":480, "color": o2_color, "thickness":3 }

		if self.user_choice == 'P':
			o3_color = (0, 200, 0)
			self.elements["O3"] = { "type":"jpg", "file":"./assets/images/opponent_3.jpg", "x":865, "y":20, "w":340, "h":520}
			self.elements["O3_BOX"] = { "type":"box",  "x":865, "y":20, "w":340, "h":520, "color": o3_color, "thickness":3 }
		else:
			o3_color = (0, 0, 0)
			self.elements["O3"] = { "type":"jpg", "file":"./assets/images/opponent_3.jpg", "x":885, "y":40, "w":300, "h":480}
			self.elements["O3_BOX"] = { "type":"box",  "x":885, "y":40, "w":300, "h":480, "color": o3_color, "thickness":3 }

		self.elements["PIP"] = { "type":"pip", "x":1020, "y":540, "w":240, "h":160 }
		self.elements["PIP_BOX"] = { "type":"box",  "x":1020, "y":540, "w":240, "h":160, "color": (0,0,0), "thickness":3 }

		self.elements["CHOOSE_OPPONENT"] = {"type":"text","message":"Choosing an opponent","x":440,"y":600,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

	def userChoiceByGesture(self):
		# convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that 
		# the color is converted from BGR to RGB
		color_coverted = cv2.cvtColor(self.stage.frame, cv2.COLOR_BGR2RGB)
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
