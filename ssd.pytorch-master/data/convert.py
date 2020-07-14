# import os
# import os.path as osp
# import cv2
# import numpy as np
#
# image_list = [osp.join('images', image) for image in os.listdir('CUSTOMdevkit/images')]
# images = [cv2.imread(image) for image in image_list]
# image_dim = [(image.shape[1], image.shape[0]) for image in images ]
#
# label_list = [osp.join('labels', label) for label in os.listdir('CUSTOMdevkit/labels')]
# labels = [np.loadtxt(label, dtype=float, delimiter=' ') for label in label_list]
# new_labels = []
# for ind in range(len(labels)):
#     dim = image_dim[ind]
#     label = labels[ind]
#     width = dim[0]
#     height = dim[1]
#     new_label = []
#     for l in label:
#         xmin = l[1] - l[3]/2
#         ymin = l[2] - l[4]/2
#         xmax = l[1] + l[3]/2
#         ymax = l[2] + l[4]/2
#         row = [int(xmin*width), int(ymin*height), int(xmax*width), int(ymax*height), int(l[0])]
#         row = np.array(row)
#         new_label.append(row)
#     new_label = np.array(new_label)
#     new_labels.append(new_label)
#     np.savetxt(label_list[ind], new_label, fmt='%3d')

from glob import glob
import cv2
pngs = glob('CUSTOMdevkit/JPEGImages/*.png')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'jpg', img)
