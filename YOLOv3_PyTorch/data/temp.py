import os
import os.path as osp

image_list = [osp.join("C:/Users/Hagar/Desktop/YOLOv3_PyTorch-master/data/images", str(image))
              for image in os.listdir("C:/Users/Hagar/Desktop/YOLOv3_PyTorch-master/data/images")]
with open('train.txt', 'w') as f:
    for item in image_list:
        f.write("%s\n" % item)
