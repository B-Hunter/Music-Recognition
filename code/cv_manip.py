import numpy as np
import cv2

coordinates = []
staff = cv2.imread('staff.png', 1)
def coord_click():
    # function to display the coordinates of
    #    of the points clicked on the image

    def click_event(event, x, y, flags, params):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:

            # displaying the coordinates
            # on the Shell
            print(x, ' ', y)
            # displaying the coordinates
            # on the image window
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(staff, str(x) + ',' +
            #             str(y), (x, y), font,
            #             1, (255, 0, 0), 2)
            cv2.imshow('Staff', staff)
            coordinates.append((x, y))

    if __name__ == "__main__":

        cv2.imshow('Staff', staff)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('Staff', click_event)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

coord_click()

print(coordinates)
cv2.rectangle(staff, coordinates[0], coordinates[1], (0, 255, 0), 2)

cv2.imshow('Rectangle', staff)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()