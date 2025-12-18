import cv2
import time
import numpy as np
from comtypes import CLSCTX
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.activate(IAudioEndpointVolume._iid_, CLSCTX, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

vol = 0
volBar = 400
vorPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]   # Thumb tip
        x2, y2 = lmList[8][1], lmList[8][2]   # Index finger tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (y2, x2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        #Hand range 50 - 300
        #Volume range -65 - 0
        vol = np.interp(length,[50, 300], [minVol, maxVol])
        volBar = np.interp(length,[50, 300], [400, 150])
        volPer = np.interp(length,[50, 300], [0, 100])


        print(length, vol)
        volume.setMasterVolumeLevel(vol, None )

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(vol)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Volume: {int(volPer)} %', (10, 650), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow('Img', img)
    cv2.waitKey(1)
