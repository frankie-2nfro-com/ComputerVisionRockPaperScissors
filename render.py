import cv2
import numpy as np

# Function to handle all opencv2 graphic handleing and rendering

# some ref:
"""
https://note.nkmk.me/en/python-pillow-putalpha/
https://fontmeme.com/fancy-fonts/
https://wallpaperboat.com/squid-game-wallpapers
"""


def add_alpha_channel(img):
	# add a alpha channel (4th) for jpg (only have three channels)
	b_channel, g_channel, r_channel = cv2.split(img) 						# get each jpg channel
	alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 	# create addition Alpha channel
	img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel)) 	# merge the channel
	return img_new


def merge_img(jpg_img, png_img, y1, y2, x1, x2):
	# check if jpg_img already 4 channel, otherwise call add_alpha_channel to add to 4 channel
	if jpg_img.shape[2] == 3:
		jpg_img = add_alpha_channel(jpg_img)
	
	'''
	when merging two image, it will raise error if the positon and size parameters error. 
	so make adjustment to make merging without exception
	'''
	yy1 = 0
	yy2 = png_img.shape[0]
	xx1 = 0
	xx2 = png_img.shape[1]
 
	if x1 < 0:
		xx1 = -x1
		x1 = 0
	if y1 < 0:
		yy1 = - y1
		y1 = 0
	if x2 > jpg_img.shape[1]:
		xx2 = png_img.shape[1] - (x2 - jpg_img.shape[1])
		x2 = jpg_img.shape[1]
	if y2 > jpg_img.shape[0]:
		yy2 = png_img.shape[0] - (y2 - jpg_img.shape[0])
		y2 = jpg_img.shape[0]
 
	# get png alpha, need to divide 255 to get the value between 0-1
	alpha_png = png_img[yy1:yy2,xx1:xx2,3] / 255.0
	alpha_jpg = 1 - alpha_png
	
	# merging
	for c in range(0,3):
		jpg_img[y1:y2, x1:x2, c] = ((alpha_jpg*jpg_img[y1:y2,x1:x2,c]) + (alpha_png*png_img[yy1:yy2,xx1:xx2,c]))
 
	# convert back to 3 channels
	img = cv2.cvtColor(jpg_img, cv2.COLOR_BGRA2BGR)

	return img


# Animation Engine
def animate(stage, name, element):
	x = 0
	y = 0
	width = 0
	height = 0
	alpha = 1

	if "x" in element:
		x = element["x"]
	
	if "y" in element:
		y = element["y"]
	
	if "w" in element:
		width = element["w"]
	
	if "h" in element:
		height = element["h"]

	if "alpha" in element:
		alpha = 1

	if "animate" in element:
		if element["animate"]=="shake":
			x = x + random.randint(-5,5)
			y = y + random.randint(-5,5)
		elif element["animate"]=="jump":
			val = 0;
			if name in stage.contentAnimationState: 
				val = stage.contentAnimationState[name]["yDelta"];
				if val <= -10: 
					val = 0
				else:
					val = val - 1;
			y = y + val;
			stage.contentAnimationState[name] = {"yDelta": val}

	return x, y, width, height, alpha




def showText(stage, x, y, text, font, size, color, thickness):
	cv2.putText(img=stage.frame, text=text, org=(x, y), fontFace=font, fontScale=size, color=color,thickness=thickness)

def showLine(stage, x, y, x2, y2, color, thickness):
	cv2.line(stage.frame, (x, y), (x2,y2), color, thickness=thickness)

def showBox(stage, x, y, w, h, color, thickness):
	cv2.line(stage.frame, (x, y), (x+w,y), color, thickness=thickness)
	cv2.line(stage.frame, (x, y), (x,y+h), color, thickness=thickness)
	cv2.line(stage.frame, (x, y+h), (x+w,y+h), color, thickness=thickness)
	cv2.line(stage.frame, (x+w, y), (x+w,y+h), color, thickness=thickness)

def showJpeg(stage, file, x, y, w, h):
	img = cv2.imread(file)
	resizeImage = cv2.resize(img, (w,h))	
	stage.frame[y:h+y,x:w+x] = resizeImage

def showPng(stage, file, x, y, w, h):
	overlay = cv2.imread(file, cv2.IMREAD_UNCHANGED)
	stage.frame = merge_img(stage.frame, overlay, y, h+y, x, w+x)

def showCaptureVideo(stage, x, y, w, h):
	pipImage = cv2.resize(stage.originalFrame, (w,h))	
	stage.frame[y:h+y,x:w+x] = pipImage

def showSnapshot(stage, x, y, w, h):
	snapshotImage = cv2.resize(stage.snapshot, (w,h))	
	stage.frame[y:h+y,x:w+x] = snapshotImage	