import torch
import torch.nn as nn
from common.utils import bbox_iou


class YOLOLayer(nn.Module):

    def __init__(self, anchors, classes, img_dim=416):
        super(YOLOLayer, self).__init__()
        self.anchors = anchors
        self.num_anchors = len(anchors)
        self.classes = classes
        self.img_dim = img_dim
        self.grid_size = 0
        self.obj_scale = 1
        self.no_obj_scale = 100
        self.ignore_thresh = 0.7
        self.mse_loss = nn.MSELoss()
        self.bce_loss = nn.BCELoss()
        self.metrics = {}

    def compute_grid_offsets(self, grid_size, CUDA=True):
        self.grid_size = grid_size
        self.stride = self.img_dim / self.grid_size

        FloatTensor = torch.cuda.FloatTensor if CUDA else torch.FloatTensor

        self.x_offsets = torch.arange(grid_size).repeat(grid_size, 1).type(FloatTensor)
        self.y_offsets = torch.arange(grid_size).repeat(grid_size, 1).t().type(FloatTensor)

        self.scaled_anchors = FloatTensor(
            [(width / self.stride, height / self.stride) for width, height in self.anchors])
        self.anchor_widths = self.scaled_anchors[:, 0:1].view((1, self.num_anchors, 1, 1))
        self.anchor_heights = self.scaled_anchors[:, 1:2].view((1, self.num_anchors, 1, 1))

    def forward(self, input_, targets=None, img_dim=416):
        self.img_dim = img_dim
        batch_size = input_.size(0)
        grid_size = input_.size(2)
        FloatTensor = torch.cuda.FloatTensor if input_.is_cuda else torch.FloatTensor

        prediction = (input_.view(batch_size, self.num_anchors, 5 + self.classes, grid_size, grid_size)
                      .permute(0, 1, 3, 4, 2).contiguous())

        x = torch.sigmoid(prediction[:, :, :, :, 0])
        y = torch.sigmoid(prediction[:, :, :, :, 1])
        w = torch.exp(prediction[:, :, :, :, 2])
        h = torch.exp(prediction[:, :, :, :, 3])
        obj_score = torch.sigmoid(prediction[:, :, :, :, 4])
        cls_scores = torch.sigmoid(prediction[:, :, :, :, 5:])

        if self.grid_size != grid_size:
            self.compute_grid_offsets(grid_size, CUDA=input_.is_cuda)

        prediction_boxes = FloatTensor(prediction[..., :4].shape)
        prediction_boxes[:, :, :, :, 0] = x.data + self.x_offsets
        prediction_boxes[:, :, :, :, 1] = y.data + self.y_offsets
        prediction_boxes[:, :, :, :, 2] = torch.exp(w.data) * self.anchor_widths
        prediction_boxes[:, :, :, :, 3] = torch.exp(h.data) * self.anchor_heights

        output = torch.cat((prediction_boxes.view(batch_size, -1, 4) * self.stride,
                            obj_score.view(batch_size, -1, 1),
                            cls_scores.view(batch_size, -1, self.classes)), -1)

        if targets is None:
            return output, 0
        else:
            iou_scores, class_mask, obj_mask, noobj_mask, tx, ty, tw, th, tcls, tobj = build_targets(
                prediction_boxes=prediction_boxes,
                cls_scores=cls_scores,
                targets=targets,
                anchors=self.scaled_anchors,
                ignore_thresh=self.ignore_thresh
            )
            x_mask = x * obj_mask
            x_loss = self.mse_loss(x_mask, tx * obj_mask)
            y_loss = self.mse_loss(y * obj_mask, ty * obj_mask)
            w_loss = self.mse_loss(w * obj_mask, tw * obj_mask)
            h_loss = self.mse_loss(h * obj_mask, th * obj_mask)
            obj_score_loss = self.bce_loss(obj_score * obj_mask, tobj * obj_mask)
            noobj_score_loss = self.bce_loss(obj_score * noobj_mask, tobj * noobj_mask)
            conf_loss = self.obj_scale * obj_score_loss + self.no_obj_scale * noobj_score_loss
            cls_loss = self.bce_loss(cls_scores * obj_mask.unsqueeze(4), tcls * obj_mask.unsqueeze(4))
            total_loss = x_loss + y_loss + w_loss + h_loss + conf_loss + cls_loss
            total_loss.requires_grad = True

            # cls_acc = 100 * class_mask[obj_mask].mean()
            # obj_acc = obj_score[obj_mask].mean()
            # noobj_acc = obj_score[noobj_mask].mean()
            # conf50 = (obj_score > 0.5).float()
            # iou50 = (iou_scores > 0.5).float()
            # iou75 = (iou_scores > 0.75).float()
            # detected_mask = conf50 * class_mask * tobj
            # precision = torch.sum(iou50 * detected_mask) / (conf50.sum() + 1e-16)
            # recall50 = torch.sum(iou50 * detected_mask) / (obj_mask.sum() + 1e-16)
            # recall75 = torch.sum(iou75 * detected_mask) / (obj_mask.sum() + 1e-16)
            #
            # self.metrics = {
            #     "loss": total_loss.to_cpu().item(),
            #     "x": x.to_cpu().item(),
            #     "y": y.to_cpu().item(),
            #     "w": w.to_cpu().item(),
            #     "h": h.to_cpu().item(),
            #     "conf": conf_loss.to_cpu().item(),
            #     "cls": cls_loss.to_cpu().item(),
            #     "cls_acc": cls_acc.to_cpu().item(),
            #     "obj_acc": obj_acc.to_cpu().item(),
            #     "noobj_acc": noobj_acc.to_cpu().item(),
            #     "precision": precision.to_cpu().item(),
            #     "recall50": recall50.to_cpu().item(),
            #     "recall75": recall75.to_cpu().item(),
            #     "grid_size": grid_size.to_cpu().item()
            # }

            return output, total_loss


