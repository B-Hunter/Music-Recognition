import numpy as np
import cv2
from PIL import Image


staff = cv2.imread('staff.png', 1)

def coord_click():
    # function to display the coordinates of
    #    of the points clicked on the image
    coordinates = []
    def click_event(event, x, y, flags, params):
        
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.imshow('Staff', staff)

            coordinates.append((x, y))

    if __name__ == "__main__":
        cv2.imshow('Staff', staff)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Staff', click_event)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return coordinates


def buffer_generator(T, image):	
    white_val = [0, 255, 0]
    # loop over the image, pixel by pixel
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            top_test_val = image[y, x]
            # threshold the pixel
            if top_test_val[1] == white_val[1]:
                buff_top = y - T
                break
        else:
            continue
        break

    for y in reversed(range(image.shape[0])):
        for x in reversed(range(image.shape[1])):
            bottom_test_val = image[y,x]
            # threshold the pixel
            if bottom_test_val[1] == white_val[1]:
                buff_bot = y + T
                break
        else:
            continue
        break       

    return buff_top, buff_bot


image_coordinates = coord_click()


print('Coordinates: ', image_coordinates)

cv2.imshow('Rectangle', staff)
cv2.waitKey(0)
snip = staff[image_coordinates[0][1]:image_coordinates[1][1], image_coordinates[0][0]:image_coordinates[1][0]]
cv2.imshow('snippet', snip)
cv2.waitKey(0)
height = snip.shape[0]
width = snip.shape[1]

y_top, y_bot = buffer_generator(10, snip)
print(y_top, y_bot)
final_y = y_top + image_coordinates[0][1] 
final_y_bot = y_bot + image_coordinates[1][1]
print('final y top ' , final_y)
print('final y bottom', final_y_bot)
snip_2 = staff[final_y:(image_coordinates[0][1]+(final_y_bot - image_coordinates[1][1])), image_coordinates[0][0]:image_coordinates[1][0]]
cv2.imshow('thisone', snip_2)
cv2.waitKey()
cv2.destroyAllWindows()
exit()
