# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:47:56 2022

@author: Mason


Not sure what I was using this file for...

"""
from PIL import Image
import os, os.path

#print(len([name for name in os.listdir(r"C:\Users\Mason\Desktop\2013\Images")]))
def convertToRelative(path):
    
    imagePath = os.path.join(path ,"Images")
    
    trainPath = os.path.join(path, "NoteTrainingSet")
    
    fixedTrainPath = os.path.join(path, "NoteTrainingSetFixed")
    try:
        os.mkdir(fixedTrainPath)
    except:
        print("Folder already created")
    #Gets image pixel size X x Y
    
    for name in os.listdir(imagePath):
        #Finds corresponding bounding box data file for each image
        dataName = name.replace('.png', '.txt')

        #Extracts data
        dataFilename = os.path.join(path, trainPath , dataName)
        
        with open(dataFilename, 'r') as f:
            lines = f.readlines()

        #Writes relative data to new file named same as image file as per YOLOv5 req

        
        #EX : C:\Users\Mason\Desktop\2013\x1\filename_x1.txt
        
        fixedDataPath = os.path.join(fixedTrainPath, dataName)
        
        with open(fixedDataPath, "w") as w:
            counter = 0
            for line in lines:
                lineList = line.strip('[]\n').split(' ')
                
                print(lineList)
                    
                classid = 0
                #Maths to convert to relative form
                #convert x1 y1 a b into relative x1 y1 x2 y2
                
                xcenter = float(lineList[1]) * 2
                ycenter = float(lineList[2]) * 2
                    
                width = float(lineList[3]) * 2
                height = float(lineList[4]) * 2
                
                classid = int(lineList[0])
                #Takes the average of x1 and x2, y1 and y2 respectivley for each box to find center x and y
                
                counter += 1
                
                if counter < len(lines):
                    w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(classid, xcenter, ycenter, width, height) + "\n")
                else:
                    w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(classid, xcenter, ycenter, width, height))
                

                
                
        print("end of file")
        
convertToRelative(r"C:\Users\Mason\Desktop\ml\2013")