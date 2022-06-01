import random
from PIL import Image, ImageOps
import numpy as np
import cv2
from camera_game_engine import GameScene

from gesture_detect import HandDetector


class PlayingScene(GameScene):

	def setup(self):
		self.__detector = HandDetector()

			
	def reset(self):
		self.__computer_choice = "";
		self.__user_choice = "";
		self.__countDownShowing = None;
		self.__totalUserWin = 0;
		self.__totalComWin = 0;
		self.__state = "WAIT";
		self.__round_who_win = None;
		self.__opponent = self.stage.getGameGlobalData("OPPENENT");
		self.stage.setCapture(True);


	def keyInToggle(self, key):
		if key & 0xFF == ord('q'):
			self.stage.jumpScene("LOSE")
		elif key & 0xFF == ord('p'):
			if self.__state=="WAIT" or (self.__state=="ROUND_RESULT" and self.__totalComWin<3 and self.__totalUserWin<3):
				if self.__state == "ROUND_RESULT":
					self.stage.delTimeout("AFTER_ROUND_RESULT")   # cancel timeout

				self.__user_choice = ""
				self.__state = "COUNTDOWN";
				self.stage.setTimeout(0, "SHOW3")
				self.stage.setTimeout(1, "SHOW2")
				self.stage.setTimeout(2, "SHOW1")
				self.stage.setTimeout(3, "SHOW0")
		elif key & 0xFF == ord('t'):			# trick to win
			self.__totalComWin = 0
			self.__totalUserWin = 2


	def timeoutCallback(self, name):
		#print("Timtout toggle! name=" + name);
		if name == "SHOW3" or name == "SHOW2" or name == "SHOW1" or name == "SHOW0":
			self.__countDownShowing = name;
		elif name == "AFTER_ROUND_RESULT":
			self.__state = "WAIT";

			# check if win 3 or lose 3
			if self.__totalComWin==3:
				self.stage.jumpScene("LOSE")
			elif self.__totalUserWin==3:
				self.stage.jumpScene("WIN")


	def update(self):
		self.elements = {}

		# always elements
		self.elements["BG"] = { "type":"jpg", "file":"./assets/images/opponent_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["BOX_YNAME_BG"] = { "type":"rect", "x":100, "y":50, "x2":300, "y2":100, "color":(50,50,50) }
		self.elements["BOX_YOU"] = { "type":"box", "x":100, "y":100, "w":480, "h":320, "thickness":3 }
		self.elements["NAME_YOU"] = {"type":"text","message":"You","x":165,"y":84,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2}
		self.elements["BOX_CNAME_BG"] = { "type":"rect", "x":980, "y":50, "x2":1180, "y2":100, "color":(50,50,50) }
		self.elements["BOX_COMP"] = { "type":"box", "x":700, "y":100, "w":480, "h":320, "thickness":3 }
		if self.__opponent is not None:
			if self.__opponent == "S":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_1.jpg", "x":700, "y":100, "w":480, "h":320}
			elif self.__opponent == "R":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_2.jpg", "x":700, "y":100, "w":480, "h":320}
			elif self.__opponent == "P":
				self.elements["O_PIC"] = { "type":"jpg", "file":"./assets/images/opponent_face_3.jpg", "x":700, "y":100, "w":480, "h":320}
		self.elements["NAME_COMP"] = {"type":"text","message":"Opponent","x":1000,"y":82,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":2}
		
		# Instruction text
		self.elements["TXT_INSTRUCTION"] = {"type":"text","message":"Who wins three rounds who wins this game","x":100,"y":570,"font":cv2.FONT_HERSHEY_SIMPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

		self.elements["Q_TO_QUIT"] = {"type":"text","message":"Press 'q' to abandon","x":100,"y":630,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

		if self.__totalUserWin>=1:
			self.elements["WIN_MARBLE_U1"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":140, "w":80, "h":80}
		if self.__totalUserWin>=2:
			self.elements["WIN_MARBLE_U2"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":240, "w":80, "h":80}
		if self.__totalUserWin>=3:
			self.elements["WIN_MARBLE_U3"] = { "type":"png","file":"./assets/images/marble.png", "x":10, "y":340, "w":80, "h":80}

		if self.__totalComWin>=1:
			self.elements["WIN_MARBLE_c1"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":140, "w":80, "h":80}
		if self.__totalComWin>=2:
			self.elements["WIN_MARBLE_C2"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":240, "w":80, "h":80}
		if self.__totalComWin>=3:
			self.elements["WIN_MARBLE_C3"] = { "type":"png","file":"./assets/images/marble.png", "x":1190, "y":340, "w":80, "h":80}

		if self.__state == "WAIT":
			# logic to update state
			self.__enable_gesture_detect()
			self.__update_state_wait()
		elif self.__state == "COUNTDOWN":
			# logic to update state
			self.__enable_gesture_detect()
			self.__computer_choice = self.__get_computer_choice()
			self.__update_state_count_down()
		elif self.__state == "ROUND_RESULT":
			self.__update_state_round_result()

	def afterRender(self):
		# handling when showing time is up
		if self.__countDownShowing == "SHOW0":		
			self.__countDownShowing = None;   

			# calculate point
			self.__set_winner(self.__computer_choice, self.__user_choice);

			# change to showing result state 
			self.__state = "ROUND_RESULT";	
			self.stage.setTimeout(3, "AFTER_ROUND_RESULT") 		# show the result for 3 second


	def __enable_gesture_detect(self):
		# logic to update state
		hand, res, dummy_x, dummy_y = self.__detector.chopHand(self.stage.originalFrame)
		self.__user_choice = self.__user_choice_by_gesture(res)
		self.stage.takeSnapshot()
		
	def __update_state_wait(self):
		self.elements["PIP"] = {"type":"pip", "x":100, "y":100, "w":480, "h":320}
		self.elements["P_TO_NEW_ROUND"] = {"type":"text", "message":"Press 'p' to start a new round", "x":100, "y":690, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2, "animate":"jump"}

		if self.__user_choice == "P":
			self.elements["USER_GESTURE"] = {"type":"text", "message":"Paper", "x":420, "y":400, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "R":
			self.elements["USER_GESTURE"] = {"type":"text", "message":"Rock", "x":420, "y":400, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "S":
			self.elements["USER_GESTURE"] = {"type":"text", "message":"Scissors", "x":420, "y":400, "font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}


	def __update_state_count_down(self):
		self.elements["TIMER"] = {"type":"text","message":"Timer","x":600,"y":35,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(100, 100, 255), "thickness":2}
		self.elements["COUNTDOWN"] = {"type":"text","message":self.__countDownShowing[-1:],"x":620,"y":130,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":3, "color":(0, 0, 0), "thickness":3, "animate":"jump"}
		self.elements["PIP"] = { "type":"pip", "x":100, "y":100, "w":480, "h":320 }

		if self.__user_choice == "P":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Paper","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "R":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Rock","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "S":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Scissors","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}

		if self.__computer_choice == "P":
			self.elements["COMP_PAPER"] = { "type":"jpg","file":"./assets/images/paper.jpg", "x":701, "y":100, "w":480, "h":320}
		elif self.__computer_choice == "R":
			self.elements["COMP_ROCK"] = { "type":"jpg","file":"./assets/images/rock.jpg", "x":701, "y":100, "w":480, "h":320}
		elif self.__computer_choice == "S":
			self.elements["COMP_SCISSORS"] = { "type":"jpg","file":"./assets/images/scissors.jpg", "x":701, "y":100, "w":480, "h":320}


	def __update_state_round_result(self):
		self.elements["PIP_SNAPSHOT"] = { "type":"snapshot", "x":100, "y":100, "w":480, "h":320 }
		self.elements["P_TO_NEW_ROUND"] = {"type":"text","message":"Press 'p' to start a new round","x":100,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2}
		
		if self.__computer_choice == "P":
			self.elements["COMP_PAPER"] = { "type":"jpg","file":"./assets/images/paper.jpg", "x":701, "y":100, "w":480, "h":320}
		elif self.__computer_choice == "R":
			self.elements["COMP_ROCK"] = { "type":"jpg","file":"./assets/images/rock.jpg", "x":701, "y":100, "w":480, "h":320}
		elif self.__computer_choice == "S":
			self.elements["COMP_SCISSORS"] = { "type":"jpg","file":"./assets/images/scissors.jpg", "x":701, "y":100, "w":480, "h":320}

		if self.__user_choice == "":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Unknown","x":400,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "P":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Paper","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "R":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Rock","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__user_choice == "S":
			self.elements["USER_GESTURE"] = {"type":"text","message":"Scissors","x":420,"y":400,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}

		if self.__round_who_win == "User":
			self.elements["BOX_YWIN_BG"] = { "type":"rect", "x":100, "y":101, "x2":300, "y2":151, "color":(80,80,80) }
			self.elements["BOX_CWIN_BG"] = { "type":"rect", "x":980, "y":101, "x2":1180, "y2":151, "color":(80,80,80) }
			self.elements["ROUND_YOU_WIN"] = {"type":"text","message":"Win","x":170,"y":143,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
			self.elements["ROUND_COMP_LOSE"] = {"type":"text","message":"Lose","x":1040,"y":143,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__round_who_win == "Computer":
			self.elements["BOX_YWIN_BG"] = { "type":"rect", "x":100, "y":101, "x2":300, "y2":151, "color":(80,80,80) }
			self.elements["BOX_CWIN_BG"] = { "type":"rect", "x":980, "y":101, "x2":1180, "y2":151, "color":(80,80,80) }
			self.elements["ROUND_YOU_LOSE"] = {"type":"text","message":"Lose","x":160,"y":143,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
			self.elements["ROUND_COMP_WIN"] = {"type":"text","message":"Win","x":1050,"y":143,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":1, "animate":"jump"}
		elif self.__round_who_win == "Tie":
			self.elements["ROUND_DRAW"] = {"type":"text","message":"Tie","x":620,"y":270,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(0, 0, 0), "thickness":2, "animate":"jump"}
	
	def __get_computer_choice(self):
		# randomly pick an option between "Rock", "Paper", and "Scissors" and return the choice.
		return ['R', 'P', 'S'][random.randint(0,2)];

	def __user_choice_by_gesture(self, gesture):
		# decode the value from the modal
		return {5:"P", 9:"S", 0:"R", 6:"R"}.get(gesture, "")

	def __set_winner(self, computer_choice, user_choice):
		self.__round_who_win = "User"
		if computer_choice == user_choice: 
			self.__round_who_win = 'Tie'
		elif user_choice=="" or (computer_choice == 'R' and user_choice == 'S') or (computer_choice == 'P' and user_choice == 'R') or (computer_choice == 'S' and user_choice == 'P'):
			self.__round_who_win = 'Computer'

		if self.__round_who_win == "User":
			self.__totalUserWin = self.__totalUserWin + 1;
		elif self.__round_who_win == "Computer":
			self.__totalComWin = self.__totalComWin + 1;




