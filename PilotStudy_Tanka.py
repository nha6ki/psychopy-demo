import time
import pandas as pd
from psychopy import visual, core


DATASET_DIR = './tanka_images/'

ids = list(range(1,102))
images_path = [DATASET_DIR+'image'+str(i)+'.png' for i in ids]

# Setting window & image size
win_width = 1080
win_height = 1080
img_width = int(win_width*0.65/2)
img_height = int(win_height*0.65)

rating_values = []
reaction_times = []
win = visual.Window(size=[win_width,win_height], units='pix')
stim_num = 10 # all: len(images_path)==101
for image_idx in range(stim_num):
    # Display image
    img = visual.ImageStim(win, images_path[image_idx])
    img.setSize([img_width,img_height])
    img.setPos([0,0])
    img.draw()
    
    # Display rating slider
    values = list(range(1,8))
    rating_slider = visual.Slider(win, ticks=values, labels=values, size=[250,25], pos=[0,-400], style='rating', font='Helvetica')
    rating_slider.draw()
    
    win.flip()
    start_time = time.time()
    
    # Get rating value
    while True:
        if rating_slider.getMouseResponses() is not None:
            rating_value = rating_slider.getRating()
            rating_values.append(rating_value)
            
            reaction_time = time.time() - start_time
            reaction_times.append(reaction_time)
            
            break
        else:
            img.draw()
            rating_slider.draw()
            win.flip()
    
    core.wait(1)
    
win.close()

# Save rating_values & reaction_times
d = {'image_path': images_path[:stim_num], 'rating_value': rating_values, 'reaction_time [s]': reaction_times}
df = pd.DataFrame(data=d, index=ids[:stim_num])
df.index.name = 'ID'
df.to_csv('result.csv')
