import spacy
import re
from spacy.lang.en import English
from spacy.matcher import Matcher
from spacy.tokens import Span

import numpy as np
import math as m
# curve-fit() function imported from scipy
from matplotlib import pyplot as plt


from scipy.optimize import curve_fit
x = np.array([1, 1, 1, 1])
y = np.array([3, 5, 10, 13])


if all(p == x[0] for p in x):
    direction = "vertical"

elif all(p == y[0] for p in y):
    direction = "horizontal"

else:
    def line(x, a, b):
        return (a * x) + b
    param, param_cov = curve_fit(line, x, y)
    angle = m.degrees(param[0])
    if 40 <= abs(angle) <= 50:
        if angle < 0:
            direction = "vertical"
        else:
            direction = "horizontal"
    elif abs(angle) > 50:
        direction = "vertical"
    else:
        direction = "horizontal"

    print(param)
    ans = (param[0] * x) + param[1]
    plt.plot(x, y, 'o', color ='red', label ="data")
    plt.plot(x, ans, '--', color ='blue', label ="optimized data")
    plt.legend()
    plt.show()

print(direction)