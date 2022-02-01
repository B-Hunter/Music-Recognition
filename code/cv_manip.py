import numpy as np
import cv2

orig = cv2.imread('p002_bina_l10_3D.png')
nostaff = cv2.imread('p002_nostaff_l10_3D.png')

success = cv2.subtract(orig, nostaff)

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(staff, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('Staff', staff)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = staff[y, x, 0]
        g = staff[y, x, 1]
        r = staff[y, x, 2]
        cv2.putText(staff, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('Staff01', staff)


# driver function
if __name__ == "__main__":
    # reading the image
    staff = cv2.imread('staff.png', 1)

    # displaying the image
    cv2.imshow('Staff', staff)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('Staff', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()

