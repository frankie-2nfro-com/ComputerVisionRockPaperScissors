import cv2
from datetime import datetime, timedelta
from render import showPng
from render import showTextByThread, showLineByThread, showBoxByThread, showJpegByThread 
from render import showRectangleByThread, showCaptureVideoByThread, showSnapshotByThread
import numpy as np
import random



class CameraGameEngine:
	def __init__(self, title="Camera Game", camera_id=0):
		# attributes
		self.camera_id = camera_id
		self.title = title
		self.currentScene = None
		self.comingScene = None
		self.frame = None 				# display frame
		self.originalFrame = None		# original captured image
		self.snapshot = None			# store frame of a moment  
		#self.interfaceFrame = None
		#self.lastFrameTime = 0			# for calculate frame per second
		#self.fps = 0					# current fps

		self.__stopCapture = False
		self.__terminateFlag = False
		self.__timeoutList = []
		self.__globalData = {}
		self.__scene = {}
		self.__content = {}
		self.__contentAnimationState = {}

		# define a video capture object
		self.vid = cv2.VideoCapture(self.camera_id)

		# first capture to get the self.frame for other function setup
		success, img = self.vid.read()
		assert success, "Webcam cannot return image properly. Please check the device."

		self.frame = cv2.flip(img, 1)

		# create interface layer, actually static interface should print on here to reduce rendering work load
		#h, w, c = self.frame.shape
		#self.interfaceFrame = np.zeros((h, w, 3), dtype=np.uint8)

		self.__main()


	def __main(self):
		# life cycle of camera game
		self.setup()

		while True:
			if self.__terminateFlag:
				break

			if self.__stopCapture is False:
				# Capture the video frame by frame
				success, img = self.vid.read()
				if not success:			# skip error frame
					continue  
				self.frame = cv2.flip(img, 1)				# mirror the screen. 
				self.originalFrame = cv2.flip(img, 1)		# mirror the screen. 
				self.originalFrame.flags.writeable = False

			self.__checkTimeout()
			self.__update()
			self.__render()
			self.__afterRender()

			# get user input 
			self.keyIn(cv2.waitKey(1))

		# After the loop release the cap object
		self.vid.release()
		# Destroy all the windows
		cv2.destroyAllWindows()


	def setup(self):
		pass


	def __update(self):
		if self.currentScene != None:
			# scene will overload update() for preparing elements 
			self.__scene[self.currentScene].update()

			# scene will publish elements to stage
			self.__setContent(self.__scene[self.currentScene].elements)


	def __render(self):
		#render add on content
		for key in self.__content.keys():
			element = self.__content[key]

			# simple animation
			x, y, w, h, a = self.__animate(key, element)		# go through animation engine

			if element["type"] == "text":
				#showText(self.frame, x, y, element["message"], element["font"], element["size"], element["color"], element["thickness"])
				showTextByThread(self.frame, x, y, element["message"], element["font"], element["size"], element["color"], element["thickness"]).join()
			elif element["type"] == "jpg":
				#showJpeg(self.frame, element['file'], x, y, w, h)
				showJpegByThread(self.frame, element['file'], x, y, w, h).join()
			elif element["type"] == "png":
				self.frame = showPng(self.frame, element['file'], x, y, w, h)	# self.frame is pass by value, so need to return the merged image
			elif element["type"] == "line":
				#showLine(self.frame, x, y, element["x2"], element["y2"], color, element["thickness"])
				showLineByThread(self.frame, x, y, element["x2"], element["y2"], element.get("color", (0,0,0)), element.get("thickness", 1)).join()
			elif element["type"] == "box":
				#showBox(self.frame, x, y, element["w"], element["h"], color, element["thickness"])
				showBoxByThread(self.frame, x, y, element["w"], element["h"], element.get("color", (0,0,0)), element.get("thickness", 1)).join()
			elif element["type"] == "rect":
				#showRectangle(self.frame, x, y, element["x2"], element["y2"], color, element["thickness"])
				showRectangleByThread(self.frame, x, y, element["x2"], element["y2"], element.get("color", (0,0,0))).join()
			elif element["type"] == "pip":
				#showCaptureVideo(self, x, y, element["w"], element["h"])
				showCaptureVideoByThread(self, x, y, element["w"], element["h"]).join()
			elif element["type"] == "snapshot":
				if self.snapshot is not None:
					#showSnapshot(self, x, y, element["w"], element["h"])
					showSnapshotByThread(self, x, y, element["w"], element["h"]).join()
			elif element["type"] == "mimage":

				memory_image = element["fimg"]
				to_image = element["timg"]
				hh, hw, hc = memory_image.shape
				h, w, c = to_image.shape
				if hh>0 and hw>0 and h>0 and w>0:
					hx = element["x"]
					hy = element["y"]
					to_image[hy:hy+hh, hx:hx+hw] = memory_image

		# calculate fps
		#currentFrameTime = time.time()
		#self.fps = 1 / (currentFrameTime - self.lastFrameTime)
		#self.lastFrameTime = currentFrameTime
		#print(f"FPS:{int(self.fps)}")

		# interface interface always on top
		#self.frame = cv2.bitwise_and(self.frame, self.interfaceFrame)	
		#self.frame = cv2.addWeighted(self.frame, 1, self.interfaceFrame, 1, 0)
		#showLine(self.interfaceFrame, 0, 0, 1000, 100, (0,255,0), 3)			# test layer

		# Display the resulting frame
		cv2.imshow(self.title, self.frame)

	def __afterRender(self):
		self.__scene[self.currentScene].afterRender()

	def takeSnapshot(self):
		self.snapshot = self.originalFrame

	#def getInterfaceImage(self):
	#	return self.interfaceFrame

	def keyIn(self, k):
		if k != -1 and self.currentScene is not None:
			self.__scene[self.currentScene].keyInToggle(k)

	def setTimeout(self, second, name):
		# calculate expiry datetime
		self.__timeoutList.append([datetime.now() + timedelta(seconds=second), name])

	def delTimeout(self, name):
		if name is None:
			self.__timeoutList = []
		else:
			for index in range(len(self.__timeoutList)):
				if self.__timeoutList[index][1] == name:
					self.__timeoutList.pop(index)

	def __checkTimeout(self):
		for index in range(len(self.__timeoutList)):
			timeout = self.__timeoutList[index]
			expiry = timeout[0]
			eventName = timeout[1]
			if datetime.now() >= expiry:
				self.__timeoutList.pop(index)
				self.__scene[self.currentScene].timeoutCallback(eventName)
				break	# wait another frame to handle

	def initScene(self, name):
		if self.currentScene == None:
			self.__setNextScene(name)

	def registerScene(self, name, scene):
		if name not in self.__scene:	
			self.__scene[name] = scene

	def __setNextScene(self, target):
		if self.comingScene!=None or target not in self.__scene:
			return

		# cancel existing timeout before jump to next scene
		self.delTimeout(None)	

		# clean up interface frame
		#h, w, c = self.frame.shape
		#self.interfaceFrame = np.zeros((h, w, 3), dtype=np.uint8)

		# swap scene
		self.comingScene = target
		self.__scene[self.comingScene].reset()
		self.currentScene = self.comingScene
		self.comingScene = None

	def __setContent(self, elements):
		self.__content = elements

	def quit(self):
		self.__terminateFlag = True

	def setCapture(self, isCap):
		self.__stopCapture = not isCap

	def setGameGlobalData(self, name, value):
		self.__globalData[name] = value

	def getGameGlobalData(self, name):
		if name not in self.__globalData:
			return None
		return self.__globalData[name]

	def jumpScene(self, targetScene):
		self.__setNextScene(targetScene)

	# Simple Animation Engine
	def __animate(self, name, element):
		x = element.get("x", 0)
		y = element.get("y", 0)
		width = element.get("w", 0)
		height = element.get("h", 0)
		alpha = element.get("alpha", 1)

		if "animate" in element:
			if element["animate"]=="shake":
				x = x + random.randint(-5,5)
				y = y + random.randint(-5,5)
			elif element["animate"]=="jump":
				val = 0;
				if name in self.__contentAnimationState: 
					val = self.__contentAnimationState[name]["yDelta"];
					if val <= -10: 
						val = 0
					else:
						val = val - 1;
				y = y + val;
				self.__contentAnimationState[name] = {"yDelta": val}

		return x, y, width, height, alpha



class GameScene:
	def __init__(self, stage):
		self.stage = stage
		self.elements = {}
		self.setup()

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
