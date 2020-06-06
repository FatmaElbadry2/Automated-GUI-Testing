from __future__ import division

from common.utils import *
import torch
import torch.nn as nn
import torch.nn.functional as f
import numpy as np


# Custom-Defined nn.Module Classes


class EmptyLayer(nn.Module):
    def __init__(self):
        super(EmptyLayer, self).__init__()


class DetectionLayer(nn.Module):
    def __init__(self, anchors):
        super(DetectionLayer, self).__init__()
        self.anchors = anchors


def create_nn_modules(modules):
    net_data = modules[0]
    net_modules = nn.ModuleList()
    input_filters = 3  # initially 3 representing RGB channels of the image
    output_filters = []

    for index, module in enumerate(modules[1:]):
        sub_module = nn.Sequential()

        if module["type"] == "convolutional":
            # Check for the presence of a batch normalization layer
            try:
                batch_norm = int(module["batch_normalize"])
                bias = False
            except:
                batch_norm = 0
                bias = True

            filters = int(module["filters"])
            kernel = int(module["size"])
            stride = int(module["stride"])
            pad = int(module["pad"])

            if pad:
                padding = (kernel - 1) // 2
            else:
                padding = 0

            activation = module["activation"]

            conv = nn.Conv2d(input_filters, filters, kernel, stride, padding, bias=bias)
            sub_module.add_module("Convolutional{}".format(index), conv)

            if batch_norm:
                batch = nn.BatchNorm2d(filters)
                sub_module.add_module("Batch_Normalization{}".format(index), batch)

            if activation == "leaky":
                leaky = nn.LeakyReLU(0.1, inplace=True)
                sub_module.add_module("Leaky_Activation{}".format(index), leaky)

            # if activation == "linear":
            #     linear = nn.Linear(input_filters, filters, bias=bias)
            #     sub_module.add_module("Linear_Activation{}".format(index), linear)

        elif module["type"] == "shortcut":  # Refers to a skip connection
            shortcut = EmptyLayer()
            sub_module.add_module("Skip_Connection{}", shortcut)

        elif module["type"] == "upsample":
            stride = int(module["stride"])
            # upsample = nn.UpsamplingBilinear2d(scale_factor=2)  # Bilinear Upsampling
            # upsample = nn.ConvTranspose2d()
            upsample = nn.UpsamplingNearest2d(scale_factor=stride)
            sub_module.add_module("Upsampling{}".format(index), upsample)

        elif module["type"] == "route":
            start_layer = int(module["layers"].split(",")[0])

            # If end layer exits
            try:
                end_layer = int(module["layers"].split(",")[1])
            except:
                end_layer = 0

            if start_layer > 0:
                start_layer = start_layer - index

            if end_layer > 0:
                end_layer = end_layer - index

            if end_layer < 0:
                filters = output_filters[index + start_layer] + output_filters[index + end_layer]
            else:
                filters = output_filters[index + start_layer]

            route = EmptyLayer()
            sub_module.add_module("Routing{}".format(index), route)

        elif module["type"] == "yolo":  # Detection module
            masks = module["mask"].split(",")
            masks = [int(mask) for mask in masks]
            anchors = module["anchors"].split(",")
            anchors = [float(anchor) for anchor in anchors]
            anchors = [(anchors[anchor], anchors[anchor + 1]) for anchor in range(0, len(anchors), 2)]
            anchors = [anchors[mask] for mask in masks]

            yolo = DetectionLayer(anchors)
            sub_module.add_module("YOLO{}".format(index), yolo)

        net_modules.append(sub_module)
        input_filters = filters
        output_filters.append(filters)

    return net_data, net_modules


