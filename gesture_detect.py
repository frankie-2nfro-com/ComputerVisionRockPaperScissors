import cv2
import threading
import numpy as np

# from keras.models import load_model	
import mediapipe as mp


# class to create thread
class DrawingThread (threading.Thread):
	def __init__(self, image, w, h, x1, y1, x2, y2):
		threading.Thread.__init__(self)
		self.image = image
		self.w = w
		self.h = h
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def run(self):
		if self.x1<0 or self.x2<0 or self.y1<0 or self.y2<0:
			exit()
		#print ("Starting DrawingThread")
		px = int(self.x1 * self.w)
		py = int(self.y1 * self.h)
		px2 = int(self.x2 * self.w)
		py2 = int(self.y2 * self.h)    
		cv2.line(self.image, (px, py), (px2, py2), (255,255,255), thickness=4)
		cv2.line(self.image, (px2, py2), (px2+1, py2), (255,255,255), thickness=4) 
		#print ("Exiting DrawingThread")




class HandDetector:
	def __init__(self, csv_path="./assets/models/dataset.csv"):
		# Load the model
		#self.model = load_model('keras_model.h5')
		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
		#self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
		self.mpHands = mp.solutions.hands
		self.mpDraw = mp.solutions.drawing_utils
		self.mpDrawingStyle = mp.solutions.drawing_styles
		self.hands = self.mpHands.Hands(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

		# Gesture recognition model
		self.csv_path = csv_path
		self.file = np.genfromtxt(self.csv_path, delimiter=",")
		self.angle = self.file[:, :-1].astype(np.float32)
		self.label = self.file[:, -1].astype(np.float32)
		self.knn = cv2.ml.KNearest_create()
		self.knn.train(self.angle, cv2.ml.ROW_SAMPLE, self.label)

	def chopHand(self, image, canvas=None, drawing=False, lx=-1, ly=-1):
		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(image)
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		h, w, c = image.shape
		p8 = None
		resized_hand_box_image = None

		if self.results.multi_hand_landmarks is not None:
			for res in self.results.multi_hand_landmarks:
				hbx1, hby1, hbx2, hby2 = self.drawHand(image, res)

				joint = np.zeros((21, 3))
				for j, lm in enumerate(res.landmark):
					joint[j] = [lm.x, lm.y, lm.z]
				# Compute angles between joints
				v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
				v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
				v = v2 - v1 
				# Normalize v
				v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
				# Get angle using arcos of dot product
				angle = np.arccos(
					np.einsum(
						"nt,nt->n",
						v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
						v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :],
					)
				)  # [15,]
				angle = np.degrees(angle)  # Convert radian to degree
				# Inference gesture
				data = np.array([angle], dtype=np.float32)
				
				# detect gesture
				ret, results, neighbours, dist = self.knn.findNearest(data, 5)
				idx = int(results[0][0])

				p8 = res.landmark[8]     # pointer finger top point
			
			hand_box_image = image[hby1:hby2, hbx1:hbx2]
			boxh, boxw, boxc = hand_box_image.shape

			if boxh > 0 and boxw > 0:
				resized_hand_box_image = cv2.resize(hand_box_image, (256,256), interpolation = cv2.INTER_AREA)

			if  drawing and canvas is not None and p8 is not None and lx!=-1 and ly!=-1 and (idx==1 or idx==7):
				# use pointer (p8) to draw the line
				DrawingThread(canvas, w, h, lx, ly, p8.x, p8.y).start()

			if p8 is not None and resized_hand_box_image is not None:
				return resized_hand_box_image, idx, p8.x, p8.y

		return None, -1, -1, -1


	def drawHand(self, image, hand_landmarks):
		#self.mpDraw.draw_landmarks(
		#	image,
		#	hand_landmarks,
		#	self.mpHands.HAND_CONNECTIONS,
		#	self.mpDrawingStyle.get_default_hand_landmarks_style(),
		#	self.mpDrawingStyle.get_default_hand_connections_style())

		# find box of detected hand 
		h, w, c = image.shape
		min_x = w
		min_y = h
		max_x = max_y = 0
		for index in range(len(hand_landmarks.landmark)):
			data_point = hand_landmarks.landmark[index]
			px = int(data_point.x * w)
			py = int(data_point.y * h)

			if px < min_x and px >0:
				min_x = px
			if py < min_y and py >0:
				min_y = py
			if px > max_x and px < w:
				max_x = px
			if py > max_y and py < h:
				max_y = py

		box_width = max_x - min_x
		box_height = max_y - min_y
		diff = int(abs(box_width - box_height) / 2)

		# make box to be a square with border
		border = 30
		min_x = min_x - border
		min_y = min_y - border
		max_x = max_x + border
		max_y = max_y + border
		if box_width > box_height:
			min_y = min_y - diff
			max_y = max_y + diff
		elif box_height > box_width:
			min_x = min_x - diff
			max_x = max_x + diff

		# draw the box
		#c = (0,0,0)
		#cv2.line(image, (min_x, min_y), (max_x, min_y), c, thickness=3)
		#cv2.line(image, (min_x, max_y), (max_x, max_y), c, thickness=3)
		#cv2.line(image, (min_x, min_y), (min_x, max_y), c, thickness=3)
		#cv2.line(image, (max_x, min_y), (max_x, max_y), c, thickness=3)

		return min_x, min_y, max_x, max_y 


	"""
	def detectGesture():
		# convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that 
		# the color is converted from BGR to RGB
		color_coverted = cv2.cvtColor(self.stage.frame, cv2.COLOR_BGR2RGB)
		image=Image.fromarray(color_coverted)
		#image = Image.open('./test_scissors.jpg')

		#resize the image to a 224x224 with the same strategy as in TM2:
		#resizing the image to be at least 224x224 and then cropping from the center
		size = (224, 224)
		image = ImageOps.fit(image, size, Image.ANTIALIAS)

		#turn the image into a numpy array
		image_array = np.asarray(image)
		# Normalize the image
		normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
		# Load the image into the array
		self.data[0] = normalized_image_array

		# run the inference
		prediction = self.model.predict(self.data)

		pPos = prediction[0][0]
		sPos = prediction[0][1]
		rPos = prediction[0][2]

		# logic to determine the result
		choice = self.user_choice;
		if sPos > 0.5:		# and sPos > rPos
			choice = "S"
		elif rPos > 0.7 and rPos > pPos and rPos > sPos:
			choice = "R"
		elif pPos > 0.7 and pPos > rPos and pPos > sPos:
			choice = "P"

		return choice;
	"""