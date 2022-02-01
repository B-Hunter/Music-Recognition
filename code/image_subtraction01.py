import numpy as np
import cv2

orig = cv2.imread('p002_bina_l10_3D.png')
nostaff = cv2.imread('p002_nostaff_l10_3D.png')

staff = cv2.subtract(orig, nostaff)

cv2.imshow('Staff.jpg', staff)

cv2.waitKey(0)

cv2.destroyAllWindows()

