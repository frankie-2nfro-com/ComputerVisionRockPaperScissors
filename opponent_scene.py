from camera_game_engine import GameScene
import cv2

from gesture_detect import HandDetector

class OpponentScene(GameScene):
	def setup(self):
		self.__detector = HandDetector()
			

	def reset(self):
		self.__user_choice = "";
		self.stage.setCapture(True);
		

	def keyInToggle(self, key):
		if key & 0xFF == ord('p'):
			if self.__user_choice!="":
				self.stage.setGameGlobalData("OPPENENT", self.__user_choice)
				self.stage.jumpScene("PLAYING")
		elif key & 0xFF == ord('q'):
			self.stage.jumpScene("INTRO")


	def update(self):
		self.elements = {}

		hand, res, dummy_x, dummy_y = self.__detector.chopHand(self.stage.originalFrame)
		if self.__userChoiceByGesture(res)!="":
			self.__user_choice = self.__userChoiceByGesture(res)

		self.elements["BG"] = { "type":"jpg", "file":"./assets/images/opponent_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["CHOOSE_OPPONENT"] = {"type":"text","message":"Choosing your opponent by gesture","x":340,"y":600,"font":cv2.FONT_HERSHEY_SIMPLEX, "size":1, "color":(0, 0, 0), "thickness":2}

		if self.__user_choice!="":
			self.elements["KEY_FUNCTION"] = {"type":"text", "message":"Press 'p' to play; 'q' to go back","x":30,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
		else:
			self.elements["KEY_FUNCTION"] = {"type":"text", "message":"Press 'q' to go back","x":30,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
		
		if self.__user_choice == 'S':
			self.elements["O1"] = { "type":"jpg", "file":"./assets/images/opponent_1.jpg", "x":75, "y":20, "w":340, "h":520}
			self.elements["O1_BOX"] = { "type":"box", "x":75, "y":20, "w":340, "h":520, "color": (0, 200, 0), "thickness":3 }
		else:
			self.elements["O1"] = { "type":"jpg", "file":"./assets/images/opponent_1.jpg", "x":95, "y":40, "w":300, "h":480}
			self.elements["O1_BOX"] = { "type":"box",  "x":95, "y":40, "w":300, "h":480, "color": (0, 0, 0), "thickness":3 }

		if self.__user_choice == 'R':
			self.elements["O2"] = { "type":"jpg", "file":"./assets/images/opponent_2.jpg", "x":470, "y":20, "w":340, "h":520}
			self.elements["O2_BOX"] = { "type":"box",  "x":470, "y":20, "w":340, "h":520, "color": (0, 200, 0), "thickness":3 }
		else:
			self.elements["O2"] = { "type":"jpg", "file":"./assets/images/opponent_2.jpg", "x":490, "y":40, "w":300, "h":480}
			self.elements["O2_BOX"] = { "type":"box",  "x":490, "y":40, "w":300, "h":480, "color": (0, 0, 0), "thickness":3 }

		if self.__user_choice == 'P':
			self.elements["O3"] = { "type":"jpg", "file":"./assets/images/opponent_3.jpg", "x":865, "y":20, "w":340, "h":520}
			self.elements["O3_BOX"] = { "type":"box",  "x":865, "y":20, "w":340, "h":520, "color": (0, 200, 0), "thickness":3 }
		else:
			self.elements["O3"] = { "type":"jpg", "file":"./assets/images/opponent_3.jpg", "x":885, "y":40, "w":300, "h":480}
			self.elements["O3_BOX"] = { "type":"box",  "x":885, "y":40, "w":300, "h":480, "color": (0, 0, 0), "thickness":3 }

		if hand is not None and self.__user_choice!="":
			hh, hw, hc = hand.shape
			if hh>0 and hw>0:
				self.elements["PIP_BOX"] = { "type":"box",  "x":1100, "y":550, "w":160, "h":160, "color": (0,0,0), "thickness":3 }
				hand = cv2.resize(hand, (160,160), interpolation = cv2.INTER_AREA)
				self.elements["GESTURE"] = { "type":"mimage",  "x":1100, "y":550, "fimg":hand, "timg":self.stage.frame }


	def __userChoiceByGesture(self, gesture):
		# decode the value from the modal
		return {5:"P", 9:"S", 0:"R", 6:"R"}.get(gesture, "")