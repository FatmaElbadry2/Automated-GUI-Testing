from NLP.imports import *
from spacy.tokens import Span
from dictionary import *
from preProcessing import *
from InrefaceAgent import keyboard as k, mouse, shortcuts as sh
import rpa as r
from utils import matchText
from yoloInterface import Element
from objectMatcher import objectTypeMapper, Errors, e9
from dataclasses import dataclass


def getScrollType(elements):
    _, _, error = objectTypeMapper("scrollbar", False, None, None, elements, [[0, w_width]], [[0, w_height]])
    if error != Errors.no_error:
        action_type = Actions.scroll
    else:
        action_type = Actions.drag
    return action_type


def cardinalRemover(sentence):
    val = None
    i = 0
    while i < len(sentence):
        if sentence[i].tag_ == "CD":
            quantity = [sentence[i]]
            parent = list(sentence[i].ancestors)
            if len(parent) > 0:
                grandparent = list(parent[0].ancestors)
                if parent[0].dep_ == "pobj" and len(grandparent) > 0:
                    [quantity.append(l) for l in text[grandparent[0].i:parent[0].i + 1]]
                else:
                    [quantity.append(l) for l in text[sentence[i].i:parent[0].i + 1]]
            val = quantity[0]
            quantity_st = quantity[0].i
            quantity_nd = quantity[-1].i
            if len(quantity) > 1:
                quantity_st = quantity[1].i
            exp = str(sentence[quantity_st:quantity_nd+1])
            sentence = str(sentence)
            sentence = sentence.replace(exp, '')
            sentence = nlp(sentence)
            i = quantity_st-1
        i += 1
    return sentence, val


def getActionType(sentence, elements):
    actions = []
    action_type = Actions.undefined
    rights = []
    quantity = None
    for word in sentence:
        if word.dep_ == "ROOT":
            action_type = verbs.get(word.lemma_, -1)
            if action_type == -1:
                return Actions.undefined, None, None
            if word.lemma_ == "scroll":
                action_type = getScrollType(elements)
            actions = list(word.lefts)
            actions.append(word)
            rights = list(word.rights)
        elif word.tag_ == "CD":
            # quantity = [word]
            parent = list(word.ancestors)
            if len(parent) > 0:
                x = [anc for anc in parent if anc.dep_ == "prep" and str(anc) in ["by", "with", "for"]]
                if len(x) > 0:
                    quantity = [word]
    return action_type, actions, rights, quantity


def otherActions(action, elements, center):
    match, score = zip(*[matchText(e.type, str(action), 80) for e in elements])
    maxRatio = max(score)
    el = np.array(elements)
    el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
    if len(el) > 0:
        mouse.LeftClick(el[0].x_center, el[0].y_center)
        return
    match, score = zip(*[matchText(e.text, str(action), 70) for e in elements])
    maxRatio = max(score)
    el = np.array(elements)
    el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
    if len(el) > 0:
        mouse.LeftClick(el[0].x_center, el[0].y_center)
        return
    if center is not None:
        mouse.LeftClick(center[0], center[1])
    if action == "copy":
        sh.Copy()
    elif action == "paste":
        sh.Paste()
    elif action == "cut":
        sh.Cut()
    elif action == "find":
        sh.Find()
    elif action == "close":
        sh.Close()
    elif action == "undo":
        sh.Undo()
    elif action == "redo":
        sh.Redo()
    elif action == "save":
        sh.Save()
    else:
        raise ValueError(Actions.undefined)


def getRelativeDrag(directions, quantity):
    x = 0
    y = 0
    if type(directions) is not list:
        directions = [directions]

    for direction in directions:
        if direction in ["up", "top"]:
            y = -quantity
        elif direction in ["down", "bottom"]:
            y = quantity
        elif direction in ["left", "east"]:
            x = -quantity
        elif direction in ["right", "west"]:
            x = quantity
    return x, y


