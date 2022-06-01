import cv2
import numpy as np
from gesture_detect import HandDetector


canvas = None
last_x = last_y = -1

# For webcam input:
cap = cv2.VideoCapture(0)
detector = HandDetector()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        # Ignoring empty camera frame
        # If loading a video, use 'break' instead of 'continue'.
        continue        

    # Flip the capture image 
    image = cv2.flip(img, 1)

    h, w, c = image.shape
    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)



    hand, gesture, dummy_x, dummy_y = detector.chopHand(cv2.flip(img, 1))
    print(gesture)

    """
    hand, res, last_x, last_y = detector.chopHand(cv2.flip(img, 1), canvas, True, last_x, last_y)
    
    if hand is not None:
        hand = cv2.resize(hand, (128,128), interpolation = cv2.INTER_AREA)
        hh, hw, hc = hand.shape
        image[h-hh-30:h-30, w-hw-30:w-30] = hand
        print(res)
    else:
        canvas = np.zeros((h, w, 3), np.uint8)
    """




    image = cv2.addWeighted(image, 1, canvas, 1, 0)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()