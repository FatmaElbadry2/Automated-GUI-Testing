from __future__ import division

import torch
import numpy as np
import cv2
import string


def read_cfg(cfg_file):
    cfg = open(cfg_file, 'r')
    lines = cfg.readlines()
    lines = [line for line in lines if line != "\n"]
    lines = [line for line in lines if line[0] != "#"]
    lines = [line.translate({ord(unwanted_char): None for unwanted_char in string.whitespace}) for line in lines]

    modules = []
    module = {}

    for line in lines:
        if line[0] == "[":
            if len(module) != 0:
                modules.append(module)
            module = {}
            module["type"] = line[1:len(line) - 1]
            continue
        else:
            module[line.split("=")[0]] = line.split("=")[1]
    modules.append(module)
    return modules


def load_classes(classes_file):
    file = open(classes_file, "r")
    classes = file.read().split("\n")

    return classes


def resize_image(image, input_size):
    orig_h, orig_w = image.shape[0], image.shape[1]
    h = w = input_size
    new_h = round(orig_h * min(h / orig_h, w / orig_w))
    new_w = round(orig_w * min(h / orig_h, w / orig_w))
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    canvas = np.full((h, w, 3), 128)
    canvas[(h-new_h) // 2:(h-new_h) // 2 + new_h, (w-new_w) // 2:(w-new_w) // 2 + new_w, :] = resized_image

    return canvas


def image_preprocessing(image, input_size):
    image = (resize_image(image, input_size))
    image = image[:, :, ::-1].transpose((2, 0, 1)).copy()
    image = torch.from_numpy(image).float().div(255.0).unsqueeze(0)
    image = image.cuda()

    return image


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
    x, y = np.meshgrid(grid, grid)

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


def unique(classes):
    classes_np = classes.cpu().numpy()
    unique_classes_np = np.unique(classes_np)
    unique_classes_tensor = torch.from_numpy(unique_classes_np)

    unique_classes = classes.new(unique_classes_tensor.shape)
    unique_classes.copy_(unique_classes_tensor)
    return unique_classes


def bbox_iou(bbox1, bbox2):
    bb1_x1, bb1_y1, bb1_x2, bb1_y2 = bbox1[:, 0], bbox1[:, 1], bbox1[:, 2], bbox1[:, 3]
    bb2_x1, bb2_y1, bb2_x2, bb2_y2 = bbox2[:, 0], bbox2[:, 1], bbox2[:, 2], bbox2[:, 3]

    bb_inter_x1 = torch.max(bb1_x1, bb2_x1)
    bb_inter_y1 = torch.max(bb1_y1, bb2_y1)
    bb_inter_x2 = torch.min(bb1_x2, bb2_x2)
    bb_inter_y2 = torch.min(bb1_y2, bb2_y2)

    bb_inter_area = torch.clamp(bb_inter_x2 - bb_inter_x1 + 1, min=0) * torch.clamp(bb_inter_y2 - bb_inter_y1 + 1, min=0)

    bb1_area = (bb1_x2 - bb1_x1 + 1) * (bb1_y2 - bb1_y1 + 1)
    bb2_area = (bb2_x2 - bb2_x1 + 1) * (bb2_y2 - bb2_y1 + 1)

    IoU = bb_inter_area/(bb1_area + bb2_area - bb_inter_area)

    return IoU


def true_detections(prediction, classes, obj_thresh, nms_thresh):
    # Threshold objectness scores
    obj_mask = (prediction[:, :, 4] > obj_thresh).float().unsqueeze(2)
    prediction *= obj_mask

    # Transform bbox attributes to top-left and bottom-right corners to compute IoU more easily
    box_corners = prediction.new(prediction.shape)
    box_corners[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
    box_corners[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
    box_corners[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
    box_corners[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
    prediction[:, :, :4] = box_corners[:, :, :4]

    batch_size = prediction.size(0)

    collector = 0
    for image in range(batch_size):
        image_pred = prediction[image]

        # Removing all class scores except max. score
        max_class_scores, max_class_indices = torch.max(image_pred[:, 5:5 + classes], 1)
        max_class_scores = max_class_scores.float().unsqueeze(1)
        max_class_indices = max_class_indices.float().unsqueeze(1)
        image_pred = torch.cat((image_pred[:, :5], max_class_scores, max_class_indices), 1)

        # Removing all bboxes with a zero objectness score
        non_zero_indices = torch.nonzero(image_pred[:, 4])
        try:
            image_predict = image_pred[non_zero_indices.squeeze(), :].view(-1, 7)
        except:
            continue

        if image_predict.shape[0] == 0:
            continue

        image_classes = unique(image_predict[:, -1])

        for cls in image_classes:
            class_mask = image_predict * (image_predict[:, -1] == cls).float().unsqueeze(1)
            class_mask_indices = torch.nonzero(class_mask[:, -2]).squeeze()
            image_pred_class = image_predict[class_mask_indices].view(-1, 7)

            desc_obj_indices = torch.sort(image_pred_class[:, 4], descending=True)[1]
            image_pred_class = image_pred_class[desc_obj_indices]
            num_class_detections = image_pred_class.size(0)

            for detection in range(num_class_detections):
                try:
                    IoUs = bbox_iou(image_pred_class[detection].unsqueeze(0), image_pred_class[detection + 1:])
                except ValueError:
                    break
                except IndexError:
                    break

                IoU_mask = (IoUs < nms_thresh).float().unsqueeze(1)
                image_pred_class[detection + 1:] *= IoU_mask

                non_zero_indices = torch.nonzero(image_pred_class[:, 4]).squeeze()
                image_pred_class = image_pred_class[non_zero_indices].view(-1, 7)

            batch_index = image_pred_class.new(image_pred_class.size(0), 1).fill_(image)

            if not collector:
                output = torch.cat((batch_index, image_pred_class), 1)
                collector = 1
            else:
                out = torch.cat((batch_index, image_pred_class), 1)
                output = torch.cat((output, out))

    try:
        return output
    except:
        return 0
