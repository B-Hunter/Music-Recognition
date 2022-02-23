import numpy as np
import cv2

coordinates = []
staff = cv2.imread('staff.png', 1)
staff2 = cv2.imread('staff.png', 1)
picWidth = staff.shape[1]
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

            cv2.imshow('Staff', staff)

            coordinates.append((x, y))

    if __name__ == "__main__":
        cv2.imshow('Staff', staff)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Staff', click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Creates buffer of snippet for every iteration over staff
def buffer_generator(T, image):
    white_val = [0, 255, 0]
    [[x, j], [a, b]] = coordinates
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
            bottom_test_val = image[y, x]
            # threshold the pixel
            if bottom_test_val[1] == white_val[1]:
                buff_bot = y + T
                break
        else:
            continue
        break

    final_y = buff_top + j  # top buffer coord
    final_y_bot = buff_bot + j  # bottom buffer coord

    return final_y, final_y_bot


# box iterates over staff line by half-width until end of frame
def iterate_box(image):
    [[x, y], [a, b]] = coordinates
    while a < picWidth:
        x = int(x + width / 2)
        a = int(a + width / 2)
        print(x, y, a, b)
        next_box = image[y:b, x:a]
        top_y, bot_y = buffer_generator(10, next_box)
        buffed_box = image[top_y:bot_y, x:a]
        print('top', top_y, 'bot', bot_y)
        cv2.imshow('next', buffed_box)
        cv2.waitKey(0)

    return buffed_box


# Calls click function and prints coordinate points in console
coord_click()
print('Coordinates: ', coordinates)

# Shows the rectangle made by the coordinates,
cv2.rectangle(staff, coordinates[0], coordinates[1], (0, 255, 0), 2)
cv2.imshow('Rectangle', staff)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Shows the cropped rectangle and stores height/width
snip = staff[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]
cv2.imshow('snippet', snip)
cv2.waitKey(0)
height = snip.shape[0]
width = snip.shape[1]
cv2.destroyAllWindows()

# Calls iterate_box function of given image
print(picWidth)
iterate_box(staff2)
# cv2.imshow('snippet', box)
# cv2.waitKey(0)

exit()
