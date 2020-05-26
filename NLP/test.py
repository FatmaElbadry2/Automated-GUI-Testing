import spacy
import re
from spacy.lang.en import English
from spacy.matcher import Matcher
from spacy.tokens import Span
# from yoloInterface import *
# from preProcessing import *
import numpy as np


# import math as m
# # curve-fit() function imported from scipy
# from matplotlib import pyplot as plt
#
#
# from scipy.optimize import curve_fit
# x = np.array([1, 1, 1, 1])
# y = np.array([3, 5, 10, 13])
#
#
# if all(p == x[0] for p in x):
#     direction = "vertical"
#
# elif all(p == y[0] for p in y):
#     direction = "horizontal"
#
# else:
#     def line(x, a, b):
#         return (a * x) + b
#     param, param_cov = curve_fit(line, x, y)
#     angle = m.degrees(param[0])
#     if 40 <= abs(angle) <= 50:
#         if angle < 0:
#             direction = "vertical"
#         else:
#             direction = "horizontal"
#     elif abs(angle) > 50:
#         direction = "vertical"
#     else:
#         direction = "horizontal"
#
#     print(param)
#     ans = (param[0] * x) + param[1]
#     plt.plot(x, y, 'o', color ='red', label ="data")
#     plt.plot(x, ans, '--', color ='blue', label ="optimized data")
#     plt.legend()
#     plt.show()
#
# print(direction)


# e1 = elementStruct(gui_elements[1])
# e2 = elementStruct(gui_elements[0])
# e3 = elementStruct(gui_elements[2])
# e4 = [e1, e2, e3]
#
# e4.sort(key=operator.attrgetter('x_center'))
# e4.sort(key=operator.attrgetter('y_center'))
# print(e4)