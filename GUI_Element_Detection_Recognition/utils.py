from __future__ import division
from torch.autograd import variable
import torch
import torch.nn as nn
import torch.nn.functional as f
import numpy as np
import cv2


def predict_transform(prediction, input_size, anchors, classes, CUDA=True):
    batch_size = prediction.size(0)
    stride = input_size // prediction.size(2)
    grid_size = input_size // stride
    # grid_size = prediction.size(2)
    bbox_size = 5 + classes
    num_anchors = len(anchors)

    # Tensor Transformation

    prediction = prediction.view(batch_size, bbox_size * num_anchors, grid_size * grid_size)
    prediction = prediction.transpose(1, 2).contiguous()
    prediction = prediction.view(batch_size, grid_size * grid_size * num_anchors, bbox_size)

    anchors = [(anchor[0] / stride, anchor[1] / stride) for anchor in anchors]

    # Bounding Box Transformations

    # prediction[:, :, 0] = torch.sigmoid(prediction[:, :, 0])
    # prediction[:, :, 1] = torch.sigmoid(prediction[:, :, 1])

    grid = np.arange(grid_size)
    y, x = np.meshgrid(grid, grid)

    x_offset = torch.FloatTensor(x).view(-1, 1)
    y_offset = torch.FloatTensor(y).view(-1, 1)

    if CUDA:
        x_offset = x_offset.cuda()
        y_offset = y_offset.cuda()

    cell_offset = torch.cat((x_offset, y_offset), 1).repeat(1, num_anchors).view(-1, 2).unsqueeze(0)

    prediction[:, :, 0: 2] = torch.sigmoid(prediction[:, :, 0: 2]) + cell_offset

    anchors = torch.FloatTensor(anchors)

    if CUDA:
        anchors = anchors.cuda()

    anchors = anchors.repeat(grid_size*grid_size, 1).unsqueeze(0)

    prediction[:, :, 2: 4] = torch.exp(prediction[:, :, 2: 4]) * anchors

    prediction[:, :, 4] = torch.sigmoid(prediction[:, :, 4])
    prediction[:, :, 5: 5 + classes] = torch.sigmoid(prediction[:, :, 5: 5 + classes])

    prediction[:, :, : 4] *= stride

    return prediction
