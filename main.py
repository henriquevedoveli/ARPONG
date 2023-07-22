import cv2
import numpy as np
import os
import handTracking

# Constants
BRUSH_THICKNESS = 15
ERASE_THICKNESS = 25
FOLDER_PATH = 'assets'
DRAW_COLOR = (0, 255, 0)  # Green color
XP, YP = 0, 0
WCAM, HCAM = 640, 480
DETECTION_CON = 0.8

# Load color images for the header
myList = os.listdir(FOLDER_PATH)
overlayList = [cv2.imread(f'{FOLDER_PATH}/{imgPath}') for imgPath in myList]
header = overlayList[0]

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, WCAM)
cap.set(4, HCAM)

detector = handTracking.Detector(detectionCon=DETECTION_CON)

# Create an image to store the drawing
imgCanvas = np.zeros((HCAM, WCAM, 3), np.uint8)

while True:
    # Capture the frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Get the coordinates of the middle and index fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()

        # Selection Mode: Two fingers are up
        if fingers[1] and fingers[2]:
            XP, YP = 0, 0
            print('Selection Mode')
            if y1 < 90:
                # Color selection based on x-coordinate
                if 250 < x1 < 350:
                    header = overlayList[2]
                    DRAW_COLOR = (255, 0, 0)
                elif 500 < x1 < 600:
                    header = overlayList[1]
                    DRAW_COLOR = (0, 0, 0)
                elif 400 < x1 < 450:
                    header = overlayList[0]
                    DRAW_COLOR = (0, 255, 0)
                elif 70 < x1 < 150:
                    header = overlayList[3]
                    # Blue with reduced brightness
                    DRAW_COLOR = (int(0.3 * 255), int(2 * 0), int(0.3 * 255))

            cv2.rectangle(img, (x1, y1-20), (x2, y2+20), DRAW_COLOR, cv2.FILLED)

        # Drawing Mode: Index finger is up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, DRAW_COLOR, cv2.FILLED)
            print('Drawing Mode')

            if XP == 0 and YP == 0:
                XP, YP = x1, y1

            if DRAW_COLOR == (0, 0, 0):
                cv2.line(img, (XP, YP), (x1, y1), DRAW_COLOR, ERASE_THICKNESS)
                cv2.line(imgCanvas, (XP, YP), (x1, y1), DRAW_COLOR, ERASE_THICKNESS)
            else:
                cv2.line(img, (XP, YP), (x1, y1), DRAW_COLOR, BRUSH_THICKNESS)
                cv2.line(imgCanvas, (XP, YP), (x1, y1), DRAW_COLOR, BRUSH_THICKNESS)

            XP, YP = x1, y1

    # Convert the drawing to grayscale and apply threshold
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Combine the webcam image with the drawing
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:90, 0:640] = header
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
