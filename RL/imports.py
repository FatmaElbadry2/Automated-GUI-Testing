import numpy as np
import random
from IPython.display import clear_output
from collections import deque
import progressbar

import tensorflow as tf
from tensorflow import keras

from win32api import GetSystemMetrics

Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)