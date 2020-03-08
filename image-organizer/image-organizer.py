#!/usr/bin/env python3

"""
Image organizer

The script loads all JPG image from the current folder. You can
sort the images into folders by pressing a key on your keyboard. 
The script creates a folder (folder name: the button you pressed)
and moves the image into this new folder. 

Use the backspace key to undo last operation.

Usage: python3 image-organizer.py
"""

__author__ = "Lorand Horvath"
__copyright__ = "Copyright 2020, hlorand.hu"
__license__ = "https://choosealicense.com/licenses/gpl-3.0/"
__version__ = "0.1"
__email__ = "email at hlorand dot hu"

import cv2
import glob
import os
import sys
import shutil
import numpy as np

print("Current directory: " + os.getcwd())

# load every jpg in the current directory
images = glob.glob('*.jpg') + glob.glob('*.JPG') + glob.glob('*.JPEG') + glob.glob('*.jpeg')

# move history
folders = []

# create window
cv2.namedWindow("window",cv2.WINDOW_NORMAL)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)
cv2.resizeWindow("window", 1200,600)
cv2.moveWindow("window", 40,40)

def calculate_dim(image):

    height, width, channels = image.shape

    if width > height:
        dim = ( 640, 480)
    else: 
        dim = ( 360, 480 )
    return dim


i = 0
while i < len(images):
    
    #load 3 images
    img1 = images[i]
    img2 = images[i+1] if i+1<len(images) else images[i]
    img3 = images[i+2] if i+2<len(images) else (images[i+1] if i+1<len(images) else images[i])
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)
    image3 = cv2.imread(img3)

    # stack images
    
    image1 = cv2.resize(image1, calculate_dim(image1), interpolation = cv2.INTER_LINEAR)
    image2 = cv2.resize(image2, calculate_dim(image2), interpolation = cv2.INTER_LINEAR)
    image3 = cv2.resize(image3, calculate_dim(image3), interpolation = cv2.INTER_LINEAR)

    # add image num and filename
    text = str(i+1) + " / " + str(len(images)) + " - " + images[i]
    cv2.putText(image1,text, (5,460), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3)

    numpy_horizontal = np.hstack((image1, image2, image3))
    image = np.concatenate((image1, image2, image3), axis=1)
    
    cv2.imshow("window", image)

    # debug info
    print(img1)

    key = cv2.waitKey(0)

    # Esc = quit
    if key == 27:
        exit()

    # Space = skip image
    if key == 32:
        i = i + 1
        continue
    
    # c,v,b = open image in full size
    if key == ord('c') or key == ord('v') or key == ord('b'):
        path = os.path.dirname(os.path.realpath(__file__))
        if key == ord('c'):
            os.system("open \"" + path + "/" + img1 + "\"")
        if key == ord('v'):
            os.system("open \"" + path + "/" + img2 + "\"")
        if key == ord('b'):
            os.system("open \"" + path + "/" + img3 + "\"")

    # Backspace = undo last operation
    if key == 8 and i>0:
        i = i-1
        print("undo " + images[i])
        os.rename(os.getcwd() + "/" + folders.pop() + "/" + images[i], os.getcwd() + "/" + images[i])
        continue

    if chr(key) not in "1234567890a  defghijklmnopqrstu wxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        continue

    try:
        os.mkdir(os.getcwd() + "/" + chr(key))
    except FileExistsError:
        pass

    # move image
    os.rename(os.getcwd() + "/" + img1, os.getcwd() + "/" + chr(key) + "/" + img1)
    
    # save history
    folders.append( chr(key) )

    # close all open windows
    #cv2.destroyAllWindows()

    # next image
    i = i + 1
