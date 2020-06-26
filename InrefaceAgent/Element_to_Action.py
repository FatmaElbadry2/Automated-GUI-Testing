
from InrefaceAgent.imports import *


class Actions(Enum):
    left_click = 0
    double_left_click = 1
    right_click = 2
    drag_up = 3
    drag_down = 4
    drag_left = 5
    drag_right = 6
    write_letters = 7
    write_numbers = 8
    write_alphanumeric = 9
    write_long = 10
    write_short = 11
    delete = 12
    undefined = 13
    click_no_change = 14


click = ["button", "tab"]

one_click = ["combobox", "submenu",  "icon_button", "close", "save", "load", "redo", "undo", "export", "new", "info", "settings", "max_min", "dropdown", "button_combobox"]

click_no_change = ["radio_button", "checkbox", "switch"]

write = ["textbox", "textarea", "search", "text_combobox", "spinbox"]
drag_horizontal = ["horizontal_scrollbar"]
drag_vertical = ["vertical_scrollbar"]


def element_action_mapper(type):
    if type in click:
        return [Actions.double_left_click, Actions.left_click]
    elif type in one_click:
        return [Actions.left_click]
    elif type in click_no_change:
        return [Actions.click_no_change]
    elif type in write:
        return [Actions.write_letters, Actions.write_numbers, Actions.write_alphanumeric, Actions.write_short,\
               Actions.write_long, Actions.delete]
    elif type in drag_horizontal:
        return [Actions.drag_left, Actions.drag_right]
    elif type in drag_vertical:
        return [Actions.drag_up, Actions.drag_down]

    return None
