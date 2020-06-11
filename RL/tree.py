from imports import *
from InrefaceAgent import Element_to_Action as eta
stateAction = {}
taken = np.zeros(2000)
tree = []


# click: button , icon button, check box,radio button,combobox,menu, 1-800
# double click : link  801-900
# slide : scroll bar, slider  : 901-1000
# type : textbox , alphabetic :1001-1200 , alphanumeric : 1201-1400, numbers:1401-1600, longcom:1601-1800,empty:1801-2000
# add scroll up and down


def elementtoAction(element):
    pass


def actionSpaceMapper(action):  # it should return the ranges of Ids for each element in the action space
    action_type = eta.actions
    if action == action_type.LeftClick:
        return [1, 800]
    elif action == action_type:
        return [201, 1401]
    else:
        return[1402, 1602]



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


def state_exist(image):
    if stateAction.get(image, -1) == -1:
        stateAction[image] = []
        return False
    return True


def buildTree(elements):
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



