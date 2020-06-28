# from imports import *
from dictionary import *
from preProcessing import *
from colors import *
from utils import *
from RNInterface import *


def colorMatcher(color, elements):
    pass


def objectSplitter(text,start):  # it takes one sentence and split it into mini sentences according to the objects
    i = 0
    sub_sentences = []
    prep_next = []
    while i < len(text):
        new_sent = False
        sent = []
        if text[i].dep_ == "dobj" or text[i].dep_ == "nsubj":
            [sent.append(l) for l in text[i].lefts if l.pos_ != "DET"]
            sent.append(text[i])
            new_sent = True
        elif text[i].dep_ == "prep":
            index = [obj.i for obj in text[i].rights]
            if len(index) == 0:
                index = [i-start]
            [sent.append(text[j]) for j in range(i, index[0]+1-start) if text[j].pos_ != "DET"]
            i = index[0]-start
            new_sent = True
        if new_sent:
            if i < len(text)-1 and text[i+1].dep_ == "prep" and str(text[i+1]) in ["to", "of"]:
                prep_next.append(True)
            else:
                prep_next.append(False)
            # sent.append(text[i:index[0]+1])
        if len(sent) > 0:
            sub_sentences.append(sent)
        i += 1
    return sub_sentences, prep_next


class ObjType(Enum):  # it represents all type of possible objects
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


class ReturnTypes(Enum):  # return type of the sentence
    single_element = 0
    range = 1


def objectTypeMapper(obj, prep_next, text_dict, input_dict, elements, x_range, y_range):
    in_range_elements = in_range(x_range, y_range, elements)  # gets all objects in a given range
    if str(obj)[0:5] == "text_":
        try:
            match, score = zip(*[matchText(e.text, text_dict[str(obj)], 70) for e in in_range_elements])
            maxRatio = max(score)
            el = np.array(in_range_elements)
            el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
            if len(el) > 0:
                error = Errors.no_error
            else:
                error = Errors.object_not_found
            return el, ObjType.elementArray, error

        except ValueError:
            return None, ObjType.elementArray, Errors.empty_range

    elif str(obj)[0:6] == "input_":
        try:
            return input_dict[str(obj)], ObjType.input, Errors.no_error
        except KeyError:
            return None, ObjType.input, Errors.invalid_key

    elif str(obj) in elementsMatcher:
        try:
            match, score = zip(*[matchText(e.type, str(obj), 80) for e in in_range_elements])
            maxRatio = max(score)
            el = np.array(in_range_elements)
            el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
            if len(el) > 0:
                error = Errors.no_error
            else:
                error = Errors.object_not_found
            return el, ObjType.elementArray, error
        except ValueError:
            return None, ObjType.elementArray, Errors.empty_range

    elif str(obj) in objects:
        return obj, ObjType.built_in, Errors.no_error

    elif str(obj) in absPositions:
        if obj.dep_ in ["pobj", "dobj"] and prep_next:
            return obj, ObjType.abs_position_prep, Errors.no_error
        else:
            return obj, ObjType.abs_position, Errors.no_error

    elif str(obj) in colors:
        try:
            el = [c for c in in_range_elements if c.color == str(obj)]
            if len(el) > 0:
                error = Errors.no_error
            else:
                error = Errors.object_not_found
            return el, ObjType.elementArray, error
        except ValueError:
            return None, ObjType.elementArray, Errors.object_not_found

    elif str(obj) in colorAdj:
        return obj, ObjType.color_adj, Errors.no_error

    elif obj.ent_type_ == "ORDINAL":
        return obj, ObjType.ordinal_val, Errors.no_error

    else:
        return None, ObjType.unknown, Errors.no_error


