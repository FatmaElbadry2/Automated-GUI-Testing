from imports import *
from dictionary import *
from preProcessing import *
from yoloInterface import *
from colors import *


def matchText(eText, uText,thresh):
    print(eText, uText)
    levRatio = fuzz.partial_ratio(eText.lower(), uText.lower())
    print(levRatio)
    if levRatio >= thresh:
        return True, levRatio
    return False, levRatio


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

        if i < len(text)-1 and text[i+1].dep_ == "prep" and text[i+1] in ["to", "of"]:
            prepNext.append(True)
        else:
            prepNext.append(False)
            # sent.append(text[i:index[0]+1])
        if len(sent) > 0:
            objects.append(sent)
        i += 1
    return objects, prepNext


def retrieveObject():
    pass


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
    unknown = 9


def getObjectRange(x_center, y_center, width, height):
    x_min = x_center - (width / 2)
    x_max = x_center + (width / 2)
    y_min = y_center - (height / 2)
    y_max = y_center + (height / 2)
    return x_min, x_max, y_min, y_max


def in_range(x_range, y_range, objs):
    in_x = False
    in_y = False
    in_obj = []
    for obj in objs:
        x_min, x_max, y_min, y_max = getObjectRange(obj.x_center, obj.y_center, obj.width, obj.height)
        for x in x_range:
            if x_min >= x[0] and x_max <= x[1]:
                in_x = True
                break
        for y in y_range:
            if y_min >= y[0] and y_max <= y[1]:
                in_y = True
                break
        if in_x and in_y:
            in_obj.append(obj)
    return in_obj


def objectTypeMapper(objects, textDict, inputDict, eAvailable, x_range, y_range):
    elms = in_range(x_range, y_range, eAvailable)  # gets all objects in a given range
    for obj, prepNext in objects:
        if str(obj[0:5]) == "text_":
            match, score = zip(*[matchText(e.text, textDict[obj], 70) for e in elms])
            maxRatio = max(score)
            el = np.array(elms)
            return el[np.logical_and(np.array(score) == maxRatio, np.array(match))], ObjType.elementArray

        elif str(obj[0:6]) == "input_":
            return inputDict[obj], ObjType.input

        elif str(obj) in elementsMatcher:
            match, score = zip(*[matchText(e.type, textDict[obj], 80) for e in elms])
            maxRatio = max(score)
            el = np.array(elms)
            return el[np.logical_and(np.array(score) == maxRatio, np.array(match))], ObjType.elementArray

        elif str(obj) in objects:
            return obj, ObjType.built_in

        elif str(obj) in absPositions:
            if obj.dep_ in ["pobj", "dobj"] and prepNext:
                return obj, ObjType.abs_position_prep
            else:
                return obj, ObjType.abs_position

        elif str(obj) in colors:
            return [c for c in elms if c.color == str(obj)], ObjType.elementArray

        elif str(obj) in colorAdj:
            return obj, ObjType.color_adj

        elif obj.ent_type == "ORDINAL":
            return obj, ObjType.ordinal_val

        else:
            return None, ObjType.unknown


def colorComparator(shade,elems):
    colors = np.array([e.hex for e in elems])
    lightest = max(colors)
    darkest = min(colors)
    if shade == "light":
        return colors[colors == lightest]
    else:
        return colors[colors == darkest]


ordinal_dict = {}


