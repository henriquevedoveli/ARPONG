# Criado em  : 2021-05-27
# Ult. att   : 2021-06-02
# 
# Autor      : Henrique Vedoveli <henriquevedoveli@gmail.com>

# bibiotecas necessarias
import cv2
import numpy as np
import os
import HandTracking as ht

###########################
# size header 640x90
brushThickness = 15
eraseThickness = 25
folderPath = 'header'
drawColor = (255,0,0)
xp, yp =0,0
wCam, hCam = 640, 480
detectionCon = 0.55
############################

# criando o header, imagem onde ficara o menu de troca de cores
myList = os.listdir(folderPath)
overlayList = []

for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

header = overlayList[0]

# iniciando a camera
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4, hCam)

detector = ht.handDetector(detectionCon=detectionCon)

# criando uma nova imagem que contera apenas o desenho
imgCanvas = np.zeros((hCam,wCam,3), np.uint8)

while True:
    # Importando a imagem
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Encontrando landmarks da mao
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # encontrando valores de x e y dos dedos medios e indicadores
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

    # Checando quais dedos estao levantados
        fingers = detector.fingersUp()
        
    # Casos dois dedos estejam levantados:
    # Entrara em modo de selecao
        if fingers[1] and fingers[2]:
            xp, yp =0,0
            print('Selection Mode')
            if y1 < 90:
                # Valores encontrados na base de tentativa e erro
                if 250<x1<350:
                    header = overlayList[0]
                    drawColor = (255,0,0)
                elif 500<x1<600:
                    header = overlayList[1]
                    drawColor = (0,0,0)
                elif 400<x1<450:
                    header = overlayList[2]
                    drawColor = (0,255,0)
                elif 70<x1<150:
                    header = overlayList[3]    
                    drawColor = (0,0,255)

            cv2.rectangle(img, (x1, y1-20), (x2,y2+20), drawColor, cv2.FILLED)   

        # Caso o dedo indicador esteja levantado entrara em modo desenho
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print('Drawing Mode')

            if xp==0 and yp==0: 
                xp,yp = x1, y1

            if drawColor == (0,0,0):
                cv2.line(img, (xp,yp), (x1, y1), drawColor,eraseThickness)
                cv2.line(imgCanvas, (xp,yp), (x1, y1), drawColor,eraseThickness)
            
            else:
                cv2.line(img, (xp,yp), (x1, y1), drawColor,brushThickness)
                cv2.line(imgCanvas, (xp,yp), (x1, y1), drawColor,brushThickness)
            
            xp, yp = x1, y1

    # transformando apenas o desenho em escala de ciza
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    # aplicando threshold e voltando para colorido
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    # unindo a imagem da webcam com o desenho
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    img[0:90, 0:640] = header
    cv2.imshow('Image',img)
    cv2.waitKey(1)