def sentenceInterpreter(sentence, x_range, y_range, elements, text_dict, input_dict, obj_count, return_type, prep_next,ordinal_dict,
                        prev_obj=None, direction=None):
    filteredObj = elements
    Obj_changed = False
    t_input = None
    prep = None
    abs_pos = False
    abs_pos_prep = False
    for i in range(len(sentence)-1, -1, -1):

        if i == 0 and sentence[i].dep_ == "prep":
            prep = sentence[i]
            break

        obj, objType, error = objectTypeMapper(sentence[i], prep_next, text_dict, input_dict, filteredObj, x_range, y_range)

        if error != Errors.no_error:
            raise ValueError(error)

        if objType == ObjType.abs_position:
            if obj.dep_ in ["pobj", "dobj"]:
                direction = [s for s in sentence if s.dep_ != "prep"]
                return t_input, x_range, y_range, direction, prev_obj, return_type, obj_count

            elif abs_pos_prep:
                if prev_obj is None:
                    raise ValueError(Errors.object_not_found)
                x_min, x_max, y_min, y_max = getObjectRange(prev_obj.x_center, prev_obj.y_center, prev_obj.width,
                                                            prev_obj.height)
                temp_x_range, temp_y_range = prepMatcher(x_min, x_max, y_min, y_max, 0, w_width, 0, w_height, str(obj))
                temp_x_range, temp_y_range = Intersection(x_range, temp_x_range, y_range, temp_y_range)
                if temp_x_range is not None:
                    x_range = temp_x_range
                    y_range = temp_y_range
                else:
                    raise ValueError(Errors.empty_range)

            else:
                _, filteredObj = ordinalSorter(1, filteredObj, str(obj))  # at the end we choose the first object
                Obj_changed = True
                abs_pos = True

        elif objType == ObjType.abs_position_prep:
            if prev_obj is None:
                raise ValueError(Errors.object_not_found)
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
                                               w_height, str(obj))
            return_type = ObjType.range
            abs_pos_prep = True

        elif objType == ObjType.input:
            t_input = str(obj)

        elif objType == ObjType.elementArray:
            filteredObj = obj
            Obj_changed = True

        elif objType == ObjType.color_adj:
            filteredObj = colorComparator(str(obj), filteredObj)
            Obj_changed = True

        elif objType == ObjType.ordinal_val:
            val = min(ordinal_dict[str(obj)], len(filteredObj))
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
        for dirc in reversed(direction):
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


def objectFinder(sentence, elements, textdict, inputdict,ordinal_dict,start):
    print(sentence)
    mini_sent, prep_next = objectSplitter(sentence,start)
    print(mini_sent)
    print(prep_next)
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
                                                                                                     prep_next[i],ordinal_dict,
                                                                                                     prev_obj,
                                                                                                     direction)

        i -= 1

    return prev_obj, x_range, y_range, t_input, direction, return_type

'''
e1 = elementStruct(gui_elements[0])
e2 = elementStruct(gui_elements[1])
e3 = elementStruct(gui_elements[2])
e4 = elementStruct(gui_elements[3])
e5 = elementStruct(gui_elements[4])
e6 = elementStruct(gui_elements[5])
e7 = elementStruct(gui_elements[6])
e8 = elementStruct(gui_elements[7])
e9 = [e1, e2, e3, e4, e5, e6, e7, e8]

# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
# text = "click on the button on the left of the {cancel} button"
# text = "click on the button on the top right of the {ok} button inside the dialogbox"
text = "scroll up until the left button is visible"

ordinal_dict = createOrdinalDict()
# text, dict1, dict2 = textReplacer(text)
sentence_nlp = nlp(text)
print(objectSplitter(sentence_nlp))
# try:
#     prev_object, x_range, y_range, t_input, direction, return_type = objectFinder(sentence_nlp, e9, dict1, dict2)
#     print(prev_object)
# except ValueError as e:
#     print(str(e))
'''
# text="click on the first icon_button from the east"
# sentence_nlp=nlp(text)
# print(sentence_nlp[5].dep_)
# x=sentence_nlp[1:]
# print(x[4].dep_)
# print(objectSplitter(x,1))
