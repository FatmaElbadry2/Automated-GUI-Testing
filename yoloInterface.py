import rpa as r
from dataclasses import dataclass

# r.init(visual_automation=True, chrome_browser=False)
elements = [[0, 50, 70, 10, 10, "save", "red", 0x123456], [3, 120, 30, 20, 20, "submit", "blue", 0x123456],
            [9, 60, 30, 10, 10, "save", "red", 0x123456]]


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
    e.type = elementsMatcher[element[0]]
    e.x_center = element[1]
    e.y_center = element[2]
    e.width = element[3]
    e.height = element[4]
    e.text = element[5]
    e.color = element[6]
    e.hex = element[7]
    return e


def buildElements(elements):
    # get elements from YOLO
    all_elements = []
    for element in elements:
        getElementText(element)
        getElementColor(element)
        eStruct = elementStruct(element)
        all_elements.append(eStruct)
    return all_elements


