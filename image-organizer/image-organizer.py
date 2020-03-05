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

i = 0
while i < len(images):
    
    #load 3 images
    img = images[i]
    img2 = images[i+1] if i+1<len(images) else images[i]
    img3 = images[i+2] if i+2<len(images) else (images[i+1] if i+1<len(images) else images[i])
    image = cv2.imread(img)
    image2 = cv2.imread(img2)
    image3 = cv2.imread(img3)

    # stack images
    dim = (640, 480)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_NEAREST)
    image2 = cv2.resize(image2, dim, interpolation = cv2.INTER_NEAREST)
    image3 = cv2.resize(image3, dim, interpolation = cv2.INTER_NEAREST)

    # add image num and filename
    text = str(i+1) + " / " + str(len(images)) + " - " + images[i]
    cv2.putText(image,text, (5,460), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 3)

    numpy_horizontal = np.hstack((image, image2, image3))
    image = np.concatenate((image, image2, image3), axis=1)
    
    cv2.imshow("window", image)

    # debug info
    print(img)

    key = cv2.waitKey(0)

    # Esc = quit
    if key == 27:
        exit()

    # Backspace = undo last operation
    if key == 8 and i>0:
        i = i-1
        print("undo " + images[i])
        os.rename(os.getcwd() + "/" + folders.pop() + "/" + images[i], os.getcwd() + "/" + images[i])
        continue

    if chr(key) not in "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        continue

    try:
        os.mkdir(os.getcwd() + "/" + chr(key))
    except FileExistsError:
        pass

    # move image
    os.rename(os.getcwd() + "/" + img, os.getcwd() + "/" + chr(key) + "/" + img)
    
    # save history
    folders.append( chr(key) )

    # close all open windows
    #cv2.destroyAllWindows()

    # next image
    i = i + 1
