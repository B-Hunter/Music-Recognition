import numpy as np
import cv2

coordinates = []

staff = cv2.imread('staff.png', 1)
staff2 = cv2.imread('staff.png', 1)
T = 10


def coord_click():
    # function to display the coordinates of
    #    of the points clicked on the image

    def click_event(event, x, y, flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(staff, str(x) + ',' +
                        str(y), (x, y), font,
                        1, (255, 0, 0), 2)
            # displaying the coordinates
            # on the image window
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(staff, str(x) + ',' +
            #             str(y), (x, y), font,
            #             1, (255, 0, 0)
            cv2.imshow('Staff', staff)

            coordinates.append((x, y))

    if __name__ == "__main__":
        cv2.imshow('Staff', staff)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Staff', click_event)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


# def buffer_generator(T, image):
#     # loop over the image, pixel by pixel
#     for y in range(0, image.shape[0]):
#         for x in range(0, image.shape[1]):
#             # threshold the pixel
#             if image[y, x] == 255:
#                 buff_top = y - T
#
#     for y in reversed(range(0, image.shape[0])):
#         for x in reversed(range(0, image.shape[1])):
#             # threshold the pixel
#             if image[y, x] == 255:
#                 buff_bot = y + T
#
#     return buff_top, buff_bot


coord_click()


# box iterates over staff line by half-width until end of frame
def iterate_box(image):
    [[x, y], [a, b]] = coordinates
    x = int(x + width / 2)
    a = int(a + width / 2)
    print(x, y, a, b)
    next_box = staff2[y:b, x:a]
    return next_box


print('Coordinates: ', coordinates)

cv2.rectangle(staff, coordinates[0], coordinates[1], (0, 255, 0), 2)

cv2.imshow('Rectangle', staff)
cv2.waitKey(0)
cv2.destroyAllWindows()
snip = staff[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]
cv2.imshow('snippet', snip)
cv2.waitKey(0)
height = snip.shape[0]
width = snip.shape[1]
cv2.destroyAllWindows()

box = iterate_box(staff2)
cv2.imshow('please work', box)
cv2.waitKey(0)

exit()
