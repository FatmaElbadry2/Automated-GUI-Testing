import rpa as r
import webcolors
import cv2

inside_text = ["button", "combobox", "menu", "submenu", "progressbar", "tab", "dialogbox", "dropdown"]
text_left = ["textbox", "checkbox"]
text_right = ["radio"]


def getTextAndColor(elements, image):

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for element in elements:
        colors=getDominantcolor(image[element.y_center-(element.height/2):element.y_center+(element.height/2),element.x_center-(element.width/2):element.x_center+(element.width/2),:])
        rgb = img[element.y_center, element.x_center, :]
        if element.type in inside_text:
            getInsideText(element)
        elif element.type in text_left:
            getLeftText(element)
        elif element.type in text_right:
            getRightText(element)
        _,color = get_colour_name(rgb)
        element.color = color
    return elements

def getDominantcolor(img):
    img=img.tolist()
    dict=
    for i in range(len(img)):
        for j in range(len(img[0])):
            if str(img[i][j]) in dict:
                dict[str(img[i][j])]+=1
            else:
                dict[str(img[i][j])]=0
    dict

    return dict


def getInsideText(element):
    xmin = round(element.x_center-(element.width/2))
    xmax = round(element.x_center+(element.width/2))
    ymin = round(element.y_center-(element.height/2))
    ymax = round(element.y_center+(element.height/2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text=text
    print(text)
    return element


def getLeftText(element):
    xmax = round(element.x_center - (element.width / 2))
    xmin = xmax-element.width
    ymin = round(element.y_center - (element.height / 2))
    ymax = round(element.y_center + (element.height / 2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text = text
    return element


def getRightText(element):
    xmin = round(element.x_center + (element.width / 2))
    xmax = xmin + element.width
    ymin = round(element.y_center - (element.height / 2))
    ymax = round(element.y_center + (element.height / 2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text = text
    return element


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS2_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name



# import numpy as np
# from itertools import groupby
# img1=cv2.imread("RetinaNet\\tex.JPG")
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#
# image=img1.tolist()
# print(len(image[0][0]))
# p=[[str(z) for z in x] for x in image]
# print(p)
# print(len(p))
# print(len(p[0]))

# print(len(img))
# print()
# y=[1,2,34,1,1,2,4,5]
# x=[len(list(group)) for key,group in groupby(y)]
# print(x)
# print(len(x))

# import collections as c
# counter=c.Counter(p)
# print(counter)
# print(counter.values())



