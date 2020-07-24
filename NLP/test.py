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
# import time
# import rpa as r
# r.init(visual_automation=True, chrome_browser=False)
# time.sleep(5)
# print(r.mouse_xy())
# import cv2
# import numpy as np
#
# def IsDifferent(img_1,img_2):
#     img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
#     img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
#     img_3 = np.zeros((img_1.shape[0], img_1.shape[1]))
#     img_3[img_1 == img_2] = 1
#     # cv.imshow('image',img_3)
#     # cv.waitKey(0)
#     diff = img_3[img_3 == 0].shape[0]
#     similar = img_3[img_3 == 1].shape[0]
#     per_diff =  100 * diff / (diff + similar)
#     if per_diff > 10:
#         return True,per_diff
#     return False,0
#
#
#
#
# img_1= cv2.imread("image_0.png")
# img_2 = cv2.imread("image_1.png")
#
# print(IsDifferent(img_1,img_2))