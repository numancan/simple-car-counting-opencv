import numpy as np
import random
import cv2

cap = cv2.VideoCapture("src/traffic.mp4")
subtractor = cv2.createBackgroundSubtractorMOG2()
FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
KERNEL = np.ones((5, 5))


class CarCounter:
    def __init__(self):
        self.biggest_visible_c_c = 0
        self.visible_car_count = 0
        self.have_car = False
        self.count = 0
        self.frame = None

    def ProcessFrame(self, frame):
        mask = subtractor.apply(frame)
        mask = cv2.GaussianBlur(mask.copy(), (5, 5), 0)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL)
        mask = cv2.inRange(mask, 140, 255)
        self.DrawRect(mask)
        return mask

    def DrawRect(self, image):
        p, conts, __ = cv2.findContours(image, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_NONE)

        self.visible_car_count = 0
        for cnt in conts:
            if(cv2.contourArea(cnt) > 300):
                x, y, w, h = cv2.boundingRect(cnt)
                if y > 200:
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(self.frame, str(self.count), (30, 30), FONT, 1,
                            (255, 0, 0), 1, cv2.LINE_AA)
                if(y > 300 and y < 360):
                    self.visible_car_count += 1
                    if self.biggest_visible_c_c < self.visible_car_count:
                        self.biggest_visible_c_c = self.visible_car_count

        if(self.visible_car_count == 0 and self.have_car == False):
            pass
        elif(self.visible_car_count == 0 and self.have_car):
            self.Counter(self.biggest_visible_c_c)
            self.have_car = False
            self.biggest_visible_c_c = 0
        elif (self.visible_car_count > 0 and self.have_car == False):
            self.have_car = True

    def Counter(self, value):
        self.count += value
        print("COUNT: ", self.count)

    def Start(self):
        while(True):
            _, self.frame = cap.read()
            processed = self.ProcessFrame(self.frame)

            cv2.imshow("frame", self.frame)
            cv2.imshow("processed", processed)

            if cv2.waitKey(29) & 0xFF == 27:
                break


CarCounter().Start()
cap.release()
cv2.waitKey()
cv2.destroyAllWindows()
