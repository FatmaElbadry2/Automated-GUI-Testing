import rpa as r

inside_text = ["button", "combobox", "menu", "submenu", "progressbar", "tab", "dialogbox", "dropdown"]
text_left = ["textbox","checkbox"]
text_right = ["radio"]


def getText(elements):
    for element in elements:
        if element.type in inside_text:
            getInsideText(element)
        elif element.type in text_left:
            getLeftText(element)
        elif element.type in text_right:
            getRightText(element)
    return elements


def getInsideText(element):
    xmin = round(element.x_center-(element.width/2))
    xmax = round(element.x_center+(element.width/2))
    ymin = round(element.y_center-(element.height/2))
    ymax = round(element.y_center-(element.height/2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text=text
    return element


def getLeftText(element):
    xmax = round(element.x_center - (element.width / 2))
    xmin = xmax-element.width
    ymin = round(element.y_center - (element.height / 2))
    ymax = round(element.y_center - (element.height / 2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text = text
    return element


def getRightText(element):
    xmin = round(element.x_center + (element.width / 2))
    xmax = xmin + element.width
    ymin = round(element.y_center - (element.height / 2))
    ymax = round(element.y_center - (element.height / 2))
    text = r.read(xmin, ymin, xmax, ymax)
    element.text = text
    return element

