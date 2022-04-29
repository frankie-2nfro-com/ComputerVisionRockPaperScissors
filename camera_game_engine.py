import cv2
import random
from datetime import datetime, timedelta

class GameraGameEngine:
	def __init__(self, camera_id=0, title="Camera Game"):
		self.camera_id = camera_id
		self.title = title

		self.content = {}
		self.contentAnimationState = {}
		self.detectKey = None;
		self.terminateFlag = False;

		self.timeoutList = [];

		# define a video capture object
		self.vid = cv2.VideoCapture(camera_id)

		while True:
			# Capture the video frame by frame
			ret, self.frame = self.vid.read()
			if ret:
				self.checkTimeout()
				self.update()
				self.render()
				self.afterRender()

			waitkey = cv2.waitKey(1)
			self.keyIn(waitkey)

			if self.terminateFlag:
				break;

		# After the loop release the cap object
		self.vid.release()
		# Destroy all the windows
		cv2.destroyAllWindows()

	def update(self):
		pass

	def render(self):
		#render add on content apart from the camera capture picture
		for key in self.content.keys():
			elements = self.content[key];

			# simple animation
			x = elements["x"]
			y = elements["y"]
			if "animate" in elements:
				if elements["animate"]=="shake":
					x = x + random.randint(-5,5)
					y = y + random.randint(-5,5)
				elif elements["animate"]=="jump":
					val = 0;
					if key in self.contentAnimationState: 
						val = self.contentAnimationState[key]["yDelta"];
						if val == 0: 
							val = -10
						else:
							val = 0;
					y = y + val;
					self.contentAnimationState[key] = {"yDelta": val}
				
			if elements["type"] == "text":
				cv2.putText(img=self.frame, text=elements["message"], org=(x, y), fontFace=elements["font"], fontScale=elements["size"], color=elements["color"],thickness=elements["thickness"])
					

		# Display the resulting frame
		cv2.imshow(self.title, self.frame)

	def afterRender(self):
		pass

	def keyIn(self, k):
		if k != -1:
			self.detectKey = k;
			self.keyInToggle()

	def keyInToggle(self):
		pass

	def setTimeout(self, second, name):
		# calculate expiry datetime
		self.timeoutList.append([datetime.now() + timedelta(seconds=second), name])

	def checkTimeout(self):
		for index in range(len(self.timeoutList)):
			timeout = self.timeoutList[index];
			expiry = timeout[0]
			eventName = timeout[1]
			if datetime.now() >= expiry:
				self.timeoutList.pop(index)
				self.timeoutCallback(eventName)
				break;	# wait another frame to handle

	def timeoutCallback(self):
		pass









