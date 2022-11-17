# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 10:26:47 2022

@author: Mason

Converts (x1, y1, x2, y2) to (obj centerX centerY w h)

"""

from PIL import Image
import os, os.path

#print(len([name for name in os.listdir(r"C:\Users\Mason\Desktop\2013\Images")]))
def convertToRelative(path, dataWidth):
    
    imagePath = os.path.join(path ,"Images")
    
    trainPath = os.path.join(path, "train")
    try:
        os.mkdir(trainPath)
    except:
        print("Folder already created")
    #Gets image pixel size X x Y
    
    for name in os.listdir(imagePath):
        filename = os.path.join(path ,"Images", str(name))
        
        img = Image.open(filename)
        #return(img.size)
        print(img.size)
        
        xsize, ysize = img.size
        
        
        #Finds corresponding bounding box data file for each image
        dataName = name
        dataSuffix = ".txt" #"_" + str(dataWidth) +
        
        remove = ".png"
        
        for char in remove:
            dataName = dataName.replace(char, "")
        
        dataNameR = dataName + dataSuffix

        #Extracts data
        dataFilename = os.path.join(path, dataWidth , dataNameR)
        
        with open(dataFilename, 'r') as f:
            lines = f.readlines()
        
        #Removes the header (first line) from the file and writes correct header (x center, y center, width, height)
        lines.pop(0)

        #Writes relative data to new file named same as image file as per YOLOv5 req
        relativeDataName =  dataName + ".txt"
        
        #EX : C:\Users\Mason\Desktop\2013\x1\filename_x1.txt
        relativeDataPath = os.path.join(path, "train", relativeDataName)
        with open(relativeDataPath, "w") as w:
            counter = 0
            for line in lines:
                lineList = line.strip('[]\n').split(', ')

                
                classid = 0
                #Maths to convert to relative form
                #convert x1 y1 a b into relative x1 y1 x2 y2
                
                x1 = float(lineList[0]) / xsize
                x2 = float(lineList[2]) / xsize
                    
                y1 = float(lineList[1]) / ysize
                y2 = float(lineList[3]) / ysize
                #Takes the average of x1 and x2, y1 and y2 respectivley for each box to find center x and y
                xcenter = (x1 + x2)/2
                ycenter = (y1 + y2)/2
                    
                width = x2 - x1
                height = y2 - y1
                
                counter += 1
                
                if counter < len(lines):
                    w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(classid, xcenter, ycenter, width, height) + "\n")
                else:
                    w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(classid, xcenter, ycenter, width, height))
                

                
                
        print("end of file")
        
sizeToRun = input("What size should be run? ")
convertToRelative(r"C:\Users\Mason\Desktop\ml\2013", sizeToRun)