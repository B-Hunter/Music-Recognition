# Project Journal
## Hunter Baum
### 26 Jan 2022
## Here We Go

First Journal Entry! This project as a whole seems a bit daunting, but I am both
confident and excited to carry this out with great execution. Machine learning
is all but a couple of words to me right now. What better way to explore a 
new field than to dive right in? I have little to no experience in Python,
Pytorch, pandas, and any machine learning models. A trial by fire! 
A detailed explanation of the music-recognition project will (hopefully) be 
detailed in the "README.md" of the repository. 

So far I have been able to load/manipulate/analyze images into Python at a basic 
level. Here is an example of a program I wrote which loads an image, turns the 
image to grayscale then displays both. Immediately after it calculates and prints
the percentage of pixels with a value >= 150. A big thanks goes out to my research
partner, Chandler, who showed me how to finish the second half of the code seen
below: 

image = Image.open("pyimg.png")
image.show()

gray = image.convert('L')
gray.show()
gray.save('grayPy.png')

width, height = image.size
print(width, height)



count = 0
for x in range(gray.height):
  for y in range(gray.width):
    pixel = gray.getpixel((x, y))
    if pixel >= 150:
      count += 1

print(count)

pixelPer = (count / (width * height)) * 100

print(pixelPer, "%")


Python syntax is much more simple/clean than what I am accustomed to with Java. I 
feel like this is going to be a blessing and a curse in terms of organization, only 
time will tell.

