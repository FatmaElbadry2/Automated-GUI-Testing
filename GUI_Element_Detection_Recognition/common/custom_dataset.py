from torch.utils.data import Dataset
from utils import image_preprocessing
import numpy as np
import os
import cv2
import logging


class CustomDataset(Dataset):
    def __init__(self, data_path, img_dim):
        self.img_files = []
        self.label_files = []
        for path in open(data_path, 'r'):
            label_path = path.replace('images', 'labels').replace('.png', '.txt').replace(
                '.jpg', '.txt').strip()
            if os.path.isfile(label_path):
                self.img_files.append(path.replace('\n', ''))
                self.label_files.append(label_path)
            else:
                logging.info("no label found. skip it: {}".format(path))
        logging.info("Total images: {}".format(len(self.img_files)))
        self.img_size = img_dim
        # self.imgs = [image_preprocessing(cv2.imread(image), self.img_size) for image in self.img_files]

    def __getitem__(self, index):
        img_path = self.img_files[index % len(self.img_files)]
        # img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.imread(img_path)
        ori_h, ori_w = img.shape[:2]
        img = image_preprocessing(img, self.img_size)
        if img is None:
            raise Exception("Read image error: {}".format(img_path))

        label_path = self.label_files[index % len(self.img_files)].rstrip()
        if os.path.exists(label_path):
            labels = np.loadtxt(label_path).reshape(-1, 5)
        else:
            logging.info("label does not exist: {}".format(label_path))
            labels = np.zeros((1, 5), np.float32)

        sample = {'image': img, 'label': labels, "image_path": img_path, "origin_size": str([ori_w, ori_h])}
        return sample

    def __len__(self):
        return len(self.img_files)
