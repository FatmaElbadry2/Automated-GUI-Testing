import rpa as r
import cv2
from dataclasses import dataclass
from global_imports import MY_DIRNAME
from InrefaceAgent import shortcuts as sh
#from YOLOv3_PyTorch.test import detect as d

#r.init(visual_automation=True, chrome_browser=False)
# gui_elements = [[0, 80, 70, 10, 10, "save", "red", 0x123456], [1, 120, 40, 20, 20, "submit", "blue", 0x123456],
#             [0, 60, 30, 10, 10, "save", "red", 0x123456]]

gui_elements = [[20, 300, 170, 100, 70, "are you sure you wanna do this", "white", 0x123456],
                [0, 330, 190, 30, 20, "cancel", "red", 0x123456], [22, 340, 145, 10, 10, "x", "red", 0x123456],
                [0, 315, 160, 10, 10, "flower", "pink", 0x123456], [0, 260, 145, 10, 10, "heart", "pink", 0x123456],
                [0, 275, 160, 10, 10, "star", "yellow", 0x123456], [0, 360, 160, 10, 10, "ok", "green", 0x123456],
                [0, 270, 190, 30, 20, "ok", "green", 0x123456]]

elementsMatcher = [
    "button",
    "label",
    "radio_button",
    "textbox",
    "checkbox",
    "combobox",
    "spinbox",
    "menu",
    "submenu",
    "scrollbar",
    "progressbar",
    "dial",
    "tab",
    "tab_bar",
    "table",
    "slider",
    "calendar",
    "link",
    "switch",
    "icon_button",
    "dialogbox",
    "textarea",
    "close",
    "save",
    "load",
    "redo",
    "undo",
    "export",
    "new",
    "info",
    "search",
    "settings",
    "max_min",
    "dropdown",
    "text_combobox",
    "button_combobox"
]


@dataclass
class Element:
    ID: int = None
    type: str = ""
    x_center: int = -1
    y_center: int = -1
    width: int = -1
    height: int = -1
    text: str = ""
    color: str = ""
    hex: hex = 0x00


def getElementText(element):
    xmin = element[1]-(element[3]/2)
    xmax = element[1]+(element[3]/2)
    ymin = element[2]-(element[4]/2)
    ymax = element[2]+(element[4]/2)
    text = r.read(xmin, ymin, xmax, ymax)
    element.append(text)


def getElementColor(elements):
    pass


def elementStruct(element):
    e = Element()
    e.type = elementsMatcher[int(element[0])]
    e.x_center = element[1]
    e.y_center = element[2]
    e.width = element[3]
    e.height = element[4]
    # e.text = element[5]
    # e.color = element[6]
    # e.hex = element[7]
    return e


def buildElements(image,i):
    elements = d.detect(image, "image_" + str(i) + ".png")
    print(i," :",len(elements))
    all_elements = []
    for element in elements:
        # getElementText(element)
        # getElementColor(element)
        eStruct = elementStruct(element)
        all_elements.append(eStruct)
    return all_elements


def save_image(i):
    image = sh.ScreenShot()
    print("screen-shot taken")
    image.save(MY_DIRNAME + "\\RL\\images\\image_" + str(i) + ".png")
    image = cv2.imread(MY_DIRNAME + "\\RL\\images\\image_" + str(i) + ".png", cv2.IMREAD_COLOR)
    return image, MY_DIRNAME + "\\RL\\images\\image_" + str(i) + ".png"


