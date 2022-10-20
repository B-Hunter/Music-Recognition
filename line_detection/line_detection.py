import cv2 as cv
import numpy as np
import matplotlib as plot

mxb_file = 'mxb'
image_name = 'cropTest'
image_path = r'/Users/chandlerbeitia/Repos/Music-Recognition/line_detection/' + image_name + '.png'
window_name = 'window'
img = cv.imread(image_path)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow(window_name, img)
cv.waitKey(0)

(thresh, blackAndWhiteImage) = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)


# remove noise
#kernel_size = 5
#sigma = 1 
#img_gaus = cv.GaussianBlur(img,(kernel_size, kernel_size), 0)

#cv.imshow('Gaussian Blur Applied', img_gaus)
#cv.waitKey(0)

# Apply Canny edge detection
low_thresh = 1
high_thresh = 150

edges = cv.Canny(gray, low_thresh, high_thresh)

#cv.imshow('Canny Applied', edges)
#cv.waitKey(0)

# HoughLinesP to get lines

# Distance resolution in pixels
rho = .5

# angular resolution
theta = np.pi / 90

# min number of intersections
threshold = 100

# min number of pixels in a line
min_line = 20

# max number of pixes lin a gap between line for line to continnue
max_gap = 3

# create blank image same size as image for lines to be placed on
line_image = np.copy(img) * 0

# Hough edge detection step
lines = cv.HoughLinesP(cv.bitwise_not(blackAndWhiteImage), rho, theta, threshold, np.array([])
        , min_line, max_gap)

imsize = img.shape
x = np.linspace(0, imsize[1], 100)
output = []
linevals = []
for line in lines:
    for x1,y1,x2,y2 in line:
        cv.line(line_image,(x1,y1),(x2,y2),(255,0,0),3)
        linetest = [((y2 - y1) / (x2 - x1)), (y1 - ((y2 - y1) / (x2 - x1)) * x1) ]
        linevals.append(linetest[0] * x + linetest[1])
        output.append(linetest)


# place lines on image
lines_img = cv.addWeighted(img, 0.8, line_image, .1 , 1)

cv.imshow('final output ', line_image)
cv.waitKey(0)

for y in range(len(linevals)):
        plot.pyplot.plot(x, linevals[y], '-r', label='y=2x+1')
plot.pyplot.title('Graph of y=2x+1')
plot.pyplot.xlabel('x', color='#1C2833')
plot.pyplot.ylabel('y', color='#1C2833')
plot.pyplot.legend(loc='upper left')
plot.pyplot.grid()
plot.pyplot.show()

cv.waitKey(0)

file1 = open(image_name + '_' + mxb_file + '.txt','w')
file1.writelines('m  |  b\n')
content = str(output)
file1.writelines(content)
file1.close()
