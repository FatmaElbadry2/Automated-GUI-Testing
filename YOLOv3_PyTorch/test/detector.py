from __future__ import division

from nets.model_main import ModelMain
from nets.yolo_loss import YOLOLoss
from common.utils import *
import torch
import pandas as pd
import pickle as pkl
import cv2
import os.path as osp
import os
import random
import importlib
from collections import OrderedDict

params_path = "params.py"
config = importlib.import_module(params_path[:-3]).TRAINING_PARAMS
weights = config["pretrain_snapshot"]
anchors = config["yolo"]["anchors"]
num_classes = config["yolo"]["classes"]
yolo_w = config["img_w"]
yolo_h = config["img_h"]
class_names = config["classes_names_path"]
conf_thres = config["confidence_threshold"]

classes = 36
class_names = open("../data/custom.names", "r").read().split("\n")[:-1]

model = ModelMain(config, is_training=False)
model.train(False)

if weights:
    state_dict = torch.load(weights)

    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]
        new_state_dict[name] = v
    model.load_state_dict(new_state_dict)
else:
    raise Exception("missing pretrain_snapshot!!!")

# YOLO loss with 3 scales
yolo_losses = []
for i in range(3):
    yolo_losses.append(YOLOLoss(anchors[i], num_classes, (yolo_w, yolo_h)))

image_list = ["images/Apprentice_Video(10).jpg"]

if not os.path.exists("detections"):
    os.makedirs("detections")

loaded_images = [cv2.imread(image) for image in image_list]

dataset_images = list(map(image_preprocessing, loaded_images, [yolo_w for image in range(len(image_list))]))

dataset_images_dim = [(image.shape[1], image.shape[0]) for image in loaded_images]
dataset_images_dim = torch.FloatTensor(dataset_images_dim).repeat(1, 2)



dataset_images =[image.unsqueeze(0) for image in dataset_images]
dataset_images = torch.FloatTensor(dataset_images[0])
with torch.no_grad():
    outputs = model(dataset_images)
    output_list = []
    for i in range(3):
        output_list.append(yolo_losses[i](outputs[i]))
    output = torch.cat(output_list, 1)
    detections = non_max_suppression(output, num_classes, conf_thres=conf_thres, nms_thres=0.45)

scaling_factor = torch.min(yolo_w/dataset_images_dim[0:2], 1)[0]


detections[0][:, 0] -= (yolo_w - scaling_factor*dataset_images_dim[0][0]) / 2
detections[0][:, 2] -= (yolo_w - scaling_factor*dataset_images_dim[0][0]) / 2
detections[0][:, 1] -= (yolo_w - scaling_factor*dataset_images_dim[0][1]) / 2
detections[0][:, 3] -= (yolo_w - scaling_factor*dataset_images_dim[0][1]) / 2

detections[0][:, 0:4] /= scaling_factor

for i in range(detections[0].size(0)):
    detections[0][i, 0] = torch.clamp(detections[0][i, 0], 0.0, dataset_images_dim[0][0])
    detections[0][i, 2] = torch.clamp(detections[0][i, 2], 0.0, dataset_images_dim[0][0])
    detections[0][i, 1] = torch.clamp(detections[0][i, 1], 0.0, dataset_images_dim[0][1])
    detections[0][i, 3] = torch.clamp(detections[0][i, 3], 0.0, dataset_images_dim[0][1])


colors = pkl.load(open("../common/pallete", "rb"))


def draw_bb(x, results):
    img = results
    for i in x:
        c1 = (int(i[0].item()), int(i[1].item()))
        c2 = (int(i[2].item()), int(i[3].item()))
        cls = int(i[-1])
        color = random.choice(colors)
        label = "{0}".format(class_names[cls])
        cv2.rectangle(img, c1, c2, color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(img, c1, c2, color, -1)
        cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
    return img


list(map(lambda x: draw_bb(x, loaded_images[0]), detections))

cv2.imwrite("detections/{}".format(image_list[0][7:]), loaded_images[0])
torch.cuda.empty_cache()