def actionMapper(elements, action, action_type, center_1, center_2=None, t_input=None, quantity=None, direction=None):
    if action_type == Actions.click:
        if "east" in action and "double" in action:
            mouse.DoubleLeftClick(center_1[0], center_1[1])
        elif "right" in action and "double" in action:
            mouse.DoubleRightClick(center_1[0], center_1[1])
        elif "right" in action:
            mouse.Rightclick(center_1[0], center_1[1])
        else:
            mouse.LeftClick(center_1[0], center_1[1])

    elif action_type == Actions.wait:
        if quantity is None:
            quantity = 2
        r.wait(quantity)

    elif action_type == Actions.hover:
        r.hover(center_1[0], center_1[1])

    elif action_type == Actions.write:
        mouse.LeftClick(center_1[0], center_1[1])
        k.Write(t_input)

    elif action_type == Actions.drag:
        if quantity is None:
            quantity = 10
        r.hover(center_2[0], center_2[1])
        if center_1 is not None:   # it means that i have a target destination
            mouse.Drag(center_1[0], center_1[1])
        elif direction is not None:
            x, y = getRelativeDrag(direction, quantity)
            mouse.RelativeDrag(x, y)
        else:
            print("destination is not specified")

    elif action_type == Actions.delete:
        mouse.LeftClick(center_1[0], center_1[1])
        sh.MarkAll()
        k.KeyPress('backspace')

    elif action_type == Actions.scroll:
        if quantity is not None:
            if direction is None or direction in ["down", "bottom"]:
                quantity = - quantity
            mouse.scroll(quantity)
        else:
            mouse.scroll(5)

    elif action_type == Actions.key:
        k.KeyPress(t_input)

    elif action_type == Actions.other:
        otherActions(action[-1], elements,center_1)

    else:
        raise ValueError(action_type)


@dataclass
class CustomPOS:
    action: list = None
    target_element: spacy.tokens.doc.Doc = None
    source_element: spacy.tokens.doc.Doc = None
    direction: spacy.tokens.doc.Doc = None
    quantity: int = None
    input: str = ""


def getBoundaries(direction, action, quantity_st, quantity_nd, org_size):
    ordered_parts = []
    [ordered_parts.append([x.i for x in p]) for p in [[action], [direction], [quantity_st, quantity_nd]] if p[0] is not None]
    ordered_parts.sort(key=lambda x: x[0])
    ordered_parts.append([org_size])
    print(ordered_parts)
    empty_range = []
    for i in range(len(ordered_parts)-1, 0, -1):
        diff = ordered_parts[i][0]-ordered_parts[i-1][-1]
        if diff > 1:
            empty_range.append([ordered_parts[i-1][-1]+1, ordered_parts[i][0]-1])
    print(empty_range)
    return empty_range


def getSentenceStructure(sentence, elements):
    pos = CustomPOS()
    to_index = None
    quantity_st = None
    quantity_nd = None
    action_type, actions, rights, quantity = getActionType(sentence, elements)
    for right in rights:
        if str(right) in ["up", "upwards", "down", "downwards"]:
            pos.direction = right
            break
        elif str(right) == "to":
            to_index = right.i
    pos.action = actions
    if quantity is not None:
        pos.quantity = quantity[0]

    simple_actions = [Actions.click, Actions.write, Actions.hover, Actions.delete, Actions.key, Actions.other]
    if action_type in simple_actions:
        # pos.direction = None
        # empty_range = getBoundaries(pos.direction, actions[-1], quantity_st, quantity_nd, len(sentence))
        pos.target_element = sentence[actions[-1].i+1:]

    elif action_type == Actions.scroll:
        if to_index is not None:
            pos.target_element = sentence[to_index+1:]

    elif action_type == Actions.drag:
        if to_index is not None:
            pos.target_element = sentence[to_index + 1:]
            pos.source_element = sentence[actions[-1].i+1:to_index]
        else:
            pos.source_element = sentence[actions[-1].i+1:]

    elif action_type == Actions.undefined:
        raise ValueError(action_type)
    return pos, action_type


from objectMatcher import objectSplitter
text = nlp("drag the the {ok} button inside the dialog box to the left of the {file} menu by 5 pixels")
print(getSentenceStructure(text, e9))
print(objectSplitter(text))
# print(cardinalRemover(text))
