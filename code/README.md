# Music Recognition Training Data
>Version 1.05

Trainingcutter.py will take input GT and BW images and create bounding boxes for training data to be used in staff recognition. Do not dump images into main directory. training cutter will copy them out of other directories listed below and delete them when they are no longer needed.


# Directory

Your main directory will be named **MusicRecognition**. Additional folders needed are:
- **xy1xy2**
>This will store output .txt files [x1, y1, x2, y2] form
-  **xywh**
>This will store output .txt files in [x1, y1, w, h] form
-  **Training_BW**
> This holds all Black and White Training Data
- **Training_GT**
> This holds Ground Truth Training Data
- **Training_GR**
> This holds Grey Scale Training Images

# KNOWN ERRORS AND HOW TO FIX

 ERROR: 
 cv2.error: OpenCV(4.5.5) /Users/xperience/actions-runner/_work/opencv-python/opencv-python/opencv/modules/highgui/src/window.cpp:1000: error: (-215:Assertion failed) size.width>0 && size.height>0 in function 'imshow'
- CAUSE: accidental double click
- FIX: don't double click

ERROR:
 UnboundLocalError: local variable 'box_top' referenced before assignment
 - CAUSE: creating bounding box in empty space
 - FIX: LINE 110 (while x2 < picWidth - x:) - make x value larger

 ERROR: UnboundLocalError: local variable 'box_top' referenced before assignment
 - CAUSE: creating bounding box in empty space
 - FIX: LINE 111 (while x2 < picWidth - 100:) - make 100 value larger
-- same type of error can happen if line 106 (while y2 < picHeight - 300:) allows for empty box to be created when moving vertically

ERROR: AttributeError: 'NoneType' object has no attribute 'shape'
- CAUSE: FILENAME is incorrect
- FIX: update FILENAME

## Version Log
1.05
- addition of file copying and pasting files to keep source clean
- bug: file will create one to many snips per staff row hanging off the edge of the screen
