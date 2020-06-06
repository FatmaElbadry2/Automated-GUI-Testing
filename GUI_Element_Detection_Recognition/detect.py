from __future__ import division

from nets.darknet import DarkNet
from common.utils import *
import torch
import pandas as pd
import pickle as pkl
import cv2
import os.path as osp
import os
import random


dataset = "test"
batch_size = 1
res = 416
conf_thresh = 0.5
nms_thresh = 0.4
cfg_file = "cfg/yolov3-custom.cfg"
weights_file = "weights/model.pth"
CUDA = torch.cuda.is_available()

classes = 36
class_names = load_classes("data/obj.names")

print("Loading the network.......")
model = DarkNet(cfg_file)
model.load_weights(weights_file)
print("Network successfully loaded")

model.net_data["width"] = str(res)
input_size = int(model.net_data["width"])
assert input_size % 32 == 0
assert input_size > 32

if CUDA:
    model.cuda()

model.eval()

try:
    # image_list = [osp.join(osp.realpath("."), dataset, image) for image in os.listdir(dataset)]
    image_list = [osp.join(dataset, image) for image in os.listdir(dataset)]
    # image_list = [dataset]
except NotADirectoryError:
    image_list = [osp.join(osp.realpath("."), dataset)]
except FileNotFoundError:
    print("No file or directory found with the name {}".format(dataset))
    exit()

if not os.path.exists("detections"):
    os.makedirs("detections")

loaded_images = [cv2.imread(image) for image in image_list]

dataset_images = list(map(image_preprocessing, loaded_images, [input_size for image in range(len(image_list))]))

dataset_images_dim = [(image.shape[1], image.shape[0]) for image in loaded_images]
dataset_images_dim = torch.FloatTensor(dataset_images_dim).repeat(1, 2)

if CUDA:
    dataset_images_dim = dataset_images_dim.cuda()

rem = 0
if len(dataset_images) % batch_size:
    rem = 1

if batch_size != 1:
    num_batches = len(dataset_images) // batch_size + rem
    dataset_images = [torch.cat((dataset_images[i * batch_size: min((i + 1) * batch_size, len(dataset_images))])) for i in range(num_batches)]

collector = 0
for i, batch in enumerate(dataset_images):

    if CUDA:
        batch = batch.cuda()

    with torch.no_grad():
        prediction = model(batch, CUDA)

    prediction = true_detections(prediction,  classes, conf_thresh, nms_thresh)

    prediction[:, 0] += i*batch_size

    if not collector:
        output = prediction
        collector = 1
    else:
        output = torch.cat((output, prediction))

    if CUDA:
        torch.cuda.synchronize()

    try:
        output
    except NameError:
        print("No detections were made")
        exit()

dataset_images_dim = torch.index_select(dataset_images_dim, 0, output[:, 0].long())

scaling_factor = torch.min(input_size/dataset_images_dim, 1)[0].view(-1, 1)


output[:, [1, 3]] -= (input_size - scaling_factor*dataset_images_dim[:, 0].view(-1, 1)) / 2
output[:, [2, 4]] -= (input_size - scaling_factor*dataset_images_dim[:, 1].view(-1, 1)) / 2

output[:, 1:5] /= scaling_factor

for i in range(output.shape[0]):
    output[i, [1, 3]] = torch.clamp(output[i, [1, 3]], 0.0, dataset_images_dim[i, 0])
    output[i, [2, 4]] = torch.clamp(output[i, [2, 4]], 0.0, dataset_images_dim[i, 1])


colors = pkl.load(open("common/pallete", "rb"))


def draw_bb(x, results):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    img = results[int(x[0])]
    cls = int(x[-1])
    color = random.choice(colors)
    label = "{0}".format(class_names[cls])
    cv2.rectangle(img, c1, c2, color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2, color, -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
    return img


list(map(lambda x: draw_bb(x, loaded_images), output))

det_names = pd.Series(image_list).apply(lambda x: "{}/det_{}".format("detections", x.split("\\")[-1]))

list(map(cv2.imwrite, det_names, loaded_images))

torch.cuda.empty_cache()
