import os
import os.path as osp

image_list = [osp.join(r"C:\Users\Hagar\Downloads\YOLOv3_PyTorch-master\data\images", str(image))
              for image in os.listdir(r"C:\Users\Hagar\Downloads\YOLOv3_PyTorch-master\data\images")]
with open(r'C:\Users\Hagar\Downloads\YOLOv3_PyTorch-master\data\train.txt', 'w') as f:
    for item in image_list:
        f.write("%s\n" % item)
