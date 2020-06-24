import re
import numpy as np
import cv2
import random
# from IPython.display import clear_output
# from collections import deque
# import progressbar
# import tensorflow as tf
# from tensorflow import keras
from enum import Enum
import time

import numpy as np
import random
from collections import namedtuple, deque
import threading, _thread, queue

# import torch
# import torch.nn.functional as F
# import torch.optim as optim
# import torch.nn as nn
import os
MY_DIRNAME = os.path.dirname(os.path.abspath(__file__))

from win32api import GetSystemMetrics
Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)
print("width: ",Width)
print("Height: ", Height)
#print("window ratio: ", Height/Width)
