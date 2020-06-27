# import spacy
# import re
# from spacy.lang.en import English
# from spacy.matcher import Matcher
# from spacy.tokens import Span
# # from yoloInterface import *
# from preProcessing import *
# import numpy as np
# import math as m
# # from objectMatcher import *
# from dataclasses import dataclass


# text_dict = {
#     "text_0": "help",
#     "text_1": "germany",
#     "text_2": "Navigate"
# }
#
# input_dict = {
#     "input_0": "Fatma Elbadry",
#     "input_1": "password",
#     "input_2": "egypt"
# }
# text = "write 'fatooma' in the {file} menu"
# # ordinal_dict = createOrdinalDict()
# text, text_dict, input_dict = textReplacer(text)
# sentence_nlp = nlp(text)
# print(sentence_nlp)
# print(objectSplitter(sentence_nlp))
# obj, Type, error = objectTypeMapper(sentence_nlp[0], False, text_dict, input_dict, e5, [[0, w_width]], [[90, w_height]])
# print(obj)
# print(Type)
# print(error)

import numpy as np
x=np.array([0,0,0])
print((x==2).any())