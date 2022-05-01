import cv2
import random
from datetime import datetime, timedelta
import numpy as np
import time
from render import animate, showText, showLine, showBox, showJpeg, showPng
from render import showCaptureVideo, showSnapshot





class GameraGameEngine:
	def __init__(self, camera_id=0, title="Camera Game"):
		# Stage attributes
		self.camera_id = camera_id
		self.title = title
		self.terminateFlag = False

		self.timeoutList = [];
		
		self.scene = {}
		self.currentScene = None
		self.comingScene = None
		
		self.content = {}
		self.contentAnimationState = {}
		
		self.lastFrameTime = 0
		self.fps = 0

		self.stopCapture = False
		self.originalFrame = None
		self.snapshot = None

		self.globalData = {}

		self.setup()

		# define a video capture object
		self.vid = cv2.VideoCapture(camera_id)
		ret, self.frame = self.vid.read()

		while True:
			if self.terminateFlag:
				break;

			if self.stopCapture is False:
				# Capture the video frame by frame
				ret, self.frame = self.vid.read()

				# mirror the screen captured by webcam to have better user experience
				self.originalFrame = cv2.flip(self.frame, 1)
				self.frame = cv2.flip(self.frame, 1)		

			self.checkTimeout()
			self.update()
			self.render()
			self.afterRender()

			# get user input 
			waitkey = cv2.waitKey(1)
			self.keyIn(waitkey)

		# After the loop release the cap object
		self.vid.release()
		# Destroy all the windows
		cv2.destroyAllWindows()

	def setup(self):
		pass

	def update(self):
		if self.currentScene != None:
			# scene will overload update() for preparing elements 
			self.scene[self.currentScene].update();

			# scene will publish elements to stage
			self.scene[self.currentScene].commit();

	def render(self):
		#render add on content
		for key in self.content.keys():
			element = self.content[key];

			# simple animation
			x, y, w, h, a = animate(self, key, element); 		# go through animation engine

			if element["type"] == "text":
				showText(self, x, y, element["message"], element["font"], element["size"], element["color"], element["thickness"])
			elif element["type"] == "jpg":
				showJpeg(self, element['file'], x, y, w, h)
			elif element["type"] == "png":
				showPng(self, element['file'], x, y, w, h)
			elif element["type"] == "line":
				color = (0, 0, 0)		# default
				if "color" in element:
					color = element["color"]
				showLine(self, x, y, element["x2"], element["y2"], color, element["thickness"])
			elif element["type"] == "box":
				color = (0, 0, 0)		# default
				if "color" in element:
					color = element["color"]
				showBox(self, x, y, element["w"], element["h"], color, element["thickness"])
			elif element["type"] == "pip":
				showCaptureVideo(self, x, y, element["w"], element["h"])
			elif element["type"] == "snapshot":
				if self.snapshot is not None:
					showSnapshot(self, x, y, element["w"], element["h"])

		# calculate fps
		currentFrameTime = time.time()
		self.fps = 1 / (currentFrameTime - self.lastFrameTime)
		self.lastFrameTime = currentFrameTime
		#print(f"FPS:{int(self.fps)}")

		# Display the resulting frame
		cv2.imshow(self.title, self.frame)

	def afterRender(self):
		self.scene[self.currentScene].afterRender()

	def takeSnapshot(self):
		self.snapshot = self.originalFrame;

	def getSnapshot(self):
		return self.originalFrame

	def keyIn(self, k):
		if k != -1 and self.currentScene is not None:
			self.scene[self.currentScene].keyInToggle(k)

	def setTimeout(self, second, name):
		# calculate expiry datetime
		self.timeoutList.append([datetime.now() + timedelta(seconds=second), name])

	def delTimeout(self, name):
		for index in range(len(self.timeoutList)):
			if self.timeoutList[index][1] == name:
				self.timeoutList.pop(index)

	def checkTimeout(self):
		for index in range(len(self.timeoutList)):
			timeout = self.timeoutList[index];
			expiry = timeout[0]
			eventName = timeout[1]
			if datetime.now() >= expiry:
				self.timeoutList.pop(index)
				self.scene[self.currentScene].timeoutCallback(eventName)
				break;	# wait another frame to handle

	def initScene(self, name):
		if self.currentScene == None:
			self.currentScene = name;

	def registerScene(self, name, scene):
		if name in self.scene:
			return False;
		self.scene[name] = scene;

	def setNextScene(self, target):
		if self.comingScene!=None or target not in self.scene:
			return False;

		# cancel existing timeout before jump to next scene
		self.timeoutList = [];	

		# swap scene
		self.comingScene = target
		self.scene[self.comingScene].reset();
		self.currentScene = self.comingScene;
		self.comingScene = None;

	def setContent(self, elements):
		self.content = elements

	def quit(self):
		self.terminateFlag = True;

	def setCapture(self, isCap):
		self.stopCapture = not isCap



class CameraGameScene:
	def __init__(self, stage):
		self.stage = stage
		self.elements = {}
		self.setup();

	def commit(self):
		self.stage.setContent(self.elements)

	def jumpScene(self, targetScene):
		self.stage.setNextScene(targetScene)

	def setTimeout(self, second, name):
		# calculate expiry datetime
		self.stage.setTimeout(second, name)

	def delTimeout(self, name):
		self.stage.delTimeout(name)

	def setGameGlobalData(self, name, value):
		self.stage.globalData[name] = value

	def getGameGlobalData(self, name):
		if name not in self.stage.globalData:
			return None;
		return self.stage.globalData[name]

	def setup(self):
		pass

	def reset(self):
		pass

	def update(self):
		pass

	def afterRender(self):
		pass

	def keyInToggle(self, key):
		pass

	def timeoutCallback(self):
		pass
