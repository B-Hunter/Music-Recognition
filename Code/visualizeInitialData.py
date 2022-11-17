# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:59:35 2022

@author: Mason

USE THIS FILE WITH (x1, y1, x2, y2) FORMATTED DATA OR YOU WILL HAVE ISSUES

"""

# -*- coding: utf-8 -*-
import random
import os
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt


#Plots the images and bounding boxes
def plotBox(image, dataFile):
    
    #Gets the boxes from the list   
    
    imagePlot = ImageDraw.Draw(image)
    
    with open(dataFile, 'r') as f:
        lines = f.readlines()

    lines.pop(0)
    
    for line in lines:
        lineList = line.strip('[]\n').split(', ')
                
        x1 = float(lineList[0])
        x2 = float(lineList[2])
                    
        y1 = float(lineList[1])
        y2 = float(lineList[3])
        imagePlot.rectangle((x1, y1, x2, y2), outline=0, width = 5)
        print(str(x1) + ", " + str(y1) + ", " + str(x2) + ", " + str(y2))
    #Plots boxes and image
    

    #print(x1, y1, x2, y2)
    
    
    plt.imshow(np.array(image), cmap = 'gray') 
    plt.show()
    
    
#Gets current path
path = os.path.abspath(os.getcwd())

#Determines what file to look at
#size = input("What file size would you like to run?")

size = "x1"

dataFile = os.path.join(path, size)
dataName = 'GR_0004.txt'

dataFile = os.path.join(path, size, dataName)



print(dataFile)

    
imageName = dataName.replace('.txt', '.png')
#imageFile = os.path.join(path, "Images", imageName)
imageFile = os.path.join(path, 'Images', 'GR_0004.png')
print(imageFile)
    


image = Image.open(imageFile)

plotBox(image, dataFile)