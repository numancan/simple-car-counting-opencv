import numpy as np
import random
import cv2

cap = cv2.VideoCapture("src/traffic.mp4")
cap_res = (720, 1280)
# cap_res = (cv2.get(cv2.cv_cap), cv2.get(cv2.CV_CAP_PROP_FRAME_HEIGHT))
subtractor = cv2.createBackgroundSubtractorMOG2()
font = cv2.FONT_HERSHEY_COMPLEX_SMALL


class CarCounter:
    def __init__(self):
        self.biggest_visible_c_c = 0
        self.visible_car_count = 0
        self.have_car = False
        self.count = 0
        self.frame = None
        self.kernel = np.ones((5, 5))
        self.line = np.empty_like(cap.read()[1][300:720, 220:850])
        cv2.line(self.line, (0, 550), (850, 550), (0, 0, 255), 30)
        # cv2.imshow("sas",self.line)
        self.line = cv2.cvtColor(self.line.copy(), cv2.COLOR_BGR2GRAY)

    def ProcessFrame(self, frame):
        # mask = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = subtractor.apply(frame)
        mask = cv2.GaussianBlur(mask.copy(), (5, 5), 0)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
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
                cv2.putText(self.frame, str(self.count), (30, 30), font, 1,
                            (255, 0, 0), 1, cv2.LINE_AA)
                if(y > 300 and y < 360):
                    self.visible_car_count += 1
                    if(self.biggest_visible_c_c < self.visible_car_count):
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

            if cv2.waitKey(25) & 0xFF == ord('q') or self.frame is None:
                break


CarCounter().Start()
cap.release()
cv2.waitKey()
cv2.destroyAllWindows()
