"""
Created on Sun Apr 24 12:47:56 2022

@author: Mason


This is my main file. It handles most of the post processing. It is currently
in shambles since I was trying to use parts of it and such... probably best
to just rip my functions out of this and use in a seperate file with your own
pathing.

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

yAdjustTolerance = 50
#NO MORE DATAFILE SHENANIGANS THERE IS boxData and noteData - one for bounding boxes one for notes
def showBoxesOnImage(image, boxes):
    
    imageFile = cv.imread(image)
    
    for box in boxes:
        x1, y1, x2, y2 = box

        x1 = int(box[0])
        y1 = int(box[1])

        x2 = int(box[2])
        y2 = int(box[3])
        #print(x1, y1, x2, y2)

        #cv.rectangle(r"C:\Users\Mason\Desktop\ml\2013\GR_3000.png", (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)


    cv.imshow('image', imageFile)
    cv.waitKey(0)
    cv.destroyAllWindows()
def convertToRelative(xsize, ysize, bb):
    

    
    #Maths to convert to relative form
    #convert x1 y1 a b into relative x1 y1 x2 y2
    classID = bb[0]
    
    if classID > 1:
        print('error')
        return()
    else:
        x1 = float(bb[1]) / xsize
        x2 = float(bb[3]) / xsize
        
        y1 = float(bb[2]) / ysize
        y2 = float(bb[4]) / ysize
        
        if x1 < 0:
            x1 = 0
        elif x2 > 1:
            x2 = 1
            
        if y1 < 0:
            y1 = 0
        elif y2 > 1:
            y2 = 1
        
        #Takes the average of x1 and x2, y1 and y2 respectivley for each box to find center x and y
        xcenter = (x1 + x2)/2
        ycenter = (y1 + y2)/2
        
        width = x2 - x1
        height = y2 - y1
    
        if xcenter < 0:
            xcenter = 0
        elif xcenter > 1:
            xcenter = 1
            
        if ycenter < 0:
            ycenter = 0
        elif ycenter > 1:
            ycenter = 1
            
    
        bbOut = [classID, xcenter, ycenter, width, height]
    
        return(bbOut)
def convertToPixel(image, dataFile):


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
    
def rowGrouping(usefulBoxes):
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
        
        if rowLength[rowNum] == 0:
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
            
            rowLength[rowNum] += 1
        
        #Checks if the box is within the row and adjusts the start and end plaements
        elif y1 > rowStartY - 50 and y1 < rowStartY + 50:
            
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
            rowPositions.append([rowStartX, rowStartY, rowEndX, rowEndY])
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
            rowNum += 1
            rowLength.append(1)

        if totalCount >= len(usefulBoxes):
            rowPositions.append([rowStartX, rowStartY, rowEndX, rowEndY])
            rowStartY = y1
            rowStartX = x1
            
            rowEndY = y2
            rowEndX = x2
            
    return(rowPositions)

def boxExpansion(rowPositions, rowLength, boxes):
    
    #EXPANSION
    saveDir = os.path.join(usefulBoxDir, dataName)
    expansionSizes = []
    
    for i in range(len(rowPositions)):
        if i == 0:
            bottomExpansion = 0.5 * (rowPositions[i + 1][1] - rowPositions[i][3])
            
            topExpansion = bottomExpansion
            
            expansionSizes.append((topExpansion, bottomExpansion))
            
        elif i + 1 < len(rowPositions):
            bottomExpansion = 0.5 * (rowPositions[i + 1][1] - rowPositions[i][3])
            
            
            topExpansion = expansionSizes[i - 1][1]
            
            expansionSizes.append((topExpansion, bottomExpansion))
            
        else:
            
            
            topExpansion = expansionSizes[i - 1][1]
            bottomExpansion = topExpansion
            
            expansionSizes.append((topExpansion, bottomExpansion))
        
        rowPositions[i][1] -= topExpansion + 20
        rowPositions[i][3] += bottomExpansion + 20
        
    expandedBoxes = []
    boxNumber = 0
    for i in range(len(rowLength)):
        for j in range(rowLength[i]):
            
            expandedBox = [boxes[boxNumber][0], boxes[boxNumber][1], rowPositions[i][1], boxes[boxNumber][3], rowPositions[i][3]]
            boxNumber += 1
            
            expandedBoxes.append(expandedBox)
    
    
    '''
    with open(saveDir, "w") as w:
        
        print(len(expandedBoxes))
        counter = 1
        for box in expandedBoxes:
            print(box)
            if counter < len(expandedBoxes):
                w.write("{}, {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(int(box[0]), box[1], box[2], box[3], box[4]) + "\n")
            else:
                w.write("{}, {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(int(box[0]), box[1], box[2], box[3], box[4]))
                
            counter += 1
    '''
    return(expandedBoxes)
    #print(expandedBoxes)
    
    
def checkNotesInBox(image, box = [0]):
    
    dataName = image.replace('.png', '.txt')

    noteData = os.path.join(noteDetectionDir, dataName)
    
    
    saveDir = os.path.join(usefulBoxDir, dataName)
    imageWithDir = os.path.join(imageDir, image)
    
    
    noteList = convertToPixel(imageWithDir, noteData)
    
    if box[0] == 0:
        boxData = os.path.join(staffDetectionDir, dataName)
        boxList = convertToPixel(imageWithDir, boxData)
    else:
        boxList = box

    iteration = 0
    for box in boxList:
        
        notesInBox = []
        usefulBox = False
        for note in noteList:
            #Checks if the note's left x is < the boxes right x and if the note's right x is > the boxes right x\
                
            fiftyPercentX = (note[3] - note[1])/2
            fiftyPercentY = (note[4] - note[2])/2
                
            if note[1] + fiftyPercentX > box[1] and note[3] - fiftyPercentX < box[3]:
                #Checks if the note's top y is < the boxes bottom y and the note's bottom y is > the boxes top y
                if note[2] + fiftyPercentY > box[2] and note[4] - fiftyPercentY < box[4]:
            
                    
                    usefulBox = True
                    
                    noteX1 = note[1] - box[1]
                    noteX2 = note[3] - box[1]
                    
                    noteY1 = note[2] - box[2]
                    noteY2 = note[4] - box[2]
                    
                    print(noteX1, noteX2, noteY1, noteY2)
                    
                    
                    
                    noteInBox = [note[0], noteX1, noteY1, noteX2, noteY2]
                    
                    boxX = box[3] - box[1]
                    boxY = box[4] - box[2]
                    
                    print('boxX - ', boxX, ' boxY - ', boxY)
                    
                    print('-')
                    
                    relativeNoteToBox = convertToRelative(boxX, boxY, noteInBox)
                    
                    notesInBox.append(relativeNoteToBox)                    
        
        if usefulBox == True:
            imageName = cropper(image, iteration, box)
            
            noteName = imageName.replace('.png', '.txt')
            
            saveDir = os.path.join(usefulBoxDir, noteName)
            
            with open(saveDir, "w") as w:
                
                counter = 1
                for box in notesInBox:
                    if counter < len(notesInBox):
                        w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(int(box[0]), box[1], box[2], box[3], box[4]) + "\n")
                    else:
                        w.write("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(int(box[0]), box[1], box[2], box[3], box[4]))
                        
                    counter += 1
            
            iteration += 1
            usefulBoxes.append(box)
            
    return usefulBoxes
    #Uncomment to save sorted bounding boxes        
    

    
    
def getStaffBoxes(image):
    imageWithDir = os.path.join(imageDir, image)

    dataName = image.replace('.png', '.txt')

    boxData = os.path.join(staffDetectionDir, dataName)
    boxList = convertToPixel(imageWithDir, boxData)
    
    return boxList

def cropper(image, iteration, boxPosition):
    
    
    imageWithDir = os.path.join(imageDir, image)
    
    img = cv.imread(imageWithDir)
    
    boundingBoxCrop = img[int(boxPosition[2]):int(boxPosition[4]), int(boxPosition[1]):int(boxPosition[3])]
    
    croppedName = image.replace('.png', str(iteration) + '.png')
    cv.imwrite(os.path.join(saveDir, croppedName), boundingBoxCrop)

    return(croppedName)
def cropFullImage(image, boxes):
    iteration = 0
    for box in boxes:
        cropper(image, iteration, box)
        iteration += 1

for image in os.listdir(imageDir):

    if '.png' in image:
        dataName = image.replace('.png', '.txt')

        boxData  = os.path.join(staffDetectionDir, dataName)
        noteData = os.path.join(noteDetectionDir, dataName)
        
        imageDirect = r"C:\Users\Mason\Desktop\ml\2013\testImage"
  
        imageWithDir = os.path.join(imageDirect, image)

        print(dataName)
        print(imageWithDir)
        
        
        boxes = getStaffBoxes(image)
        
        
        showBoxesOnImage(imageWithDir, rowGrouping(boxes))
        
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


    


