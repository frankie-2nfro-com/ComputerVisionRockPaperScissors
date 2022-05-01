from camera_game_engine import CameraGameScene
import cv2

class WinScene(CameraGameScene):
	def setup(self):
		self.stage.setCapture(False);
			
	def reset(self):
		self.stage.setCapture(False);

	def keyInToggle(self, key):
		# logic to handle keyboard press 
		if key & 0xFF == ord('c'):
			self.jumpScene("INTRO")

	def update(self):
		self.elements["BG"] = { "type":"jpg","file":"./assets/images/win_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text","message":"Press 'c' to continue.","x":30,"y":660,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
		self.elements["WIN_MSG"] = {"type":"text","message":"You Win","x":380,"y":260,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":4, "color":(0, 0, 0), "thickness":4}
