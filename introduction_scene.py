from camera_game_engine import CameraGameScene
import cv2

class IntroductionScene(CameraGameScene):
	def setup(self):
		self.stage.setCapture(False);
			
	def reset(self):
		self.stage.setCapture(False);

	def keyInToggle(self, key):
		# logic to handle keyboard press 
		if key & 0xFF == ord('p'):
			self.jumpScene("OPPONENT")
		elif key & 0xFF == ord('q'):
			self.stage.quit()

	def update(self):
		self.elements["BG"] = { "type":"jpg","file":"./assets/images/intro_bg.jpg", "x":0, "y":0, "w":1280, "h":720}
		self.elements["KEY_FUNCTION"] = {"type":"text","message":"Press 'p' to play","x":30,"y":690,"font":cv2.FONT_HERSHEY_TRIPLEX, "size":1, "color":(255, 255, 255), "thickness":2, "animate":"jump"}
