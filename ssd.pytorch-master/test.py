from __future__ import print_function
import sys
import os
import random
import argparse
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
from torch.autograd import Variable
from data import CUSTOM_ROOT, CUSTOM_CLASSES as labelmap
from PIL import Image
from data import CUSTOMAnnotationTransform, CUSTOMDetection, BaseTransform, CUSTOM_CLASSES
import torch.utils.data as data
from ssd import build_ssd
from data.config import COLORS
from data.custom_dataset import CUSTOM_CLASSES
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

# parser = argparse.ArgumentParser(description='Single Shot MultiBox Detection')
# parser.add_argument('--trained_model', default='weights/ssd_300_VOC0712.pth',
#                     type=str, help='Trained state_dict file path to open')
# parser.add_argument('--save_folder', default='eval/', type=str,
#                     help='Dir to save results')
# parser.add_argument('--visual_threshold', default=0.6, type=float,
#                     help='Final confidence threshold')
# parser.add_argument('--cuda', default=True, type=bool,
#                     help='Use cuda to train model')
# parser.add_argument('--voc_root', default=VOC_ROOT, help='Location of VOC root directory')
# parser.add_argument('-f', default=None, type=str, help="Dummy arg so we can load in Jupyter Notebooks")
# args = parser.parse_args()

trained_model = 'weights/ssd300_CUSTOM_final1000.pth'
save_folder = 'eval/'
visual_threshold = 0.6
cuda = True
custom_root = CUSTOM_ROOT

if cuda and torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')

if not os.path.exists(save_folder):
    os.mkdir(save_folder)


def test_net(save_folder, net, cuda, testset, transform, thresh):
    # dump predictions and assoc. ground truth to text file for now
    filename = save_folder+'test1.txt'
    num_images = len(testset)
    for i in range(num_images):
        print('Testing image {:d}/{:d}....'.format(i+1, num_images))
        img = testset.pull_image(i)
        img_id, annotation = testset.pull_anno(i)
        x = torch.from_numpy(transform(img)[0]).permute(2, 0, 1)
        x = torch.FloatTensor(x.unsqueeze(0))

        with open(filename, mode='a') as f:
            f.write('\nGROUND TRUTH FOR: '+img_id+'\n')
            for box in annotation:
                f.write('label: '+' || '.join(str(b) for b in box)+'\n')
        if cuda:
            x = x.cuda()

        y = net(x)      # forward pass
        detections = y.data
        # scale each detection back up to the image
        scale = torch.Tensor([img.shape[1], img.shape[0],
                             img.shape[1], img.shape[0]])
        pred_num = 0
        plt.figure()
        fig, ax = plt.subplots(1)
        ax.imshow(img)
        for idx in range(detections.size(1)):
            j = 0
            while detections[0, idx, j, 0] >= 0.6:
                color = random.choice(COLORS)
                color = tuple(ti/255 for ti in color)
                if pred_num == 0:
                    with open(filename, mode='a') as f:
                        f.write('PREDICTIONS: '+'\n')
                score = detections[0, idx, j, 0]
                label_name = labelmap[idx-1]
                pt = (detections[0, idx, j, 1:]*scale).cpu().numpy()
                coords = (pt[0], pt[1], pt[2], pt[3])
                # Create a Rectangle patch
                bbox = patches.Rectangle((pt[0], pt[1]), pt[2], pt[3], linewidth=2,
                                         edgecolor=color,
                                         facecolor='none')
                # Add the bbox to the plot
                ax.add_patch(bbox)
                # Add label
                plt.text(pt[0], pt[1], s=label_name, color='white',
                         verticalalignment='top',
                         bbox={'color': color, 'pad': 0})
                pred_num += 1
                with open(filename, mode='a') as f:
                    f.write(str(pred_num)+' label: '+label_name+' score: ' +
                            str(score) + ' '+' || '.join(str(c) for c in coords) + '\n')
                j += 1
        plt.axis('off')
        plt.gca().xaxis.set_major_locator(NullLocator())
        plt.gca().yaxis.set_major_locator(NullLocator())
        plt.savefig(r'C:\Users\Hagar\Downloads\ssd.pytorch-master\eval\output/{}.jpg'.format(i), bbox_inches='tight', pad_inches=0.0)
        plt.close()


def test_custom():
    # load net
    num_classes = len(CUSTOM_CLASSES) + 1 # +1 background
    net = build_ssd('test', 300, num_classes) # initialize SSD
    net.load_state_dict(torch.load(trained_model))
    net.eval()
    print('Finished loading model!')
    # load data
    testset = CUSTOMDetection(custom_root, [('val')], None, CUSTOMAnnotationTransform())
    if cuda:
        net = net.cuda()
        cudnn.benchmark = True
    # evaluation
    test_net(save_folder, net, cuda, testset,
             BaseTransform(net.size, (104, 117, 123)),
             thresh=visual_threshold)

if __name__ == '__main__':
    test_custom()
