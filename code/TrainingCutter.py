import numpy as np
import cv2
import shutil
import os

FILENAME = '3003'
TYPE = 'Base'

global x1_start
coordinates = []
coordinate_list = []
xywh_list = []

T = 5


def coord_click():
    # function to display the coordinates of
    #  the points clicked on the image

    def click_event(event, x, y, flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            #font = cv2.FONT_HERSHEY_SIMPLEX
           # cv2.putText(staff, str(x) + ',' +
             # str(y), (x, y), font,
            #  1, (255, 0, 0), 2)

            cv2.imshow('Staff', staff)

            coordinates.append((x, y))
            

    if __name__ == "__main__":
        cv2.imshow('Staff', staff)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Staff', click_event)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()

# Creates buffer of snippet for every iteration over staff
def buffer_generator(T, image, x1, x2, y1, y2):
    buff_top = 0
    buff_bot = 0
    #box_top = 0
    #box_bottom = 0
    white_val = [0, 255, 0]
    # [[x, j], [a, b]] = coordinates
    # loop over the image, pixel by pixel
    for y in range(y1, y2):
        for x in range(x1, x2):
            top_test_val = image[y, x]
            # threshold the pixel
            if top_test_val[1] == white_val[1]:
                box_top = y - T
                break
        else:
            continue
        break

    for y in range(y2, y1, -1):
        for x in range(x1, x2):
            bottom_test_val = image[y, x]
            # threshold the pixel
            if bottom_test_val[1] == white_val[1]:
                box_bottom = y + T
                break
        else:
            continue
        break

    return box_top, box_bottom

# box iterates over staff line by half-width until end of frame
def iterate_box(image):
    
    [[x1, y1], [x2, y2]] = coordinates
    wid = x2 - x1
    hei = y2 - y1

    while y2 < picHeight - 100:
        while x2 < picWidth - 10:
            
            top_y = 0
            bot_y = 0
            
            while y1 != top_y and y2 != bot_y:
                if top_y != 0 or bot_y != 0:
                    y1 = top_y
                    y2 = bot_y
                top_y, bot_y = buffer_generator(30, image, x1, x2, y1, y2)
                #if(top_y == 0 and bot_y == 0):
                #    break
                buffed_box = image[top_y:bot_y, x1:x2]
                cv2.rectangle(three, [x1, y1], [x2,y2], (0, 255, 0), 2)
                cv2.rectangle(four, [x1, y1], [x2,y2], (0, 255, 0), 2)
               # cv2.imshow('Corrected Box', buffed_box)
                
            # return buffed_box
            # iterate until next staff

            i = 0
            #h = ((a - x) / 2) + x
            y1 = top_y
            y2 = bot_y
            x1 = x1+int(wid/2)
            x2 = x2+int(wid/2)
            next_box = image[top_y:bot_y, x1:x2]
            #cv2.imshow('Next Clip', next_box)
            #cv2.waitKey(0)
            coord_set = [x1+int(wid/2), top_y, x2+int(wid/2), bot_y]
            xy_wh_set = [x1+int(wid/2), top_y,(x2-x1+1),(bot_y - top_y + 1)]
            coordinate_list.append(coord_set)
            xywh_list.append(xy_wh_set)
            #coord_set = [h, top_y, a, bot_y]
            #coordinate_list.append(coord_set)
            i = i + 1

        #next_under = image[(y2 + int(hei/4)):(y2 + int((5*hei)/4)), x1_start: (x1_start + wid)]
        #cv2.imshow('NextLine', next_under)
        #cv2.waitKey(0)
        # new coordinates for next staff  line
        [[x1, y1], [x2, y2]] = [[x1_start, (y2 + int(hei/4))], [(x1_start + wid), (y2 + int((5*hei)/4))]]

        # Shows the rectangle made by the coordinates,
        
    return coordinate_list, xywh_list


# creates the txt documents
def coord_list_gen(xy1xy2_list, xywh_list):
    src_folder = r"/Users/chandlerbeitia/PycharmProjects/VIP400/MusicRegognition/"
    xy1xy2_folder = r"/Users/chandlerbeitia/PycharmProjects/VIP400/MusicRegognition/xy1xy2/"
    xywh_folder = r"/Users/chandlerbeitia/PycharmProjects/VIP400/MusicRegognition/xywh/"
    xywh_list.insert(0, ['x1', 'y2','w', 'h'])
    xy1xy2_list.insert(0, ['x1', 'y1', 'x2', 'y2'])
    with open('GR_' + FILENAME + '.txt', 'w') as file:
        file.write('\n'.join(str(coords) for coords in xy1xy2_list))
    shutil.move(src_folder + 'GR_' + FILENAME + '.txt', xy1xy2_folder)
    with open('GR_' + FILENAME + '.txt', 'w') as file:
        file.write('\n'.join(str(coords) for coords in xywh_list))
    shutil.move(src_folder + 'GR_' + FILENAME + '.txt', xywh_folder)

def open_music():
    src_folder = r"/Users/chandlerbeitia/PycharmProjects/VIP400/MusicRegognition/"
    GR_folder = r"Training_GR/"
    BW_folder = r"Training_BW/"
    GT_folder = r"Training_GT/"

    shutil.copy(GR_folder + 'GR_' + FILENAME + '.png', src_folder)
    shutil.copy(BW_folder + 'BW_' + FILENAME + '.png', src_folder)
    shutil.copy(GT_folder + 'GT_' + FILENAME + '.png', src_folder)

def delete_music():
    src_folder = r"/Users/chandlerbeitia/PycharmProjects/VIP400/MusicRegognition/"
    os.remove(src_folder + 'GR_' + FILENAME + '.png')
    os.remove(src_folder + 'BW_' + FILENAME + '.png')
    os.remove(src_folder + 'GT_' + FILENAME + '.png')


open_music()

one = cv2.imread('GT_' + FILENAME + '.png')
two = cv2.imread('BW_' + FILENAME + '.png')
three = cv2.imread('BW_' + FILENAME + '.png')
four = cv2.imread('GR_' + FILENAME + '.png')
staff = cv2.subtract(two, one)
staff2 = cv2.subtract(two, one)

picWidth = staff.shape[1]
picHeight = staff.shape[0]

# Calls click function and prints coordinate points in console
coord_click()

x1_start = coordinates[0][0]

# Shows the cropped rectangle and stores height/width
snip = staff2[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]
height = snip.shape[0]
width = snip.shape[1]
cv2.destroyAllWindows()

# Calls iterate_box function
xy1xy2_list, xywh_list = iterate_box(staff)
coord_list_gen(xy1xy2_list, xywh_list)
cv2.imshow('Rectangle', three)
cv2.imshow('Rectangle', four)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite(FILENAME + '_bounded' + '.png', three)
cv2.imwrite(FILENAME + 'grey_bounded' + '.png', four)

delete_music()

exit()
