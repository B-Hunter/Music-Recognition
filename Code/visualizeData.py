# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:59:35 2022

@author: Mason


USE THIS FILE WITH YOLOV5 FORMATTED DATA OR YOU WILL HAVE ISSUES


"""
import random
import os
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def plotBox(image, boxList):
	boxes = np.array(boxList)
	width, height = image.size

	image = image.convert('1')

	imagePlot = ImageDraw.Draw(image)

	reconvert = np.copy(boxes)
	reconvert[:, [1, 3]] = boxes[:, [1, 3]] * width
	reconvert[:, [2, 4]] = boxes[:, [2, 4]] *height

	reconvert[:, 1] = reconvert[:, 1] - (reconvert[:, 3] / 2)
	reconvert[:, 2] = reconvert[:, 2] - (reconvert[:, 4] / 2)
	reconvert[:, 3] = reconvert[:, 1] + (reconvert[:, 3])
	reconvert[:, 4] = reconvert[:, 2] + (reconvert[:, 4])

	#print(boxes)

	for x in reconvert:
		obj_cls, x1, y1, x2, y2 = x
		print(x)
		#print(x1, y1, x2, y2)
		imagePlot.rectangle((x1, y1, x2, y2), outline=0, width = 5)
		print('rectmade mate')

	plt.imshow(np.array(image))
	plt.show()
path = os.path.abspath(os.getcwd())

dataDir = os.path.join(path, "train")
#dataName = random.choice(os.listdir(dataDir))
dataName = 'GR_3000.txt'
dataFile = os.path.join(dataDir, dataName)

with open(dataFile, "r") as f:
	boxList = f.read().split("\n")
	boxList = [x.split(" ") for x in boxList]
	boxList = [[float(y) for y in x ] for x in boxList]

print(dataFile)
#imageFile = dataFile.replace("train", "Images").replace(".txt", ".png")

imageFile = dataFile.replace("train", "testImage").replace(".txt", ".png")
print(imageFile)



image = Image.open(imageFile)

plotBox(image, boxList)