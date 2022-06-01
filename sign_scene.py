from camera_game_engine import GameScene
import cv2
import numpy as np
from gesture_detect import HandDetector

class SignScene(GameScene):
	def setup(self):
		self.__detector = HandDetector()
		self.__last_x = -1
		self.__last_y = -1
		self.elements["PRIZE"] = {"type":"text","message":"You win $184,231,897,232","x":30,"y":80,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":2, "color":(255, 255, 255), "thickness":1, "animate":"shake"}
		self.elements["KEY_FUNCTION"] = {"type":"text","message":"Press 'c' to continue.","x":30,"y":660,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
		self.elements["BOX_SIGN"] = { "type":"box", "x":160, "y":120, "w":880, "h":420, "thickness":3 }
		self.elements["SIGN_INSTRUCTION"] = {"type":"text","message":"Use pointer finger to sign for confirmation","x":260,"y":570,"font":cv2.FONT_HERSHEY_SIMPLEX, "size":1, "color":(255, 255, 255), "thickness":1}
			
	def reset(self):
		# erase drawing 
		h, w, c = self.stage.frame.shape
		self.__canvas = np.zeros((h, w, 3), np.uint8)
		
		self.stage.setCapture(True);

	def keyInToggle(self, key):
		if key & 0xFF == ord('c'):
			self.stage.jumpScene("PRIZE")

	def update(self):
		hand, res, self.__last_x, self.__last_y = self.__detector.chopHand(self.stage.frame, self.__canvas, True, self.__last_x, self.__last_y)
		self.stage.frame = cv2.addWeighted(self.stage.frame, 1, self.__canvas, 1, 0)

		#if hand is None:
		#	h, w, c = self.stage.frame.shape
		#	self.__canvas = np.zeros((h, w, 3), np.uint8)
