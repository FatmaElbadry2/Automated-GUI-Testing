import numpy as np
import torchvision
import time
import os
import copy
import pdb
import time
import argparse

import sys
import cv2

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms

from global_imports import MY_DIRNAME

from retinanet.dataloader import ImageLoader, CSVDataset, collater, Resizer, AspectRatioBasedSampler, Augmenter, \
	UnNormalizer, Normalizer


assert torch.__version__.split('.')[0] == '1'

print('CUDA available: {}'.format(torch.cuda.is_available()))

def detect(img_path, i):

	elements=[]

	dataset_val = ImageLoader(img_path, transform=transforms.Compose([Normalizer(), Resizer()]))

	sampler_val = AspectRatioBasedSampler(dataset_val, batch_size=1, drop_last=False)
	dataloader_val = DataLoader(dataset_val, num_workers=1, collate_fn=collater, batch_sampler=sampler_val)

	model_path = MY_DIRNAME + "\\RetinaNet\\model_final.pt"
	if not torch.cuda.is_available():
		retinanet = torch.load(model_path,map_location='cpu')
		retinanet.src_device_obj = 'cpu'
		retinanet.device_ids = []
	else:
		retinanet = torch.load(model_path)

	use_gpu = True

	if use_gpu:
		if torch.cuda.is_available():
			retinanet = retinanet.cuda()

	if torch.cuda.is_available():
		retinanet = torch.nn.DataParallel(retinanet).cuda()
	else:
		retinanet = torch.nn.DataParallel(retinanet)

	retinanet.eval()

	unnormalize = UnNormalizer()

	def draw_caption(image, box, caption):

		b = np.array(box).astype(int)
		cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
		cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

	for idx, data in enumerate(dataloader_val):

		with torch.no_grad():
			st = time.time()
			if torch.cuda.is_available():
				scores, classification, transformed_anchors = retinanet(data['img'].cuda().float())
			else:
				scores, classification, transformed_anchors = retinanet(data['img'].float())
			print('Elapsed time: {}'.format(time.time()-st))
			idxs = np.where(scores.cpu()>0.5)

			img = np.array(255 * unnormalize(data['img'][0, :, :, :])).copy()

			img[img<0] = 0
			img[img>255] = 255

			img = np.transpose(img, (1, 2, 0))

			img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2RGB)

			print("Image size after training: ", img.shape)
			print("ratio: ",  img.shape[0]/img.shape[1])

			#cv2.imwrite(MY_DIRNAME + "\\RL\\output\\image_" + str(-1) + ".png", img)
			#-----------------------------TRY-------------------------------
			R = img[:, :, 0]
			G = img[:, :, 1]
			B = img[:, :, 2]

			r = img.shape[0] - 1
			c = img.shape[1] - 1
			print(R[r][c])
			print(G[r][c])
			print(B[r][c])
			while r >= 0 and R[r][0] == 103 and G[r][0] == 116 and B[r][0] == 123:
				r -= 1
			while c >= 0 and R[0][c] == 103 and G[0][c] == 116 and B[0][c] == 123:
				c -= 1
			img = img[0:r, 0:c, :]
			print(img.shape)

			for j in range(idxs[0].shape[0]):
				bbox = transformed_anchors[idxs[0][j], :]
				x1 = int(bbox[0])
				y1 = int(bbox[1])
				x2 = int(bbox[2])
				y2 = int(bbox[3])
				label_name = dataset_val.labels[int(classification[idxs[0][j]])]
				draw_caption(img, (x1, y1, x2, y2), label_name)

				elements.append([label_name, x1, x2, y1, y2])
				if label_name == 'button':
					cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
				else:
					cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
				cv2.imwrite(MY_DIRNAME + "\\RL\\output\\image_" + str(i) + ".png", img)
				#print(label_name)

			#cv2.imshow('img', img)
			#cv2.waitKey(0)
			#return x1, y1, x2, y2

	return elements, img.shape


if __name__ == '__main__':
	elements = detect("elmerf.PNG",1)
	print(elements)