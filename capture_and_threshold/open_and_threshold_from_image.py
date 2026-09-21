#! /bin/env/pyhton3
import cv2 as cv
import numpy as np
import sys
import matplotlib.pyplot as plt

def nothing(x):
    pass

#cap = cv.VideoCapture(0)

#if cap == None:
#   syslog(f"La camera non può essere aperta")


#while True:
    #ret, img = cap.read()
path: str = '/home/simone/Uni/magistrale/tirocinio/tesi/images/chap_3/cella_vishay_strain_gauge.jpg'
img = cv.imread(path,1)

window = 'Originale'
cv.namedWindow(window,cv.WINDOW_NORMAL)
cv.imshow(window,img)

cv.imshow('finestra',img)
    #if cv.waitKey(1) == ord('q'):
    #    cv.destroyWindow('finestra')
    #   cap.release()
    #   break

cv.namedWindow('Binary threshold')
cv.namedWindow('Gaussian threshold')
cv.namedWindow('Blurred')
trackbar_name = 'soglia'

soglia_bt = cv.createTrackbar(trackbar_name, 'Binary threshold' , 0, 255, nothing)
soglia_gt = cv.createTrackbar(trackbar_name, 'Gaussian threshold' , 0, 100, nothing)
cv.setTrackbarMin(trackbar_name,'Gaussian threshold',1)

while True:
    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY,0)

    soglia_bt = cv.getTrackbarPos(trackbar_name,'Binary threshold')
    soglia_gt = cv.getTrackbarPos(trackbar_name,'Gaussian threshold')

    ret, bin_thresh = cv.threshold(gray,soglia_bt,255,cv.THRESH_BINARY)
    gaussian_threshold = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,soglia_gt*2+1,2)
    blurred = cv.blur(gray,(10,2))  # eventualmente aggiungi trackbar
    gx = cv.Sobel(gray,cv.CV_64F,1,0,ksize = 1)
    gy = cv.Sobel(gray,cv.CV_64F,0,1,ksize = 1)
    magnitude = np.sqrt((np.abs(gx) ** 2)+(np.abs(gy) ** 2))
    laplacian = cv.Laplacian(gray,cv.CV_64F)

    cv.imshow('Gray',gray)
    cv.imshow('Binary threshold',bin_thresh)
    cv.imshow('Gaussian threshold',gaussian_threshold)
    cv.imshow('Blurred',blurred)
    cv.imshow('Gradient magnitude',magnitude)
    cv.imshow('laplacian',laplacian)
    if cv.waitKey(100) == ord('q'):
        break



cv.destroyAllWindows()
