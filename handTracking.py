import cv2
import mediapipe as mp
import time


class Detector():
    def __init__(self, mode = False, modelComplexity = 1, maxHands = 2, detectionCon=0.5,trackCon = 0.5):
        """
        HandDetector class detects the presence of hands in images or videos.

        Parameters:
        mode (bool): Whether to detect multiple hands.
        modelComplexity (int): Complexity of the hand detection model (0, 1, or 2).
        maxHands (int): Maximum number of hands to detect.
        detectionCon (float): Detection confidence threshold.
        trackCon (float): Tracking confidence threshold.
        """

        self.mp = mp.solutions.hands
        self.hands   = self.mp.Hands(
            mode, maxHands, modelComplexity, detectionCon, trackCon
            )
        self.mp_draw  = mp.solutions.drawing_utils
        self.tip_ids = [4,8,12,16,20] # Media Pipe Tip Ids

    def findHands(self, img, draw=True):
        """
        Find hands in images or videos.

        Parameters:
        img (numpy.ndarray): Image or video frame to detect hands.
        draw (bool): Whether to draw landmarks on the image.

        Returns:
        numpy.ndarray: Image with drawn landmarks (if draw is True).
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp.HAND_CONNECTIONS)
        
        return img


    def findPosition(self, img, handNo = 0, draw = True):
        """
        Find the position of hand landmarks in the image.

        Parameters:
        img (numpy.ndarray): Image with detected landmarks.
        handNo (int): Hand index to consider when multiple hands are detected.
        draw (bool): Whether to draw circles around landmarks.

        Returns:
        list: List containing id of the landmark, x, and y positions.
        """
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,_ = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 7 , (255, 0 ,255), cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        """
        Determine which fingers are up based on the landmarks.

        Returns:
        list: A list representing the state of each finger (0: closed, 1: open).
        """
        fingers = []
        hand = []

        if self.lmList[2][1] > self.lmList[17][1]:
            hand.append(1)
            if self.lmList[self.tip_ids[0]][1] > self.lmList[self.tip_ids[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif self.lmList[2][1] <= self.lmList[17][1]: 
            hand.append(0)
            if self.lmList[self.tip_ids[0]][1] < self.lmList[self.tip_ids[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

    
        for id in range(1,5):
            if self.lmList[self.tip_ids[id]][2] < self.lmList[self.tip_ids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    

# Demosntracao do funcionamento da classe
def main():
    # pTime - previous time; cTime - current Time
    pTime   = 0
    cTime   = 0
    cap = cv2.VideoCapture(0)
    detector = Detector()

    while True:
        # lendo imagem da webcam e criando imgs a partir do video
        _, img = cap.read()
        img = cv2.flip(img, 1)
        # aplicando a funcao a funcao findHands nas imagens obtidas dos videos
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) !=0:
            print(lmList)
            
        # calculando e mostrando na tela o fps do video
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,0), 3)

        

        cv2.imshow("Image",img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
