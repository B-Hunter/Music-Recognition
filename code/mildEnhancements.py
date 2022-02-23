def iterate_box(image):
    [[x, y], [a, b]] = coordinates
    coordinate_list= []
   # while b < picLength:
    while a < picWidth:
            x = int(x + width / 2)
            a = int(a + width / 2)
            print(x, y, a, b)
            next_box = image[y:b, x:a]
            top_y, bot_y = buffer_generator(10, next_box)
            buffed_box = image[top_y:bot_y, x:a]
            #print('top', top_y, 'bot', bot_y)
            cv2.imshow('next', buffed_box)
            cv2.waitKey(0)
            
            
            #TODO: ADD something like this
            i =0
            coord_set = [x,y,a,b]
            coordinate_list.append(coord_set)
            i = i+1
            
            
#creates the txt documents
def coord_list_gen(coord_list): 
    coord_list.insert(0, ['x', 'y', 'a', 'b'])
    with open('coordinateList.txt', 'w') as file:
        file.write('\n'.join(str(coords) for coords in coordinated))
        
        
 # ADD to main
 coord_list_gen(coordinated)
        
        
