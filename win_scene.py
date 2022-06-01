from camera_game_engine import GameScene
import cv2

class WinScene(GameScene):
	def setup(self):
		self.elements["BG"] = { "type":"jpg","file":"./assets/images/win_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text","message":"Press 'c' to continue","x":30,"y":660,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
		self.elements["WIN_MSG"] = {"type":"text","message":"Congratulations","x":130,"y":95,"font":cv2.FONT_HERSHEY_SIMPLEX, "size":4, "color":(255, 255, 255), "thickness":3}
			
	def reset(self):
		self.stage.setCapture(False)

	def keyInToggle(self, key):
		if key & 0xFF == ord('c'):
			self.stage.jumpScene("SIGN")
