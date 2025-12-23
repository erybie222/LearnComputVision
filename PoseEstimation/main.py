import cv2
import time
import PoseModule as pm
def main():

    cap = cv2.VideoCapture(0)  # można też użyć wideo zamiast kamery: cv2.VideoCapture('video.mp4')
    pTime = 0
    detector = pm.poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img, draw=True)
        lmList = detector.findPosition(img, draw=True)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == "__main__":
    main()