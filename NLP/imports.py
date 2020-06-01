# import nltk
import re
from spacy.tokens import Span
# from pysbd.util import PySBDFactory
from contractions import CONTRACTION_MAP
from nltk.tokenize import sent_tokenize
import spacy
import numpy as np
from spacy import displacy
from fuzzywuzzy import fuzz
import operator
from scipy.optimize import curve_fit
import inflect
import math as m
from enum import Enum
from win32api import GetSystemMetrics
w_width = GetSystemMetrics(0)  # depending on the OS
w_height = GetSystemMetrics(1)
print("starting...")