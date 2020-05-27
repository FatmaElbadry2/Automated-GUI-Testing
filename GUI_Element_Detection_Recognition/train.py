from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import os
import pathlib
import logging
import time
from utils import *
from nets.darknet import DarkNet
from nets.yolo_layer import YOLOLayer
from common.custom_dataset import CustomDataset
from tensorboardX import SummaryWriter

cfg_file = "cfg/yolov3-custom.cfg"
config = read_cfg(cfg_file)
model = pathlib.Path("weights/model.pth")

parameters = {
    "epochs": 160,
    "train_path": "data/train.txt",
    "batch": int(config[0]["batch"]),
    "subdivisions": int(config[0]["subdivisions"]),
    "dim": int(config[0]["width"]),
    "momentum": float(config[0]["momentum"]),
    "decay": float(config[0]["decay"]),
    "learning_rate": float(config[0]["learning_rate"]),
    "burn_in": int(config[0]["burn_in"]),
    "steps": [int(step) for step in config[0]["steps"].split(',')],
    "scales": [float(scale) for scale in config[0]["scales"].split(',')],
    "anchors": [[[116, 90], [156, 198], [373, 326]],
                    [[30, 61], [62, 45], [59, 119]],
                    [[10, 13], [16, 30], [33, 23]]],
    "classes": int(config[-1]["classes"]),
    "global_step": 0
}


def train():
    net = DarkNet(cfg_file)
    net.train(True)

    optimizer = optim.SGD(net.parameters(), lr=parameters["learning_rate"],
                          momentum=parameters["momentum"],
                          weight_decay=parameters["decay"])
    learning_rate_scheduler = optim.lr_scheduler.StepLR(optimizer, gamma=0.1, step_size=20)

    net = nn.DataParallel(net)
    net = net.cuda()

    if model.exists():
        state_dict = torch.load(model)
        net.load_state_dict(state_dict)

    yolo_losses = []
    for layer_loss in range(3):
        yolo_losses.append(YOLOLayer(parameters["anchors"][layer_loss], parameters["classes"], parameters["dim"]))

    dataset = DataLoader(CustomDataset(parameters["train_path"], parameters["dim"]),
                         batch_size=2, shuffle=True, num_workers=0, pin_memory=True)

    logging.info("Training is starting...")
    for epoch in range(parameters["epochs"]):
        for step, samples in enumerate(dataset):
            images, labels = samples["image"], samples["label"]

            start_time = time.time()
            parameters["global_step"] += 1

            optimizer.zero_grad()
            output = net(images, CUDA=True)
            # output = true_detections(output, parameters["classes"], 0.5, 0.4)
            logging.info(output)

            losses_name = ["total_loss", "x", "y", "w", "h", "conf", "cls"]
            losses = []
            for _ in range(len(losses_name)):
                losses.append([])
            for i in range(3):
                _loss_item = yolo_losses[i](output[i], labels)
                for j, l in enumerate(_loss_item):
                    losses[j].append(l)
            losses = [sum(l) for l in losses]
            loss = losses[0]
            loss.backward()
            optimizer.step()

            if step > 0 and step % 10 == 0:
                _loss = loss.item()
                duration = float(time.time() - start_time)
                example_per_second = config["batch_size"] / duration
                lr = optimizer.param_groups[0]['lr']
                logging.info(
                    "epoch [%.3d] iter = %d loss = %.2f example/sec = %.3f lr = %.5f " %
                    (epoch, step, _loss, example_per_second, lr)
                )
                SummaryWriter.add_scalar("lr", lr, parameters["global_step"])
                SummaryWriter.add_scalar("example/sec", example_per_second, parameters["global_step"])
                for i, name in enumerate(losses_name):
                    value = _loss if i == 0 else losses[i]
                    SummaryWriter.add_scalar(name, value, parameters["global_step"])

            if step > 0 and step % 1000 == 0:
                save_checkpoint(net.state_dict(), config)

        learning_rate_scheduler.step()

    save_checkpoint(net.state_dict(), config)
    logging.info("Training ended")


def save_checkpoint(state_dict):
    checkpoint_path = os.path.join("weights", "model.pth")
    torch.save(state_dict, checkpoint_path)
    logging.info("Model checkpoint saved to %s" % checkpoint_path)

train()
