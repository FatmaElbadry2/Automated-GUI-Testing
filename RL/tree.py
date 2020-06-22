from global_imports import *
from InrefaceAgent import Element_to_Action as eta


# action_space = np.empty(2901)
# action_space.fill(-1)
# action_count=np.zeros(2901)
# tree = []
# img_states = {}
# states = {}


def img_exists(elements,img_states):
    for state in img_states:
        if elements == img_states[state]:
            # stored_image = cv2.imread(state)
            # if image.tolist() == stored_image.tolist():
            return True,state
    return False,None


def actionSpaceMapper(action):  # it should return the ranges of Ids for each element in the action space
    action_type = eta.Actions
    if action == action_type.left_click:
        return [1, 800]
    elif action == action_type.double_left_click:
        return [801, 1600]
    elif action == action_type.write_letters:
        return [1601, 1800]
    elif action == action_type.write_numbers:
        return [1801, 2000]
    elif action == action_type.write_short:
        return [2001, 2200]
    elif action == action_type.write_long:
        return [2201, 2400]
    elif action == action_type.write_alphanumeric:
        return [2401, 2600]
    elif action == action_type.delete:
        return [2601, 2800]
    elif action == action_type.drag_up:
        return [2801, 2825]
    elif action == action_type.drag_down:
        return [2826, 2850]
    elif action == action_type.drag_right:
        return [2851, 2875]
    elif action == action_type.drag_left:
        return [2876, 2900]
    else:
        return [0, 0]


def addElement(element, Id,action_space):  # element is a vector contains element information
    e_type = eta.element_action_mapper(element.type)
    if e_type is not None:
        for i in range(len(e_type)):
            start, end = actionSpaceMapper(e_type[i])
            while start <= end and action_space[start] != -1:
                start += 1
            action_space[start] = Id  # the number of slots an single element can occupy should be added
        return True
    else:
        return False


def buildTree(elements,tree,action_space):
    IDs = []
    #global tree
    for element in elements:
        index = np.where(np.array(tree) == element)[0]
        if len(index) == 0:
            if addElement(element, len(tree),action_space):
                tree.append(element)
                IDs.append(len(tree)-1)
                #print(len(tree)-1)
                #print(element)
        else:
            IDs.append(index[0])
            #print("element already exists")
    return IDs

