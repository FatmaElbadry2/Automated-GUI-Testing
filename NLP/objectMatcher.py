# from imports import *
from dictionary import *
from preProcessing import *
from yoloInterface import *
from colors import *
from utils import *


def colorMatcher(color, elements):
    pass


# first look for the dobj and the pobj in the sentence

def objectSplitter(text):  # the input is nlp text
    i = 0
    objects = []
    prepNext = []
    while i < len(text):
        sent = []
        if text[i].dep_ == "dobj":
            [sent.append(l) for l in text[i].lefts if l.pos_ != "DET"]
            sent.append(text[i])

        elif text[i].dep_ == "prep":
            index = [obj.i for obj in text[i].rights if obj.dep_ == "pobj"]
            if len(index) == 0:
                index = [i]
            [sent.append(text[j]) for j in range(i, index[0]+1) if text[j].pos_ != "DET"]
            i = index[0]

        if i < len(text)-1 and text[i+1].dep_ == "prep" and str(text[i+1]) in ["to", "of"]:
            prepNext.append(True)
        else:
            prepNext.append(False)
            # sent.append(text[i:index[0]+1])
        if len(sent) > 0:
            objects.append(sent)
        i += 1
    return objects, prepNext


class ObjType(Enum):
    elementArray = 0
    input = 1
    screenText = 2
    built_in = 3
    abs_position = 4
    abs_position_prep = 5
    color = 6
    color_adj = 7
    ordinal_val = 8
    single_element = 9
    range = 10
    unknown = 11


def objectTypeMapper(obj, prep_next, textDict, inputDict, eAvailable, x_range, y_range):
    elms = in_range(x_range, y_range, eAvailable)  # gets all objects in a given range
    if str(obj)[0:5] == "text_":
        match, score = zip(*[matchText(e.text, textDict[str(obj)], 70) for e in elms])
        maxRatio = max(score)
        el = np.array(elms)
        return el[np.logical_and(np.array(score) == maxRatio, np.array(match))], ObjType.elementArray

    elif str(obj)[0:6] == "input_":
        return inputDict[obj], ObjType.input

    elif str(obj) in elementsMatcher:
        match, score = zip(*[matchText(e.type, str(obj), 80) for e in elms])
        maxRatio = max(score)
        el = np.array(elms)
        return el[np.logical_and(np.array(score) == maxRatio, np.array(match))], ObjType.elementArray

    elif str(obj) in objects:
        return obj, ObjType.built_in

    elif str(obj) in absPositions:
        if obj.dep_ in ["pobj", "dobj"] and prep_next:
            return obj, ObjType.abs_position_prep
        else:
            return obj, ObjType.abs_position

    elif str(obj) in colors:
        return [c for c in elms if c.color == str(obj)], ObjType.elementArray

    elif str(obj) in colorAdj:
        return obj, ObjType.color_adj

    elif obj.ent_type_ == "ORDINAL":
        return obj, ObjType.ordinal_val

    else:
        return None, ObjType.unknown


