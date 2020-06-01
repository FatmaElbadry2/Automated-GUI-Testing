from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import os
import pathlib
import logging
import time
from common.utils import *
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
    "subdivisions": 4,     # int(config[0]["subdivisions"]),
    "dim": int(config[0]["width"]),
    "momentum": float(config[0]["momentum"]),
    "decay": float(config[0]["decay"]),
    "learning_rate": float(config[0]["learning_rate"]),
    "burn_in": int(config[0]["burn_in"]),
    "steps": [int(step) for step in config[0]["steps"].split(',')],
    "scales": [float(scale) for scale in config[0]["scales"].split(',')],
    "anchors": [[[8.97,10.19], [4.25,0.53], [3.78,5.77]],
                    [[2.18,0.45], [1.26,1.35], [0.87,0.50]],
                    [[0.39,0.52], [0.26,6.07], [0.22, 0.35]]],
    "classes": int(config[-1]["classes"]),
    "global_step": 0
}

summary_dir = '{}/size{}x{}_try{}/{}'.format(
        "summary", 416, 416, parameters["global_step"],
        time.strftime("%Y%m%d%H%M%S", time.localtime()))
Summary = SummaryWriter(summary_dir)


def train():
    is_training = True
    net = DarkNet(cfg_file, is_training)
    net.train(is_training)

    for p in net.parameters():
        p.requires_grad = True

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
                         batch_size=4, shuffle=True, num_workers=0, pin_memory=True, collate_fn=collate)

    logging.info("Training is starting...")
    for epoch in range(parameters["epochs"]):
        for step, samples in enumerate(dataset):
            images, labels = samples["image"], samples["label"]
            labels = labels.cuda()
            start_time = time.time()
            parameters["global_step"] += 1

            optimizer.zero_grad()
            output = net(images, CUDA=True)
            # logging.info(output)

            loss = 0
            for i in range(3):
                layer_loss = yolo_losses[i](output[i], labels)
                loss += layer_loss[1]

            loss.backward()
            optimizer.step()

            if step > 0 and step % 10 == 0:
                _loss = loss.item()
                duration = float(time.time() - start_time)
                example_per_second = parameters["subdivisions"] / duration
                lr = optimizer.param_groups[0]['lr']
                logging.info(
                    "epoch [%.3d] iter = %d loss = %.2f example/sec = %.3f lr = %.5f" %
                    (epoch, step, _loss, example_per_second, lr)
                )
                Summary.add_scalar("lr", lr, parameters["global_step"])
                Summary.add_scalar("example/sec", example_per_second, parameters["global_step"])
                Summary.add_scalar("loss", _loss, parameters["global_step"])

            if step > 0 and step % 1000 == 0:
                save_checkpoint(net.state_dict())

            # if parameters["steps"][0] <= parameters["global_step"] \
            #         or parameters["steps"][1] <= parameters["global_step"]:
            #     learning_rate_scheduler.step()
        learning_rate_scheduler.step()
    save_checkpoint(net.state_dict())
    logging.info("Training ended")


def save_checkpoint(state_dict):
    checkpoint_path = os.path.join("weights", "model.pth")
    torch.save(state_dict, checkpoint_path)
    logging.info("Model checkpoint saved to %s" % checkpoint_path)


def main():
    # torch.multiprocessing.freeze_support()
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(asctime)s %(filename)s] %(message)s")
    train()


if __name__ == "__main__":
    main()
