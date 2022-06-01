from camera_game_engine import GameScene
import cv2

class PrizeScene(GameScene):
	def setup(self):
		self.elements["BG"] = { "type":"jpg","file":"./assets/images/prize_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text","message":"Press 'c' to continue.","x":30,"y":660,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
			
	def reset(self):
		self.stage.setCapture(False)

	def keyInToggle(self, key):
		if key & 0xFF == ord('c'):
			self.stage.jumpScene("INTRO")
