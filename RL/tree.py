from global_imports import *
from InrefaceAgent import Element_to_Action as eta


# action_space = np.empty(2901)
# action_space.fill(-1)
# action_count=np.zeros(2901)
# tree = []
# img_states = {}
# states = {}


def IsDifferent(img_1,img_2):
    img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
    img_3 = np.zeros((img_1.shape[0], img_1.shape[1]))
    img_3[img_1 == img_2] = 1
    # cv.imshow('image',img_3)
    # cv.waitKey(0)
    diff = img_3[img_3 == 0].shape[0]
    similar = img_3[img_3 == 1].shape[0]
    per_diff =  100 * diff / (diff + similar)
    if per_diff > 10:
        return True,per_diff
    return False,0


def img_exists(elements,img_states,image):
    diff = 0
    for state in img_states:
        if len(elements) == len(img_states[state][1]):
            for i in range(len(elements)):
                if elements[i].type == img_states[state][1][i].type and img_states[state][1][i].x_center +3 >=elements[i].x_center >= img_states[state][1][i].x_center -3 and img_states[state][1][i].y_center +3 >=elements[i].y_center >= img_states[state][1][i].y_center -3 \
                    / img_states[state][1][i].width +3 >=elements[i].width >= img_states[state][1][i].width -3 and img_states[state][1][i].height +3 >=elements[i].height >= img_states[state][1][i].height -3:
                    stored_image = cv2.imread(state)
                    is_diff, diff = IsDifferent(image, stored_image)
                    if not is_diff:
                        return True, state, diff
        '''if elements == img_states[state][1]:
            stored_image = cv2.imread(state)
            is_diff,diff = IsDifferent(image, stored_image)
            if not is_diff :
            # if image.tolist() == stored_image.tolist():
                return True,state,diff'''

    return False,None,diff


def actionSpaceMapper(action):  # it should return the ranges of Ids for each element in the action space
    action_type = eta.Actions
    if action == action_type.left_click:
        return [1, 600]
    if action == action.click_no_change:
        return [601,900]
    elif action == action_type.double_left_click:
        return [901, 1200]
    elif action == action_type.write_letters:
        return [1201, 1400]
    elif action == action_type.write_numbers:
        return [1401, 1600]
    elif action == action_type.write_short:
        return [1601, 1800]
    elif action == action_type.write_long:
        return [1801, 2000]
    elif action == action_type.write_alphanumeric:
        return [2001, 2200]
    elif action == action_type.delete:
        return [2201, 2400]
    elif action == action_type.drag_up:
        return [2401, 2425]
    elif action == action_type.drag_down:
        return [2426, 2450]
    elif action == action_type.drag_right:
        return [2451, 2475]
    elif action == action_type.drag_left:
        return [2476, 2500]
    else:
        return [0, 0]


def addElement(element, Id,action_space,element_ex_count):  # element is a vector contains element information
    e_type = eta.element_action_mapper(element.type)
    if e_type is not None:
        for i in range(len(e_type)):
            start, end = actionSpaceMapper(e_type[i])
            while start <= end and action_space[start] != -1:
                start += 1
            action_space[start] = Id  # the number of slots an single element can occupy should be added
        element_ex_count[Id]= 0
        return True
    else:
        return False


def buildTree(elements,tree,action_space,element_ex_count):
    IDs = []
    #global tree
    for element in elements:
        index=[i for i in range(len(tree)) if (tree[i].type == element.type and element.x_center +3 >=tree[i].x_center
                                               >= element.x_center-3 and element.y_center +3 >=tree[i].y_center >=
                                               element.y_center -3 and element.width +3 >=tree[i].width >= element.width -3
                                               and element.height +3 >=tree[i].height >= element.height -3)]
        if len(index) == 0:
            if addElement(element, len(tree),action_space,element_ex_count):
                tree.append(element)
                IDs.append(len(tree)-1)
                #print(len(tree)-1)
                #print(element)
        else:
            IDs.append(index[0])
            #print("element already exists")
    print(tree)
    return IDs

