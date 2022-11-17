# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:20:50 2022

@author: Mason
"""
import numpy as np
import cv2 as cv
import os

staffDetectionDir = 'train'
usefulBoxDir      = 'usefulTrain'
noteDetectionDir  = 'NoteTrainingSet'
imageDir          = 'testImage'
saveDir           = 'snippedBoxes'

usefulBoxes      = []

yAdjustTolerance = 90

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)
def rowGrouping(usefulBoxes):
    
    moveLeft = 0
    rowThreshold = 50
    rowLength = [0]
    totalCount = 0
    rowPositions = []
    rowNum = 0
    len(usefulBoxes)
    
    for boxes in usefulBoxes:
        totalCount += 1
        #boxes = [classID, x1, y1, x2, y2]
        
        
        x1 = boxes[1]
        y1 = boxes[2]
        x2 = boxes[3]
        y2 = boxes[4]
        
        roughBoxHeight = y2-y1
        
        if rowLength[rowNum] == 0:
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
            
            rowLength[rowNum] += 1
        
        #Checks if the box is within the row and adjusts the start and end plaements
        elif y1 > rowStartY - rowThreshold and y1 < rowStartY + rowThreshold:
            
            if rowStartX > x1:
                rowStartX = x1
            elif rowEndX < x2:
                rowEndX = x2
            if rowStartY > y1:
                rowStartY = y1
            elif rowEndY < y2:
                rowEndY = y2
            
            rowLength[rowNum] += 1
        
        #This else statement denotes that the current row has ended
        #Because of this we know the final positioning of the previous row and can reset and prepare for the next row.
        else:
            
            line = [(int(rowStartX), int(rowStartY+(roughBoxHeight/2))), (int(rowEndX), int(rowEndY-(roughBoxHeight/2)))]
            
            rowPositions.append([rowStartX-moveLeft, rowStartY, rowEndX-moveLeft, rowEndY, line])
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
            rowNum += 1
            rowLength.append(1)

        if totalCount >= len(usefulBoxes):
            line = [(int(rowStartX-moveLeft), int(rowStartY+(roughBoxHeight/2))), (int(rowEndX-moveLeft), int(rowEndY-(roughBoxHeight/2)))]
            
            rowPositions.append([rowStartX, rowStartY, rowEndX, rowEndY, line])
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
    print(rowPositions)        
    return(rowPositions)
def convertToPixel(image, dataFile):

    try:
        with open(dataFile, "r") as f:
            boxList = f.read().split("\n")
            boxList = [x.split(" ") for x in boxList]
            boxList = [[float(y) for y in x ] for x in boxList]
    
        boxes = np.array(boxList)
        
        img = cv.imread(image)
    
    
        width, height = img.shape[1], img.shape[0]
    
        convert = np.copy(boxes)
        convert[:, [1, 3]] = boxes[:, [1, 3]] * width
        convert[:, [2, 4]] = boxes[:, [2, 4]] *height
    
        convert[:, 1] = np.round(convert[:, 1] - (convert[:, 3] / 2), 2)
        convert[:, 2] = np.round(convert[:, 2] - (convert[:, 4] / 2), 2)
        convert[:, 3] = np.round(convert[:, 1] + (convert[:, 3]), 2)
        convert[:, 4] = np.round(convert[:, 2] + (convert[:, 4]), 2)
        #print(convert)
        return(convert)
    
        #Save converted note file
    
    
    
        #Uncomment to graph bounding boxes to ensure conversion worked properly
        '''
        for x in convert:
            obj_cls, x1, y1, x2, y2 = x
    
            x1 = int(x[1])
            y1 = int(x[2])
    
            x2 = int(x[3])
            y2 = int(x[4])
            #print(x1, y1, x2, y2)
    
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    
        cv.imshow('image', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        '''
    except:
        print("The file " , image ," you are looking for is not available")
def showBoxesOnImage(image, boxes, drawLine = False):
    
    imageFile = cv.imread(image)
    prevBox = None 
    for box in boxes:
        
        
    

        x1 = int(box[0])
        y1 = int(box[1])

        x2 = int(box[2])
        y2 = int(box[3])
        #print(x1, y1, x2, y2)
        if drawLine == True:
            line = box[4]
            slope = (line[0][1]-line[1][1])/(line[0][0]-line[1][0])
            print("The line follows Y=" + str(slope) + "x + " + str(line[0][1]))
            
            cv.line(imageFile, line[0], line[1], (255, 0, 0), 2)
        cv.rectangle(imageFile, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    resize = ResizeWithAspectRatio(imageFile, 1280)
    cv.imshow('image', resize)
    cv.waitKey(0)
    cv.destroyAllWindows() 
    
    prevBox = box
    
def getStaffBoxes(image):
    imageWithDir = os.path.join(imageDir, image)

    dataName = image.replace('.png', '.txt')

    boxData = os.path.join(staffDetectionDir, dataName)
    boxList = convertToPixel(imageWithDir, boxData)
    
    return boxList

for image in os.listdir(imageDir):

    if '.png' in image:
        dataName = image.replace('.png', '.txt')

        #boxData  = os.path.join(staffDetectionDir, dataName)
        #noteData = os.path.join(noteDetectionDir, dataName)
        imageWithDir = os.path.join(imageDir, image)
        


        print(dataName)
        print(imageWithDir)
        
        
        boxes = getStaffBoxes(image)
        
        
        showBoxesOnImage(imageWithDir, rowGrouping(boxes), True)
        
        #print(rowGrouping(boxes))
        
        #convertToPixel(imageWithDir, noteData)
        '''
        boxes = getStaffBoxes(image)
        
        rowPosition, rowLength = rowGrouping(boxes)

        expandedBoxes = boxExpansion(rowPosition, rowLength, boxes)
        
        checkNotesInBox(image, expandedBoxes)
        '''
    else:
        print('Thats not an image mate')