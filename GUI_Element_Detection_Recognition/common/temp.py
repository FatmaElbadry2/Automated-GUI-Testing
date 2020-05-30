import os
import os.path as osp

image_list = [osp.join("C:/Users/Hagar/Desktop/GP/Automated-GUI-Testing/GUI_Element_Detection_Recognition/data/images", str(image))
              for image in os.listdir("C:/Users/Hagar/Desktop/GP/Automated-GUI-Testing/GUI_Element_Detection_Recognition/data/images")]
with open('C:/Users/Hagar/Desktop/GP/Automated-GUI-Testing/GUI_Element_Detection_Recognition/data/train.txt', 'w') as f:
    for item in image_list:
        f.write("%s\n" % item)
