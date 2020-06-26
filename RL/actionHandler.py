from InrefaceAgent import mouse, keyboard as k, Element_to_Action as eta, shortcuts as sh
from RL.tree import *

def DecimalToBinary(n):
    return bin(n).replace("0b", "")

def ActionDecoder(action):  # it should return the ranges of Ids for each element in the action space
    action_type = eta.Actions
    if action in range(1, 601):
        return action_type.left_click
    elif action in range(601, 901):
        return action_type.click_no_change
    elif action in range(901, 1201):
        return action_type.double_left_click
    elif action in range(1201, 1401):
        return action_type.write_letters
    elif action in range(1401, 1601):
        return action_type.write_numbers
    elif action in range(1601, 1801) :
        return action_type.write_short
    elif action in range (1801, 2001):
        return action_type.write_long
    elif action in range (2001, 2201):
        return action_type.write_alphanumeric
    elif action in range(2201, 2401):
        return action_type.delete
    elif action in range(2401, 2426):
        return action_type.drag_up
    elif action in range(2426, 2451):
        return action_type.drag_down
    elif action in range(2451, 2476):
        return action_type.drag_right
    elif action in range(2476, 2501):
        return action_type.drag_left
    else:
        return action_type.undefined

def ActionExecuter(action_type, x, y):
    #y = y + 7
    action_type_enum = eta.Actions
    if (action_type == action_type_enum.left_click) or (action_type == action_type_enum.click_no_change):
        mouse.LeftClick(x, y)
    elif action_type == action_type_enum.double_left_click:
        mouse.DoubleLeftClick(x, y)
    elif action_type == action_type_enum.write_letters:
        mouse.LeftClick(x,y)
        k.Write('saloumi')
    elif action_type == action_type_enum.write_numbers:
        mouse.LeftClick(x, y)
        k.write('123456789')
    elif action_type == action_type_enum.write_short:
        mouse.LeftClick(x,y)
        k.Write('F')
    elif action_type == action_type_enum.write_long:
        mouse.LeftClick(x,y)
        k.Write('super cali fragilistic expialidocious, even though the sound of it is something quite atrocious')
    elif action_type == action_type_enum.write_alphanumeric:
        mouse.LeftClick(x,y)
        k.Write('%of\nk*?##@ghk123')
    elif action_type == action_type_enum.delete:
        mouse.LeftClick(x,y)
        sh.MarkAll()
        sh.Delete()
    elif action_type == action_type_enum.drag_up:
        mouse.RelativeDrag(0, -10)
    elif action_type == action_type_enum.drag_down:
        mouse.RelativeDrag(0, 10)
    elif action_type == action_type_enum.drag_left:
        mouse.RelativeDrag(-10, 0)
    elif action_type == action_type_enum.drag_right:
        mouse.RelativeDrag(10, 0)





