import cv2
import numpy as np
import os
import handTracking

# Constants
BRUSH_THICKNESS = 15
ERASE_THICKNESS = 25
FOLDER_PATH = 'assets'
DRAW_COLOR = (0, 255, 0)  
WCAM, HCAM = 640, 480
DETECTION_CON = 0.8

def load_overlay_images(folder_path):
    """
    Load overlay images for the header.

    Parameters:
    folder_path (str): The path to the folder containing the images.

    Returns:
    list: A list of overlay images.
    """
    my_list = os.listdir(folder_path)
    overlay_list = [cv2.imread(f'{folder_path}/{img_path}') for img_path in my_list]
    return overlay_list

def create_image_for_drawing(height, width):
    """
    Create an image to store the drawing.

    Parameters:
    height (int): The height of the image.
    width (int): The width of the image.

    Returns:
    numpy.ndarray: The image for drawing.
    """
    img_canvas = np.zeros((height, width, 3), np.uint8)
    return img_canvas

def select_color(x, y, header, draw_color):
    """
    Select the drawing color based on the coordinates.

    Parameters:
    x (int): The x-coordinate of the selected point.
    y (int): The y-coordinate of the selected point.
    header (numpy.ndarray): The header image.
    draw_color (tuple): The current drawing color.

    Returns:
    tuple: The updated header image and drawing color.
    """
    if y < 90:
        if 250 < x < 350:
            header = overlay_list[2]
            draw_color = (255, 0, 0)  # Red color
        elif 500 < x < 600:
            header = overlay_list[1]
            draw_color = (0, 0, 0)  # Black color
        elif 400 < x < 450:
            header = overlay_list[0]
            draw_color = (0, 255, 0)  # Green color
        elif 70 < x < 150:
            header = overlay_list[3]
            draw_color = (0, 0, 255)  # Blue color with reduced brightness
    return header, draw_color

def main():
    # Load color images for the header
    overlay_list = load_overlay_images(FOLDER_PATH)
    header = overlay_list[0]

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    cap.set(3, WCAM)
    cap.set(4, HCAM)

    detector = handTracking.Detector(detectionCon=DETECTION_CON)

    # Create an image to store the drawing
    img_canvas = create_image_for_drawing(HCAM, WCAM)

    while True:
        # Capture the frame
        success, img = cap.read()
        img = cv2.flip(img, 1)

        # Find hand landmarks
        img = detector.findHands(img)
        lm_list = detector.findPosition(img, draw=False)

        if len(lm_list) != 0:
            # Get the coordinates of the middle and index fingers
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]

            # Check which fingers are up
            fingers = detector.fingersUp()

            # Selection Mode: Two fingers are up
            if fingers[1] and fingers[2]:
                print('Selection Mode')
                header, DRAW_COLOR = select_color(x1, y1, header, DRAW_COLOR)
                cv2.rectangle(img, (x1, y1-20), (x2, y2+20), DRAW_COLOR, cv2.FILLED)

            # Drawing Mode: Index finger is up
            if fingers[1] and not fingers[2]:
                print('Drawing Mode')
                cv2.circle(img, (x1, y1), 15, DRAW_COLOR, cv2.FILLED)

                if XP == 0 and YP == 0:
                    XP, YP = x1, y1

                thickness = ERASE_THICKNESS if DRAW_COLOR == (0, 0, 0) else BRUSH_THICKNESS
                cv2.line(img, (XP, YP), (x1, y1), DRAW_COLOR, thickness)
                cv2.line(img_canvas, (XP, YP), (x1, y1), DRAW_COLOR, thickness)

                XP, YP = x1, y1

        # Convert the drawing to grayscale and apply threshold
        img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

        # Combine the webcam image with the drawing
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, img_canvas)

        img[0:90, 0:640] = header
        cv2.imshow('Image', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    XP, YP = 0, 0  # Initialize the XP and YP variables
    main()