class DarkNet(nn.Module):
    def __init__(self, cfg_file,  is_training=False):
        super(DarkNet, self).__init__()
        self.modules = read_cfg(cfg_file)
        self.net_data, self.net_modules = create_nn_modules(self.modules)
        self.is_training = is_training
        self.wf_header = None
        self.wf_images_seen = None

    def forward(self, input_, CUDA=True):
        modules = self.modules[1:]
        layer_feature_maps = {}

        collector = 0
        detections = ()
        for index, module in enumerate(modules):
            module_type = module["type"]

            if module_type == "convolutional" or module_type == "upsample":
                input_ = self.net_modules[index](input_)

            elif module_type == "shortcut":
                from_ = int(module["from"])
                # activation = module["activation"]
                #
                # x = layer_feature_maps[index + from_]
                # if activation == "linear":
                #     x = f.linear(x)

                input_ = layer_feature_maps[index-1] + layer_feature_maps[index + from_]

            elif module_type == "route":
                start_layer = int(module["layers"].split(",")[0])

                # If end layer exits
                try:
                    end_layer = int(module["layers"].split(",")[1])
                except:
                    end_layer = 0

                if start_layer > 0:
                    start_layer = start_layer - index

                if end_layer == 0:
                    input_ = layer_feature_maps[index + start_layer]
                else:
                    if end_layer > 0:
                        end_layer = end_layer - index

                    feature_map1 = layer_feature_maps[index + start_layer]
                    feature_map2 = layer_feature_maps[index + end_layer]

                    input_ = torch.cat((feature_map1, feature_map2), 1)

            elif module_type == "yolo":
                input_ = input_.data
                input_dimensions = int(self.net_data["width"])
                anchors = self.net_modules[index][0].anchors
                classes = int(module["classes"])

                if self.is_training:
                    input_.requires_grad = True
                    detections.append(input_)
                else:
                    input_ = predict_transform(input_, input_dimensions, anchors, classes, CUDA)
                    if not collector:
                        detections = input_
                        collector = 1
                    else:
                        detections = torch.cat((detections, input_), 1)

            layer_feature_maps[index] = input_

        return detections

    def load_weights(self, weights_file):
        wf = open(weights_file, "rb")
        header = np.fromfile(wf, dtype=np.int32, count=5)
        self.wf_header = torch.from_numpy(header)
        self.wf_images_seen = self.wf_header[3]

        weights = np.fromfile(wf, dtype=np.float32)

        ptr = 0
        for module in range(len(self.net_modules)):
            module_type = self.modules[module+1]["type"]

            if module_type == "convolutional":
                model = self.net_modules[module]
                conv = model[0]

                try:
                    batch_norm = int(self.modules[module + 1]["batch_normalize"])
                except:
                    batch_norm = 0

                if batch_norm:
                    bn = model[1]

                    num_bn_biases = bn.bias.numel()

                    bn_biases = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_weights = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_running_mean = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_running_var = torch.from_numpy(weights[ptr: ptr + num_bn_biases])
                    ptr += num_bn_biases

                    bn_biases = bn_biases.view_as(bn.bias.data)
                    bn_weights = bn_weights.view_as(bn.weight.data)
                    bn_running_mean = bn_running_mean.view_as(bn.running_mean)
                    bn_running_var = bn_running_var.view_as(bn.running_var)

                    bn.bias.data.copy_(bn_biases)
                    bn.weight.data.copy_(bn_weights)
                    bn.running_mean.copy_(bn_running_mean)
                    bn.running_var.copy_(bn_running_var)

                else:
                    num_conv_biases = conv.bias.numel()

                    conv_biases = torch.from_numpy(weights[ptr: ptr + num_conv_biases])
                    ptr += num_conv_biases

                    conv_biases = conv_biases.view_as(conv.bias.data)

                    conv.bias.data.copy_(conv_biases)

                num_conv_weights = conv.weight.numel()

                conv_weights = torch.from_numpy(weights[ptr: ptr + num_conv_weights])
                ptr += num_conv_weights

                conv_weights = conv_weights.view_as(conv.weight.data)

                conv.weight.data.copy_(conv_weights)
