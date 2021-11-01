import cv2 
import numpy as py
import os
import time
from ctypes import *
arducam_vcm= CDLL('./libarducam_vcm.so')
try:
    import picamera
    from picamera.array import PiRGBArray
except:
    sys.exit(0)

def focusing(val):
    arducam_vcm.vcm_write(val)
    #print("focus value: {}".format(val))

def sobel(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Sobel(img_gray,cv2.CV_16U,1,1)
    return cv2.mean(img_sobel)[0]

def laplacian(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img_sobel = cv2.Laplacian(img_gray,cv2.CV_16U)
    return cv2.mean(img_sobel)[0]


def calculation(camera):
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture,format="bgr", use_video_port=True)
    image = rawCapture.array
    rawCapture.truncate(0)
    return laplacian(image)


def autofocus():
    arducam_vcm.vcm_init()
    camera = picamera.PiCamera()
    camera.start_preview()
    camera.resolution = (640, 480)
    time.sleep(0.1)
    camera.shutter_speed=30000

    max_index = 10
    max_value = 0.0
    last_value = 0.0
    dec_count = 0
    focal_distance = 10
    #capture_interval=0
    while True:
        #capture_interval+=1
        focusing(focal_distance)
        #if capture_interval%10==0:
            #camera.capture('testimages/test'+str(a)+'.jpg')
        val = calculation(camera)
        if val > max_value:
            max_index = focal_distance
            max_value = val
        if val < last_value:
            dec_count += 1
        else:
            dec_count = 0
        if dec_count > 6:
            break
        last_value = val
        focal_distance += 15
        if focal_distance > 1000:
            break

    focusing(max_index)
    time.sleep(1)
    camera.resolution = (1920,1080)
    camera.capture("Label.jpg")
    #print("max index = %d,max value = %lf" % (max_index,max_value))
    #while True:
    #   time.sleep(1)

    camera.stop_preview()
    camera.close()
    return True
