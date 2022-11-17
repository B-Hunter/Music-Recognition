# Import the required Libraries
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile, askdirectory
import os
from PIL import Image
from math import floor
import cv2
import re

# we assume that the images and detection lists have the same names,
# and are stored in separate, clean folders.

def norm_to_pix(im_path, point_path):

    # first open the image we detected on for its size.
    # this is used to revert point normalization.
    im = Image.open(im_path)
    size = im._size
    im.close()

    # Get all normalized bounding boxes
    bboxes = []
    linecount = 0
    with open(point_path, mode="r", encoding="utf-8") as f:
        for line in f:
            lineout = line.split()
            bboxes.append(lineout)

    
    adj_bboxes = []
    for i in range(len(bboxes)):
        b_center_x = float(bboxes[i][1])
        b_center_y = float(bboxes[i][2])
        b_width = float(bboxes[i][3])
        b_height = float(bboxes[i][4])
        # multiply by w/h of original image
        b_center_x *= size[0]
        b_center_y *= size[1] 
        b_width    *= size[0]
        b_height   *= size[1]

        xmin = b_center_x - (b_width // 2)
        xmax = b_center_x + (b_width // 2)
        ymin = b_center_y - (b_height // 2)
        ymax = b_center_y + (b_height // 2)

        adj_bboxes.append([0, floor(xmin), floor(xmax), floor(ymin), floor(ymax)])


    return adj_bboxes

def save_partial_im(save_path, crop_coords, orig_path):

    im = cv2.imread(orig_path)

    h = abs(crop_coords[3] - crop_coords[4])
    w = abs(crop_coords[1] - crop_coords[2])
    cropImg=im[crop_coords[3]:crop_coords[3]+h,crop_coords[1]:crop_coords[1]+w]
    #cv2.imshow('cropped', cropImg)
    #cv2.waitKey(0)
    result = cv2.imwrite(save_path, cropImg)
    if result==True:
        print('File saved successfully')
    else:
        print('Error in saving file')
# this window will be used to display results
#win = Tk();
'''
# get user paths to their images and .txt files
print('\n\n'+'\033[95m'+'Choose folder with full images used in detection'+'\033[0m')
orig_im_path = askdirectory(title='Select image folder')
print('image folder path:'+'\033[96m', orig_im_path, '\033[0m' )
'''
orig_im_path = '/Users/chandlerbeitia/Repos/Music-Recognition/Code/datasets/test1/images/val/p014.png'
'''
# get user paths to their images and .txt files
print('\n\n'+'\033[95m'+'Choose folder with images'+'\033[0m')
orig_im_path = askdirectory(title='Select image folder')
print('image folder path:'+'\033[96m', orig_im_path, '\033[0m' )

print('\033[95m'+'Choose folder with detection lists (.txt files)'+'\033[0m')
detect_txt_path = askdirectory(title='Select detection folder')
print('detection txt folder path:'+'\033[96m', detect_txt_path, '\033[0m' )

imagestuff = norm_to_pix(orig_im_path + '/p014.png', detect_txt_path + '/p014.txt')
'''
orig_im_txt = '/Users/chandlerbeitia/Repos/Music-Recognition/Code/datasets/test1/labels/val/p014.txt'

cropped_path = '/Users/chandlerbeitia/Repos/Music-Recognition/Code/datasets/test1/images/cropped/p0.png'
crop_txt_path = '/Users/chandlerbeitia/Repos/Music-Recognition/Code/datasets/test1/labels/cropped/p0.txt'

crop_stuff = norm_to_pix(cropped_path, crop_txt_path)
#with open('tester.txt', "w", encoding="utf-8") as f:
#    f.write('\n'.join([' '.join(str(i)) for i in imagestuff]))
imagestuff = norm_to_pix(orig_im_path, orig_im_txt)

image = cv2.imread(orig_im_path)

if not os.path.exists(cropped_path):
   os.makedirs(cropped_path)

# get crops
for i in range(len(imagestuff)):
    #height, width, channels = image.shape
    start_point = (imagestuff[i][1], imagestuff[i][3])
    end_point = (imagestuff[i][2], imagestuff[i][4])
    color = (0,0,255)
    thickness = 5

    # cv2.rectangle(image, start_point, end_point, color, thickness)
    # this line will save the cropped images
    save_partial_im(cropped_path + '/p' + str(i) + '.png', imagestuff[i], orig_im_path)

if not os.path.exists(cropped_path):
   os.makedirs(cropped_path)


# get notes
for i in range(len(crop_stuff)):
    #height, width, channels = image.shape
    start_point = (crop_stuff[i][1] + imagestuff[i][1], crop_stuff[i][3] + imagestuff[i][3])
    end_point = (crop_stuff[i][2] + imagestuff[i][1], crop_stuff[i][4] + imagestuff[i][3])
    color = (255,0,255)
    thickness = 5

    cv2.rectangle(image, start_point, end_point, color, thickness)
    # this line will save the cropped images
    save_partial_im(cropped_path + '/test/p' + str(i) + '.png', imagestuff[i], orig_im_path)
cv2.imshow('Rectangle',image)
cv2.waitKey(0)
