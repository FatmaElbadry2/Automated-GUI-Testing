import numpy as np
import torch

# grid = np.arange(3)
# print(grid)
# y, x = np.meshgrid(grid, grid)
# print(y)
# print(x)
#
# x_offset = torch.FloatTensor(x).view(-1, 1)
# print(x_offset)
# y_offset = torch.FloatTensor(y).view(-1, 1)
# print(y_offset)
#
# x_y_offset = torch.cat((x_offset, y_offset), 1)
# print(x_y_offset)
# x_y_offset = x_y_offset.repeat(1, 3)
# print(x_y_offset)
# x_y_offset = x_y_offset.view(-1, 2)
# print(x_y_offset)
# x_y_offset = x_y_offset.unsqueeze(0)
# print(x_y_offset)
#
# anchors = [(1, 2), (3, 4), (5, 6)]
# anchors = torch.FloatTensor(anchors)
# anchors1 = anchors.repeat(3*3, 1)
# anchors2 = anchors.repeat(1, 3*3)
# print(anchors1)
# print(anchors2)

# test = torch.tensor([[[1, 2, 3],
#                     [4, 5, 6]],
#                     [[7, 8, 9],
#                      [10, 11, 12]]])
# print(test)
# thresh = 6
# mask = (test[:, :, 2] > thresh).float().unsqueeze(2)
# test = test*mask
# print(test)

test = torch.tensor([[1, 4, 3],
                    [4, 7, 6],
                    [7, 10, 9]])
max_num, max_index = torch.max(test[:, 1:3], 1)
print(max_num)
print(max_index)
max_num = max_num.float().unsqueeze(1)
max_index = max_index.float().unsqueeze(1)
max_index = torch.FloatTensor(max_index)
torch.add(max_index, 1)
print(max_num)
print(max_index)