def sentenceInterpreter(sentence, x_range, y_range, elements, textdict, inputdict, obj_count, return_type,prep_next, prev_obj=None,
                        direction=None):
    filteredObj = elements
    Obj_changed = False
    t_input = None
    prep = None
    abs_pos = False
    abs_pos_prep = False
    for i in range(len(sentence)-1, -1, -1):

        if sentence[i].dep_ == "prep":
            prep = sentence[i]
            break

        obj, objType = objectTypeMapper(sentence[i], prep_next,textdict, inputdict, filteredObj, x_range, y_range)

        if objType == ObjType.abs_position:
            if obj.dep_ in ["pobj", "dobj"]:
                direction = [s for s in sentence if s.dep_ != "prep"]
                return t_input, x_range, y_range, direction, prev_obj, return_type, obj_count

            elif abs_pos_prep:
                x_min, x_max, y_min, y_max = getObjectRange(prev_obj.x_center, prev_obj.y_center, prev_obj.width,
                                                            prev_obj.height)
                temp_x_range, temp_y_range = prepMatcher(x_min, x_max, y_min, y_max, 0, w_width, 0, w_height, str(obj))
                temp_x_range, temp_y_range = Intersection(x_range, temp_x_range, y_range, temp_y_range)
                if temp_x_range is not None:
                    x_range = temp_x_range
                    y_range = temp_y_range

            else:
                _, filteredObj = ordinalSorter(1, filteredObj, str(obj))  # at the end we choose the first object
                Obj_changed = True
                abs_pos = True

        elif objType == ObjType.abs_position_prep:
            if return_type == ObjType.range:
                x_min, x_max, y_min, y_max = getObjectRange(prev_obj.x_center, prev_obj.y_center, prev_obj.width,
                                                            prev_obj.height)
                temp_x_range, temp_y_range = prepMatcher(x_min, x_max, y_min, y_max, 0, w_width, 0, w_height, str(obj))
                temp_x_range, temp_y_range = Intersection(x_range, temp_x_range, y_range, temp_y_range)
                if temp_x_range is not None:
                    x_range = temp_x_range
                    y_range = temp_y_range
            else:
                x_range, y_range = prepMatcher(x_range[0][0], x_range[0][1], y_range[0][0], y_range[0][1], 0, w_width, 0,
                                               w_height, str(prep))
            return_type = ObjType.range
            abs_pos_prep = True

        elif objType == ObjType.input:
            t_input = obj

        elif objType == ObjType.elementArray:
            filteredObj = obj
            Obj_changed = True

        elif objType == ObjType.color_adj:
            filteredObj = colorComparator(str(obj), filteredObj)
            Obj_changed = True

        elif objType == ObjType.ordinal_val:
            val = ordinal_dict[str(obj)]
            if direction is None:
                filteredObj, _ = ordinalSorter(val, filteredObj)
            else:
                for dirc in direction:
                    filteredObj, _ = ordinalSorter(val, filteredObj, str(dirc))
                direction = None
            Obj_changed = True

        elif objType == ObjType.built_in:
            pass
    if direction is not None:
        for dirc in direction:
            _, filteredObj = ordinalSorter(1, filteredObj, str(dirc))  # at the end we choose the first object
            Obj_changed = True
        direction = None

    if Obj_changed and len(filteredObj) > 0:
        obj_count += 1
        if obj_count > 1 and not abs_pos:  # if this is the second object and no previous directions in the same sent.
            prev_obj = nearestElement(filteredObj, [prev_obj.x_center, prev_obj.y_center])
        else:
            prev_obj = filteredObj[0]
        x_min, x_max, y_min, y_max = getObjectRange(prev_obj.x_center, prev_obj.y_center, prev_obj.width,
                                                    prev_obj.height)
        x_range = [[x_min, x_max]]
        y_range = [[y_min, y_max]]
    else:
        print("no objects found")

    if prep is not None:
        x_range, y_range = prepMatcher(x_range[0][0], x_range[0][1], y_range[0][0], y_range[0][1], 0, w_width, 0,
                                       w_height, str(prep))

    return t_input, x_range, y_range, direction, prev_obj, return_type, obj_count


def objectFinder(sentence, elements, textdict, inputdict):
    mini_sent, prep_next = objectSplitter(sentence)
    print(mini_sent)
    direction = None
    prev_obj = None
    t_input = None
    obj_count = 0
    return_type = ObjType.single_element
    x_range = [[0, w_width]]
    y_range = [[0, w_height]]
    i = len(prep_next)-1
    for sent in reversed(mini_sent):
        t_input, x_range, y_range, direction, prev_obj, return_type, obj_count = sentenceInterpreter(sent, x_range,
                                                                                                     y_range, elements,
                                                                                                     textdict, inputdict
                                                                                                     , obj_count,
                                                                                                     return_type,
                                                                                                     prep_next[i],
                                                                                                     prev_obj,
                                                                                                     direction)
        i -= 1
    return prev_obj, x_range, y_range, t_input


e1 = elementStruct(gui_elements[1])
e2 = elementStruct(gui_elements[0])
e3 = elementStruct(gui_elements[2])
# e4 = elementStruct(gui_elements[3])
e5 = [e1, e2, e3]

# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
text = "click on the second button"
ordinal_dict = createOrdinalDict()
text, dict1, dict2 = textReplacer(text)
sentence_nlp = nlp(text)
prev_object, x_range, y_range, t_input = objectFinder(sentence_nlp, e5, dict1, dict2)
print(prev_object)






