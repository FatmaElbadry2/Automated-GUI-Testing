import numpy as np
import torch

grid = np.arange(3)
print(grid)
y, x = np.meshgrid(grid, grid)
print(y)
print(x)

x_offset = torch.FloatTensor(x).view(-1, 1)
print(x_offset)
y_offset = torch.FloatTensor(y).view(-1, 1)
print(y_offset)

x_y_offset = torch.cat((x_offset, y_offset), 1)
print(x_y_offset)
x_y_offset = x_y_offset.repeat(1, 3)
print(x_y_offset)
x_y_offset = x_y_offset.view(-1, 2)
print(x_y_offset)
x_y_offset = x_y_offset.unsqueeze(0)
print(x_y_offset)

anchors = [(1, 2), (3, 4), (5, 6)]
anchors = torch.FloatTensor(anchors)
anchors1 = anchors.repeat(3*3, 1)
anchors2 = anchors.repeat(1, 3*3)
print(anchors1)
print(anchors2)
