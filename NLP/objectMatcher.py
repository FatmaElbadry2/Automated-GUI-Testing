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

        if i < len(text)-1 and text[i+1].dep_ == "prep":
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
        if in_x and in_y:
            in_obj.append(obj)
    return in_obj


def objectTypeMapper(objects, textDict, inputDict, eAvailable, x_range, y_range):
    elms = in_range(x_range, y_range, eAvailable)
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
            if prepNext:
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


def sentenceInterpreter(sent, elems, textDict, inputDict, prevType, dir, ordinal, x_range, y_range):
    filteredElements = elems
    inputT = ""
    for i in range(len(sent)-1, -1, -1):
        obj, eType = objectTypeMapper(sent[i], textDict, inputDict, filteredElements)
        if eType == ObjType.elementArray:
            filteredElements = obj
        elif eType == ObjType.color_adj:
            filteredElements = colorComparator(obj, filteredElements)
        elif eType == ObjType.input:
            inputT = obj
        elif eType == ObjType.built_in:
            pass
        elif eType == ObjType.ordinal_val:
            pass
        elif eType == ObjType.abs_position:
            pass
        elif eType == ObjType.abs_position_prep:
            pass
        else:
            pass

    return filteredElements, inputT


inside = ["in", "on", "inside", "into", "of", "towards", "to", "for", "from", "middle"]
below = ["below", "under", "beneath", "bottom", "down"]
above = ["over", "above", "top", "up"]
beside = ["next", "beside"]


def DirectionOfIncrease(x,y):
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
        return sorted_obj[value-1]
    elif direction in above:
        sorted_obj.sort(key=operator.attrgetter('y_center'))
        return sorted_obj[value - 1]
    elif direction == "left":
        sorted_obj.sort(key=operator.attrgetter('x_center'))
        return sorted_obj[value - 1]
    elif direction == "right":
        sorted_obj.sort(key=operator.attrgetter('x_center'), reverse=True)
        return sorted_obj[value - 1]
    else:
        pass


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



# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
text = "click on the button on the left"
text, dict1, dict2 = textReplacer(text)
sentence_nlp = nlp(text)
objects, _ = objectSplitter(sentence_nlp)
print(objects)






