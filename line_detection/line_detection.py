import cv2 as cv
import numpy as np
import matplotlib as plot

mxb_file = 'mxb'
image_name = 'cropTest'
whole_image_name = 'p001'
image_path = r'/Users/chandlerbeitia/Repos/Music-Recognition/line_detection/'
window_name = 'window'
whole_image = image_path + whole_image_name + '.png'
cropped = image_path + image_name + '.png'
img = cv.imread(cropped)
whole_im = cv.imread(whole_image)
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
#low_thresh = 1
#high_thresh = 150

#edges = cv.Canny(gray, low_thresh, high_thresh)

#cv.imshow('Canny Applied', edges)
#cv.waitKey(0)

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
line_image = np.copy(img)
imsize = img.shape

# Hough edge detection step
lines = cv.HoughLinesP(cv.bitwise_not(blackAndWhiteImage), rho, theta, threshold, np.array([])
        , min_line, max_gap)

output_image = np.copy(whole_im)
x = np.linspace(0, imsize[1], 100)
output = []
linevals = []
for line in lines:
    for x1,y1,x2,y2 in line:
        cv.line(line_image,(x1,y1),(x2,y2),(255,0,0),3)
        linetest = [((y2 - y1) / (x2 - x1)), (y1 - ((y2 - y1) / (x2 - x1)) * x1) ]
        cv.line(output_image,((x1 + 1030),(y1 + 963)),((x2+ 1030),(y2 + 963)),(255,0,0),3)
        linevals.append(linetest[0] * x + linetest[1])
        output.append(linetest)


# place lines on image
lines_image = cv.addWeighted(img, 0.8, line_image, .8 , 1)
outputs_image = cv.addWeighted(whole_im, 0.8, output_image, .8 , 1)

cv.imshow('final output ', outputs_image)
cv.imshow('final output 2', lines_image)
cv.waitKey(0)
for y in range(len(linevals)):
        plot.pyplot.plot(x, linevals[y], '-r', label='y=2x+1')
        
plot.pyplot.title('Graph of lines from Hough Edge Detection')
plot.pyplot.xlabel('x', color='#1C2833')
plot.pyplot.ylabel('y', color='#1C2833')
plot.pyplot.grid()
plot.pyplot.show()

cv.waitKey(0)

file1 = open(image_name + '_' + mxb_file + '.txt','w')
file1.writelines('m  |  b\n')
content = str(output)
file1.writelines(content)
file1.close()

