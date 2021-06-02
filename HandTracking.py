# Criado em  : 2021-05-24
# Ult. att   : 2021-06-01
# 
# Autor      : Henrique Vedoveli <henriquevedoveli@gmail.com>
# Notas      : A classe handDetector detecta a presenca de maos em imagens ou videos

# bibliotecas necessarias
import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon=0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands   = self.mpHands.Hands(self.mode, self.maxHands, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw  = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20] 


    # A funcao findHands encontra as maos nas imagens ou videos.
    #
    # Eh passado como parametro a imagem onde vai ser detectado a presenca da mao
    # e draw, que por padrao eh passado como verdadeiro, caso draw seja False 
    # nao sera desenhado as landmarks
    #
    # A funcao retorna a imagem com o desenho das landmarks
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img


    # A funcao findPosition encontra a posicao das landmarks na imagem
    # 
    # Eh passado como parametro a imagem, que ja deve conter as landmarks,
    # o numero da mao e draw que caso seja False nao sera desenhado os circulos das landmarks
    #
    # A funcao retorna uma lista contendo o id da landmark, o valor de x e y
    def findPosition(self, img, handNo = 0, draw = True):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # altura largura e cor da img
                h,w,_ = img.shape
                # cx - centro de x ; cy - centro de y
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 7 , (255, 0 ,255), cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        fingers = []
        hand = []

        if self.lmList[2][1] > self.lmList[17][1]:
            hand.append(1)
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif self.lmList[2][1] <= self.lmList[17][1]: 
            hand.append(0)
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

    
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
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
    # criando o obj handDetector
    detector = handDetector()

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
