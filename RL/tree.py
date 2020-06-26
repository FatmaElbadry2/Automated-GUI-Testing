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
    print("difference: ", diff)
    print("similar: ", similar)
    print("ratio_similar: ", 100 * similar / (diff + similar))
    print("ratio_diff: ", 100 * diff / (diff + similar))
    print("diff to similar: ", 100 * diff / (similar))
    if per_diff > 10:
        return True,per_diff
    return False,0



def img_exists(elements,img_states,image):
    diff = 0
    for state in img_states:
        if elements == img_states[state][1]:
            stored_image = cv2.imread(state)
            is_diff,diff = IsDifferent(image, stored_image)
            if not is_diff :
            # if image.tolist() == stored_image.tolist():
                return True,state,diff

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

