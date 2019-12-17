#!/usr/bin/env python3

"""
Image aspect ratio cropper

This batch tool crops JPG images in the current folder 
to a desired aspect ratio. You can select the cropping 
area with your mouse.

Usage: python3 image-aspect-ratio-cropper.py
"""

__author__ = "Lorand Horvath"
__copyright__ = "Copyright 2019, hlorand.hu"
__license__ = "https://choosealicense.com/licenses/gpl-3.0/"
__version__ = "0.1"
__email__ = "email at hlorand dot hu"

import cv2
import glob
import os

# default aspect ratio
a = 3
b = 2

# jpg save quality
quality = 90

# global variable for the cropping area
croppingarea = [(-1,-1),(-1,-1)]

# selection finished?
cropit = False

def set_cropping_area(event, x, y, flags, param):
    global croppingarea, cropit, a, b
        
    if event == cv2.EVENT_MOUSEMOVE:
        croppingarea = []

        # calculate aspect ratio based on image dimensions
        aspect_a = round(image.shape[0]/a*b)
        aspect_b = round(image.shape[1]/a*b)

        # clamp aspect ratio box into the canvas
        if y > image.shape[0]-aspect_b:
            y = image.shape[0]-aspect_b
        if x > image.shape[1]-aspect_a:
            x = image.shape[1]-aspect_a

        # calculate aspect ratio box size
        if image.shape[0] > image.shape[1]:
            croppingarea.append((x, 0))
        else:
            croppingarea.append((0, y))

        if image.shape[0] > image.shape[1]:
            croppingarea.append((x+aspect_a,image.shape[0]))
        else:
            croppingarea.append((image.shape[1],y+aspect_b))

        # draw cropping area
        origimage = image.copy()
        cv2.rectangle(origimage, croppingarea[0], croppingarea[1], (0, 255, 0), 20)
        cv2.imshow("image", origimage)

    # on mouseclick crop the image
    if event == cv2.EVENT_LBUTTONDOWN:
        cropit = True


# create folders
try:
    os.mkdir(os.getcwd() + "/cropped")
except OSError:
    print ("Cannot create directory named \"cropped\" (already exsists?) ")
try:
    os.mkdir(os.getcwd() + "/original")
except OSError:
    print ("Cannot create directory named \"done\" (already exsists?) ")

# load every jpg in the current directory
print("Current directory: " + os.getcwd())
for img in glob.glob('*.jpg') + glob.glob('*.JPG'):
    
    image = cv2.imread(img)
    clone = image.copy()

    # create window
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("image", 700,700)
    cv2.moveWindow("image", 40,40)
    cv2.setMouseCallback("image", set_cropping_area)
    cv2.imshow("image", image)

    # debug info
    print(img)
    print("Original W: " + str(image.shape[1]) + " H: " + str(image.shape[0]))

    while cropit == False:
        key = cv2.waitKey(1) & 0xFF

        # keys 1,2,3 modifies the aspect ratio
        if key == ord("1"):
            a = 16
            b = 9
        if key == ord("2"):
            a = 4
            b = 3
        if key == ord("3"):
            a = 3
            b = 2
            
        # key s switches the aspect ratio
        if key == ord("s"):
            a,b = b,a
            
        # quit
        if key == ord("q"):
            exit()

        # crop shortcuts (alternative to mouse click)
        if key == ord("c") or key == ord(" "):
            cropit = True
            break

        # next image
        if key == ord("n"):
            break

    # crop the image
    if cropit and len(croppingarea) == 2:
        roi = clone[croppingarea[0][1]:croppingarea[1][1], croppingarea[0][0]:croppingarea[1][0]]
        cv2.imwrite(os.getcwd() + "/cropped/" + img, roi,[int(cv2.IMWRITE_JPEG_QUALITY), quality])
        cropit = False
        print("New      W: " + str(roi.shape[1]) + " H: " + str(roi.shape[0]) )

        # move image to the "original" folder
        os.rename(os.getcwd() + "/" + img, os.getcwd() + "/original/" + img)
     
    # close all open windows
    cv2.destroyAllWindows()
