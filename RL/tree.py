
import re
import numpy as np
import cv2

stateAction = {}
taken = np.zeros(2000)
tree = []

#click: button , icon button, check box,radio button,combobox,menu, 1-800
# double click : link  801-900
# slide : scroll bar, slider  : 901-1000
# type : textbox , alphabetic :1001-1200 , alphanumeric : 1201-1400, numbers:1401-1600, longcom:1601-1800,empty:1801-2000



def elementtoAction(element):
    pass


def actionSpaceMapper(actionType):  # it should return the ranges of Ids for each element in the action space
    if actionType == "0000":
        return [1, 200]
    elif actionType == 2:
        return [201, 1401]
    else:
        return[1402, 1602]


def readState(image, file):
    elements = []
    image = cv2.imread(image)
    f = open(file, "r")
    if f.mode == 'r':
        lines = f.readlines()
        for line in lines:
            element = re.split(" |\n",line)
            elements.append(element[0:len(element)-1])
    else:
        print("this file is not open for reading")
    return [image, elements]


#print(readState(image,"assets\AutoQ3D_1.txt"))


# def checkState(picture):
#     beg = False
#     if len(states) > 0 and picture in states:  # the state already exists
#         return True, beg
#     if len(states) == 0:
#         beg = True
#     states.append(picture)
#     return False, beg

# the state is stored in the sheet as pixels, all elements, text on element, position parent.
# the parent is the action that lead to the appearance of a certain element.
# an action is composed of an action ID, element type, type of action
# first state has a parent of ID = 0
# givens : action space, picture with all element information


actionSpace = []


def numActionsMapper(element):  # it should return the number of action each element can take
    return 0


def addElement(element):  # element is a vector contains element information
    start, end = actionSpaceMapper(element[0])
    numactions = numActionsMapper(element[0])
    while start <= end and taken[start] == 1:
        start += 1
    Id = actionSpace[start][0]
    taken[start:start+numactions] = 1  # the number of slots an single element can occupy should be added
    return Id


def buildTree(image, tree, file):
    picture, elements = readState(image, file)
    if stateAction.get(picture,-1) == -1:
        stateAction[picture] = []
        for element in elements:
            index = np.where(tree[:, 0:-1] == element)[0]
            if len(index) == 0:  # assuming that the last place contains the element's ID
                ID = addElement(element)
                element.append(ID)
                tree.append(element)
                stateAction[picture].append(element[-1])  # it appends the element ID
            else:
                stateAction[picture].append(tree[index[0]])

    return tree, stateAction[picture]



# def buildTree(picture,tree,elements,parentId):
#     if tree.get(parentId,-1) == -1:
#         tree[parentId] = []
#     exist, beg = checkState(picture)
#     availableElements = []
#     if exist:
#         return
#     if beg:  # this is the first state
#         for element in elements:
#             Id = addElement(element)
#             element.append(0)
#             element.append(Id)
#             availableElements.append(Id)
#             tree.append(element)
#
#     else:  # compare available elements
#         for element in elements:
#             element.append(parentId)
#             if element not in tree[:, 0:-1]:
#                 Id = addElement(element)
#                 element[-1] = Id
#                 tree.append(element)
#             availableElements.append(element[-1])
#     return availableElements, tree



