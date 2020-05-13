from imports import *
from dictionary import *
from preProcessing import textReplacer
from yoloInterface import *


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
    prepNext = False
    while i < len(text):
        sent = []
        if text[i].dep_ == "dobj":
            [sent.append(l) for l in text[i].lefts if l.pos_ != "DET"]
            sent.append(text[i])
            if i < len(text)-1 and text[i+1].dep_ == "prep":
                prepNext = True

        elif text[i].dep_ == "prep":
            index = [obj.i for obj in text[i].rights if obj.dep_ == "pobj"]
            if len(index) == 0:
                index = [i]
            [sent.append(text[j]) for j in range(i, index[0]+1) if text[j].pos_ != "DET"]
            if index[0] < len(text)-1 and text[index[0]+1].dep_ == "prep":
                prepNext = True
            # sent.append(text[i:index[0]+1])
            i = index[0]

        if len(sent) > 0:
            objects.append(sent)
        i += 1
    return objects,prepNext


def retrieveObject():
    pass


class ObjType(Enum):
    elementArray = 0
    input = 1
    screenText = 2
    built_in = 3
    abs_position = 4
    abs_position_prep = 5
    unknown = 6


def objectFinder(objects, textDict, inputDict,elms):
    for obj,prepNext in objects:
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
                return obj,ObjType.abs_position

        else:
            return None, ObjType.unknown


def resolvePronouns():
    pass


def positionMatcher(sent):
    pass



# look at the output objects
# process eah one
# if the right of the pobj has a preposition then we are still on the same object






def adjProcessor():
    pass



# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
# text = "click the top left button on the left of the {file} menu"
# text, dict1, dict2 = textReplacer(text)
# sentence_nlp = nlp(text)
# objects = objectSplitter(sentence_nlp)






