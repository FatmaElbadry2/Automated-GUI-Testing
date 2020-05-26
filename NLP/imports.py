import nltk
import re
from contractions import CONTRACTION_MAP
from nltk.tokenize import sent_tokenize
import spacy
import numpy as np
from spacy import displacy
# from agent import keyBoard as k
# from agent import mouse as m
# from agent import shortcuts as s
from fuzzywuzzy import fuzz
import operator
from scipy.optimize import curve_fit
import inflect
import math as m
from win32api import GetSystemMetrics
w_width = GetSystemMetrics(0)
w_height = GetSystemMetrics(1)
print("starting...")