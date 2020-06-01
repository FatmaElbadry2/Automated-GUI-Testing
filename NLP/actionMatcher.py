from NLP.imports import *
from spacy.tokens import Span
from dictionary import *
from preProcessing import *
from agent import keyBoard as k, mouse, shortcuts as sh
import rpa as r
from utils import matchText
from yoloInterface import Element
from objectMatcher import objectTypeMapper, Errors
from dataclasses import dataclass


def getScrollType(elements):
    _, _, error = objectTypeMapper("scrollbar", False, None, None, elements, [0, w_width], [0, w_height])
    if error != Errors.no_error:
        action_type = Actions.scroll
    else:
        action_type = Actions.drag
    return action_type


def getActionType(sentence, elements):
    actions = []
    action_type = Actions.undefined
    rights = []
    quantity = []
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
            quantity.append(word)
            parent = list(word.ancestors)
            if len(parent) > 0:
                quantity.append(parent[0])
    return action_type, actions, rights, quantity


def otherActions(action, elements,center):
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


def actionMapper(action, action_type, center_1, center_2=None, t_input=None, quantity=None, direction=None):
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
        r.hover(center_1[0], center_1[1])
        mouse.Drag(center_2[0], center_2[1])

    elif action_type == Actions.delete:
        mouse.LeftClick(center_1[0], center_1[1])
        sh.MarkAll()
        k.KeyPress('backspace')

    elif action_type == Actions.scroll:
        if quantity is not None:
            if direction == "down":
                quantity = - quantity
            mouse.scroll(quantity)
        else:
            mouse.scroll(1)

    elif action_type == Actions.key:
        k.KeyPress(t_input)

    elif action_type == Actions.other:
        otherActions(action[-1], center_1)

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


def getSentenceStructure(sentence, elements):
    pos = CustomPOS()
    to_index = None
    action_type, actions, rights, quantity = getActionType(sentence, elements)

    for right in rights:
        if str(right) in ["up", "upwards", "down", "downwards"]:
            pos.direction = right
            break
        elif str(right) == "to":
            to_index = right.i

    pos.action = actions
    if len(quantity) > 0:
        pos.quantity = quantity[0]

    simple_actions = [Actions.click, Actions.write, Actions.hover, Actions.delete, Actions.key, Actions.other]
    if action_type in simple_actions:
        pos.target_element = sentence[actions[-1].i+1:]

    elif action_type == Actions.scroll:
        if to_index is not None:
            pos.target_element = sentence[to_index+1:]

    elif action_type == Actions.drag:
        if to_index is not None:
            pos.target_element = sentence[to_index + 1:]
            pos.source_element = sentence[actions[-1]+1:to_index]
        else:
            pos.source_element = sentence[actions[-1]:to_index]

    elif action_type == Actions.undefined:
        raise ValueError(action_type)
    return pos


