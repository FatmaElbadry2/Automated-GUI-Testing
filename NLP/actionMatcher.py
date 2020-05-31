from NLP.imports import *
from dictionary import *
from preProcessing import *
from agent import keyBoard as k , mouse, shortcuts as sh
import rpa as r
from utils import matchText
from yoloInterface import Element


def getActionType(sentence):
    actions = []
    action_type = Actions.undefined
    rights = []
    for word in sentence:
        if word.dep_ == "ROOT":
            action_type = verbs.get(word.lemma_, -1)
            if action_type == -1:
                return Actions.undefined, None, None
            [actions.append(l) for l in word.lefts]
            actions.append(word)
            rights = [right for right in word.rights]
    return action_type, actions, rights


def otherActions(action, elements):
    match, score = zip(*[matchText(e.type, str(action), 80) for e in elements])
    maxRatio = max(score)
    el = np.array(elements)
    el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
    if len(el) > 0:
        return el[0]
    match, score = zip(*[matchText(e.text, str(action), 70) for e in elements])
    maxRatio = max(score)
    el = np.array(elements)
    el = el[np.logical_and(np.array(score) == maxRatio, np.array(match))]
    if len(el) > 0:
        return el[0]
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
    return action


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
        mouse.scroll(1)

    elif action_type == Actions.key:
        k.KeyPress(t_input)

    elif action_type == Actions.other:
        otherActions(action[-1])

    else:
        raise ValueError(action_type)



