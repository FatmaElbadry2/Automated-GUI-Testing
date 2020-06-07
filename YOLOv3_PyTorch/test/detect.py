# coding='utf-8'
import os
import sys
import numpy as np
import importlib
import cv2
import random
from imports import MY_DIRNAME
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator
from collections import OrderedDict
import torch
import torch.nn as nn


DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(DIRNAME, '..'))

from nets.model_main import ModelMain
from nets.yolo_loss import YOLOLoss
from common.utils import non_max_suppression

cmap = plt.get_cmap('tab20b')
colors = [cmap(i) for i in np.linspace(0, 1, 20)]

params_path = "params.py"
config = importlib.import_module(params_path[:-3]).TRAINING_PARAMS
model = config["pretrain_snapshot"]
anchors = config["yolo"]["anchors"]
num_classes = config["yolo"]["classes"]
yolo_w = config["img_w"]
yolo_h = config["img_h"]
class_names = config["classes_names_path"]
conf_thres = config["confidence_threshold"]


def detect(image_path,image_name):
    is_training = False
    # Load and initialize network
    net = ModelMain(config, is_training=is_training)
    net.train(is_training)

    # Set data parallel
    # net = nn.DataParallel(net)
    # net = net.cuda()

    # Restore pretrain model
    if model:
        if torch.cuda.is_available():
            map_location = lambda storage, loc: storage.cuda()
        else:
            map_location = 'cpu'
        state_dict = torch.load(model,map_location=map_location)

        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:]
            new_state_dict[name] = v
        net.load_state_dict(new_state_dict)
    else:
        raise Exception("missing pretrain_snapshot!!!")

    # YOLO loss with 3 scales
    yolo_losses = []
    for i in range(3):
        yolo_losses.append(YOLOLoss(anchors[i], num_classes, (yolo_w, yolo_h)))

    original_image = []
    images_origin = []

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    images_origin.append(image)  # keep for save result
    image = cv2.resize(image, (yolo_w, yolo_h),
                       interpolation=cv2.INTER_LINEAR)
    image = image.astype(np.float32)
    image /= 255.0
    image = np.transpose(image, (2, 0, 1))
    image = image.astype(np.float32)
    original_image.append(image)
    images = np.asarray(original_image)
    images = torch.from_numpy(images)
    # inference
    with torch.no_grad():
        outputs = net(images)
        output_list = []
        for i in range(3):
            output_list.append(yolo_losses[i](outputs[i]))
        output = torch.cat(output_list, 1)
        detections = non_max_suppression(output, num_classes, conf_thres=conf_thres, nms_thres=0.45)

    # write result images. Draw bounding boxes and labels of detections
    classes = open(class_names, "r").read().split("\n")[:-1]
    if not os.path.isdir("./output/"):
        os.makedirs("./output/")

    plt.figure()
    fig, ax = plt.subplots(1)
    ax.imshow(images_origin[0])
    if detections is not None:
        unique_labels = detections[0][:, -1].cpu().unique()
        n_cls_preds = len(unique_labels)
        actual_detections = []
        bbox_colors = random.sample(colors, n_cls_preds)
        for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections[0]:
            detection = []
            color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
            # Rescale coordinates to original dimensions
            ori_h, ori_w = images_origin[0].shape[:2]
            pre_h, pre_w = yolo_h, yolo_w
            box_h = ((y2 - y1) / pre_h) * ori_h
            box_w = ((x2 - x1) / pre_w) * ori_w
            y1 = (y1 / pre_h) * ori_h
            x1 = (x1 / pre_w) * ori_w
            # Create a Rectangle patch
            bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor='none')
            # Add the bbox to the plot
            ax.add_patch(bbox)
            # Add label
            plt.text(x1, y1, s=classes[int(cls_pred)], color='white', verticalalignment='top',
                     bbox={'color': color, 'pad': 0})
            detection.append(cls_pred.item())
            detection.append(x1.item())
            detection.append(y1.item())
            detection.append(box_w.item())
            detection.append(box_h.item())
            actual_detections.append(detection)
        # Save generated image with detections
        plt.axis('off')
        plt.gca().xaxis.set_major_locator(NullLocator())
        plt.gca().yaxis.set_major_locator(NullLocator())
        plt.savefig('output/'+image_name.format(image_path[7:-4]), bbox_inches='tight', pad_inches=0.0)
        plt.close()

        return actual_detections


print("starting...")
detections = detect(str(MY_DIRNAME) + "\\YOLOv3_PyTorch\\test\\images\\Apprentice_Video(11).jpg",'Apprentice_Video(11).jpg')
print(detections)


# if __name__ == "__main__":
#     main()