def build_targets(prediction_boxes, cls_scores, targets, anchors, ignore_thresh):
    ByteTensor = torch.cuda.ByteTensor if prediction_boxes.is_cuda else torch.ByteTensor
    FloatTensor = torch.cuda.FloatTensor if prediction_boxes.is_cuda else torch.FloatTensor

    batch_size = prediction_boxes.size(0)
    num_anchors = prediction_boxes.size(1)
    grid_size = prediction_boxes.size(2)
    classes = cls_scores.size(-1)

    iou_scores = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    class_mask = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    obj_mask = ByteTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    noobj_mask = ByteTensor(batch_size, num_anchors, grid_size, grid_size).fill_(1)
    tx = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    ty = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    tw = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    th = FloatTensor(batch_size, num_anchors, grid_size, grid_size).fill_(0)
    tcls = FloatTensor(batch_size, num_anchors, grid_size, grid_size, classes).fill_(0)

    target_boxes = targets[:, 2:] * grid_size
    txy = target_boxes[:, 0:2]
    twh = target_boxes[:, 2:]

    twh_ = FloatTensor(twh)
    zeros = FloatTensor(twh.size(0), twh.size(1)).fill_(0)
    tbox_wh = torch.cat((zeros, twh_), 1)
    zeros = FloatTensor(3, 2).fill_(0)
    anchs = torch.cat((zeros, anchors), 1)

    ious = torch.stack([bbox_iou(tbox_wh, anchor.repeat(twh.size(0), 1), False) for anchor in anchs])
    max_ious, max_n = ious.max(0)

    batch_num, target_labels = targets[:, :2].long().squeeze(0).t()
    x, y = txy.t()
    w, h = twh.t()
    ti, tj = txy.long().t()

    iou_scores[batch_num, max_n, tj, ti] = bbox_iou(prediction_boxes[batch_num, max_n, tj, ti], target_boxes, True)
    class_mask[batch_num, max_n, tj, ti] = (cls_scores[batch_num, max_n, tj, ti].argmax(-1) == target_labels).float()

    obj_mask[batch_num, max_n, tj, ti] = 1
    noobj_mask[batch_num, max_n, tj, ti] = 0

    for i, anchor_ious in enumerate(ious.t()):
        noobj_mask[batch_num[i], anchor_ious > ignore_thresh, tj[i], ti[i]] = 0

    tx[batch_num, max_n, tj, ti] = x - x.floor()
    ty[batch_num, max_n, tj, ti] = y - y.floor()

    tw[batch_num, max_n, tj, ti] = torch.log(w / anchors[max_n][:, 0] + 1e-16)
    th[batch_num, max_n, tj, ti] = torch.log(h / anchors[max_n][:, 1] + 1e-16)

    tcls[batch_num, max_n, tj, ti] = 1

    tobj = obj_mask.float()

    return iou_scores, class_mask, obj_mask, noobj_mask, tx, ty, tw, th, tcls, tobj
