import random
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
from camera_game_engine import CameraGameScene


class PlayingScene(CameraGameScene):

	def setup(self):
		# Load the model
		self.model = load_model('keras_model.h5')

		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
		self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

		self.reset();

			
	def reset(self):
		self.addContent = False;
		self.computer_choice = "NIL";
		self.user_choice = "NIL";
		self.countDownShowing = None;
		self.totalUserWin = 0;
		self.totalComWin = 0;
		self.state = "WAIT";
		self.round_who_win = None;
		self.lastUserSnapshot = None;
		self.stage.setCapture(True);
		self.opponent = self.getGameGlobalData("OPPENENT");


	def keyInToggle(self, key):
		# logic to handle keyboard press 
		if key & 0xFF == ord('q'):
			self.jumpScene("LOSE")
		elif key & 0xFF == ord('p'):
			if self.state == "WAIT" or self.state == "ROUND_RESULT":
				if self.state == "ROUND_RESULT":
					self.delTimeout("AFTER_ROUND_RESULT")   # cancel timeout

				self.state = "COUNTDOWN";
				self.addContent = False;
				self.setTimeout(0, "SHOW3")
				self.setTimeout(1, "SHOW2")
				self.setTimeout(2, "SHOW1")
				self.setTimeout(3, "SHOW0")

	def timeoutCallback(self, name):
		print("Timtout toggle! name=" + name);
		if name == "SHOW3" or name == "SHOW2" or name == "SHOW1" or name == "SHOW0":
			self.countDownShowing = name;
		elif name == "AFTER_ROUND_RESULT":
			self.state = "WAIT";




	def update(self):
		self.elements = {}

		# always elements
		self.elements["BOX_YOU"] = { "type":"box", "x":100, "y":100, "w":480, "h":320, "thickness":3 }
		self.elements["NAME_YOU"] = {"type":"text","message":"You","x":300,"y":75,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":2}

		self.elements["BOX_COMP"] = { "type":"box", "x":700, "y":100, "w":480, "h":320, "thickness":3 }
		if self.opponent is not None:
			if self.opponent == "S":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_1.jpg", "x":700, "y":100, "w":480, "h":320}
			elif self.opponent == "R":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_2.jpg", "x":700, "y":100, "w":480, "h":320}
			elif self.opponent == "P":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_3.jpg", "x":700, "y":100, "w":480, "h":320}
		self.elements["NAME_COMP"] = {"type":"text","message":"Opponent","x":860,"y":75,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":2}
		
		# Instruction
		self.elements["BOX_INSTRUCTION"] = { "type":"box", "x":100, "y":500, "w":1080, "h":80, "color":(255,255,255), "thickness":3 }
		self.elements["TXT_INSTRUCTION"] = {"type":"text","message":"Who wins three rounds firstly who wins this game","x":140,"y":550,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1}

		self.elements["Q_TO_QUIT"] = {"type":"text","message":"Press 'q' to abandon","x":100,"y":630,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

		if self.totalUserWin>=1:
			self.elements["WIN_MARBLE_U1"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":140, "w":80, "h":80}
		if self.totalUserWin>=2:
			self.elements["WIN_MARBLE_U2"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":240, "w":80, "h":80}
		if self.totalUserWin>=3:
			self.elements["WIN_MARBLE_U3"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":340, "w":80, "h":80}

		if self.totalComWin>=1:
			self.elements["WIN_MARBLE_c1"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":140, "w":80, "h":80}
		if self.totalComWin>=2:
			self.elements["WIN_MARBLE_C2"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":240, "w":80, "h":80}
		if self.totalComWin>=3:
			self.elements["WIN_MARBLE_C3"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":340, "w":80, "h":80}


		if self.state == "WAIT":
			self.updateStateWait()
		elif self.state == "COUNTDOWN":
			# logic to update state
			self.user_choice = self.userChoiceByGesture()
			self.stage.takeSnapshot()
			self.computer_choice = self.get_computer_choice()
			self.updateStateCountDown()
		elif self.state == "ROUND_RESULT":
			self.updateStateRoundResult()
		

	def updateStateWait(self):
		self.elements["PIP"] = { "type":"pip", "x":100, "y":100, "w":480, "h":320 }
		self.elements["S_TO_NEW_ROUND"] = {"type":"text","message":"Press 'p' to start a new round","x":100,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2, "animate": "jump"}

	def updateStateCountDown(self):
		self.elements["TIMER"] = {"type":"text","message":"Timer","x":600,"y":35,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":2}
		self.elements["COUNTDOWN"] = {"type":"text","message":self.countDownShowing[-1:],"x":620,"y":130,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":3, "color":(255, 255, 255), "thickness":3, "animate":"jump"}
		if self.user_choice == "P":
			self.elements["USER_PAPER"] = { "type":"jpg","file":"./assets/images/paper.jpg", "x":101, "y":100, "w":480, "h":320}
		if self.user_choice == "R":
			self.elements["USER_ROCK"] = { "type":"jpg","file":"./assets/images/rock.jpg", "x":101, "y":100, "w":480, "h":320}
		if self.user_choice == "S":
			self.elements["USER_SCISSORS"] = { "type":"jpg","file":"./assets/images/scissors.jpg", "x":101, "y":100, "w":480, "h":320}
		if self.computer_choice == "P":
			self.elements["COMP_PAPER"] = { "type":"jpg","file":"./assets/images/paper.jpg", "x":701, "y":100, "w":480, "h":320}
		if self.computer_choice == "R":
			self.elements["COMP_ROCK"] = { "type":"jpg","file":"./assets/images/rock.jpg", "x":701, "y":100, "w":480, "h":320}
		if self.computer_choice == "S":
			self.elements["COMP_SCISSORS"] = { "type":"jpg","file":"./assets/images/scissors.jpg", "x":701, "y":100, "w":480, "h":320}

	def updateStateRoundResult(self):
		self.elements["PIP_SNAPSHOT"] = { "type":"snapshot", "x":100, "y":100, "w":480, "h":320 }
		self.elements["S_TO_NEW_ROUND"] = {"type":"text","message":"Press 's' to start a new round","x":100,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}
		if self.round_who_win == "User":
			self.elements["ROUND_YOU_WIN"] = {"type":"text","message":"You win","x":120,"y":460,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.round_who_win == "Computer":
			self.elements["ROUND_COMP_WIN"] = {"type":"text","message":"Computer win","x":720,"y":460,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.round_who_win == "Draw":
			self.elements["ROUND_DRAW"] = {"type":"text","message":"Draw","x":600,"y":460,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}

		#if self.user_choice == "P":
		#	self.elements["USER_PAPER"] = { "type":"jpg","file":"paper.jpg", "x":101, "y":100, "w":480, "h":320}
		#if self.user_choice == "R":
		#	self.elements["USER_ROCK"] = { "type":"jpg","file":"rock.jpg", "x":101, "y":100, "w":480, "h":320}
		#if self.user_choice == "S":
		#	self.elements["USER_SCISSORS"] = { "type":"jpg","file":"scissors.jpg", "x":101, "y":100, "w":480, "h":320}
		if self.computer_choice == "P":
			self.elements["COMP_PAPER"] = { "type":"jpg","file":"./assets/images/paper.jpg", "x":701, "y":100, "w":480, "h":320}
		if self.computer_choice == "R":
			self.elements["COMP_ROCK"] = { "type":"jpg","file":"./assets/images/rock.jpg", "x":701, "y":100, "w":480, "h":320}
		if self.computer_choice == "S":
			self.elements["COMP_SCISSORS"] = { "type":"jpg","file":"./assets/images/scissors.jpg", "x":701, "y":100, "w":480, "h":320}




	def afterRender(self):
		# handling when showing time is up
		if self.countDownShowing == "SHOW0":		
			self.countDownShowing = None;   

			# change to showing result state 
			self.state = "ROUND_RESULT";	
			self.setTimeout(3, "AFTER_ROUND_RESULT") 
			
			# calculate point
			self.round_who_win = self.getWinner(self.computer_choice, self.user_choice);
			if self.round_who_win == "User":
				self.totalUserWin = self.totalUserWin + 1;
			elif self.round_who_win == "Computer":
				self.totalComWin = self.totalComWin + 1;

			"""
			print("This round-> YOU:" + self.user_choice + " COM:" + self.computer_choice);
			if self.round_who_win == "User":
				print("You WIN")
			elif self.round_who_win == "Computer":
				print("Computer WIN");
			else:
				print("DRAW");
			"""

			# check if win 3 or lose 3
			if self.totalComWin==3:
				self.jumpScene("LOSE")
			elif self.totalUserWin==3:
				self.jumpScene("WIN")




	# Will randomly pick an option between "Rock", "Paper", and "Scissors" and return the choice.
	def get_computer_choice(self):
		return ['R', 'P', 'S'][random.randint(0,2)];

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

	def getWinner(self, computer_choice, user_choice):
		if computer_choice == user_choice: 
			return 'Draw';
		if (computer_choice == 'R' and user_choice == 'S') or (computer_choice == 'P' and user_choice == 'R') or (computer_choice == 'S' and user_choice == 'P'):
			return 'Computer';
		return 'User';




