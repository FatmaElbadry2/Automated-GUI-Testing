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