def sentenceInterpreter(sentence, x_range, y_range, objs, textdict, inputdict, prevobj=None, direction=None):
    filteredObj = objs
    t_input = None
    for i in range(len(sentence), -1, -1):
        obj, objType = objectTypeMapper(sentence[i], textdict, inputdict, filteredObj, x_range, y_range)

        if objType == ObjType.abs_position:  # gives the direction to the previous sentence
            if obj.dep_ in ["pobj", "dobj"]:
                direction = sentence
                break
            else:
                _, filteredObj = ordinalSorter(1, str(obj), filteredObj)

        elif objType == ObjType.abs_position_prep:  # what if mafeesh previous object !!!!!!!
            x_min, x_max, y_min, y_max = getObjectRange(prevobj.x_center, prevobj.y_center, prevobj.width,
                                                        prevobj.height)
            x_range, y_range = prepMatcher(x_min, x_max, y_min, y_max, 0, GetSystemMetrics(0), 0, GetSystemMetrics(1),
                                           str(obj))

        elif objType == ObjType.input:
            t_input = obj

        elif objType == ObjType.elementArray:
            filteredObj = obj

        elif objType == ObjType.color_adj:
            filteredObj = colorComparator(str(obj), filteredObj)

        elif objType == ObjType.ordinal_val:
            val = ordinal_dict[str(obj)]
            if len(direction) == 0:
                prevobj, filteredObj = ordinalSorter(1, None, filteredObj)
            else:
                for dirc in direction:
                    prevobj, filteredObj = ordinalSorter(val, dirc, filteredObj)
        else:
            pass
    if len(filteredObj) == 1:
        prevobj = filteredObj[0]
    return t_input, x_range, y_range, direction, prevobj






inside = ["in", "on", "inside", "into", "of", "towards", "to", "for", "from", "middle"]
below = ["below", "under", "beneath", "bottom", "down"]
above = ["over", "above", "top", "up"]
beside = ["next", "beside"]


def directionOfIncrease(x, y):
    if all(p == x[0] for p in x):
        direction = "vertical"

    elif all(p == y[0] for p in y):
        direction = "horizontal"

    else:
        def line(x, a, b):
            return (a * x) + b
        param, param_cov = curve_fit(line, x, y)
        angle = m.degrees(param[0])
        if 40 <= abs(angle) <= 50:
            if angle < 0:
                direction = "vertical"
            else:
                direction = "horizontal"
        elif abs(angle) > 50:
            direction = "vertical"
        else:
            direction = "horizontal"
    return direction


def ordinalSorter(value, direction, objs):
    sorted_obj = objs
    if direction in below:
        sorted_obj.sort(key=operator.attrgetter('y_center'), reverse=True)
    elif direction in above:
        sorted_obj.sort(key=operator.attrgetter('y_center'))
    elif direction == "left":
        sorted_obj.sort(key=operator.attrgetter('x_center'))
    elif direction == "right":
        sorted_obj.sort(key=operator.attrgetter('x_center'), reverse=True)
    else:
        x_points = [p.x_center for p in objs]
        y_points = [p.y_center for p in objs]
        direction = directionOfIncrease(x_points, y_points)
        if direction == "vertical":
            sorted_obj.sort(key=operator.attrgetter('y_center'))
        else:
            sorted_obj.sort(key=operator.attrgetter('x_center'))
    return sorted_obj[value - 1], sorted_obj


def prepMatcher(x_min, x_max, y_min, y_max, wx_min, wx_max, wy_min, wy_max, prep):
    if prep in inside:
        return [[x_min, x_max]], [[y_min, y_max]]
    elif prep in below:
        return [[wx_min, wx_max]], [[y_max, wy_max]]
    elif prep in above:
        return [[wx_min, wx_max]], [[wy_min, y_min]]
    elif prep in beside:
        return [[wx_min, x_min], [x_max, wx_max]], [wy_min, wy_max]
    elif prep == "out":
        return [[wx_min, x_min], [x_max, wx_max]], [[wy_min, y_min], [y_max, wy_max]]
    elif prep == "left":
        return [[wx_min, x_min]],  [wy_min, wy_max]
    elif prep == "right":
        return [[x_max, wx_max]], [wy_min, wy_max]
    return [[wx_min, wx_max]], [[wy_min, wy_max]]


# e1 = elementStruct(elements[1])
# e2 = elementStruct(elements[0])
# e3 = elementStruct(elements[2])
# e4 = [e1, e2, e3]

# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
text = "click on the button on the left"
text, dict1, dict2 = textReplacer(text)
sentence_nlp = nlp(text)
objects, _ = objectSplitter(sentence_nlp)
print(objects)






