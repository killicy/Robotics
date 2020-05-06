import numpy as np
import cv2
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

video_capture = cv2.VideoCapture(-1)
video_capture.set(3, 160)
video_capture.set(4, 120)

# Setup Output Pins

#left and right PWM voltages
PWM.start("P8_13", 0, 1000)
PWM.start("P8_19", 0, 1000)
PWM.set_duty_cycle("P8_13", 60)
PWM.set_duty_cycle("P8_19", 60)

#Left (in1, in2)
GPIO.setup("P9_11", GPIO.OUT)
GPIO.setup("P9_13", GPIO.OUT)

#Right (in3, in4)
GPIO.setup("P9_12", GPIO.OUT)
GPIO.setup("P9_14", GPIO.OUT)

while(True):

    # Capture the frames
    ret, frame = video_capture.read()

    # Crop the image
    crop_img = frame[60:120, 0:160]

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
    _,contours,_ = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        print cx
        print cy

        if cx >= 120:
            offset_x = (cx-60)
            GPIO.output("P9_11", GPIO.HIGH)
            GPIO.output("P9_13", GPIO.LOW)
            GPIO.output("P9_12", GPIO.LOW)
            GPIO.output("P9_14", GPIO.LOW)
            print "left"

        if cx < 120 and cx > 50:
            GPIO.output("P9_11", GPIO.HIGH)
            GPIO.output("P9_13", GPIO.LOW)
            GPIO.output("P9_12", GPIO.LOW)
            GPIO.output("P9_14", GPIO.HIGH)
            print "forward"

        if cx <= 50:
            offset_x = (60-(60-cx))
            GPIO.output("P9_12", GPIO.LOW)
            GPIO.output("P9_14", GPIO.HIGH)
            GPIO.output("P9_11", GPIO.LOW)
            GPIO.output("P9_13", GPIO.LOW)
            print "right"

    else:
        GPIO.output("P9_11", GPIO.LOW)
        GPIO.output("P9_13", GPIO.LOW)
        GPIO.output("P9_12", GPIO.LOW)
        GPIO.output("P9_14", GPIO.LOW)

