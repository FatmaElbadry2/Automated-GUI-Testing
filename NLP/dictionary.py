from enum import Enum


class Actions(Enum):  # return type of the sentence
    click = 0
    scroll = 1
    drag = 2
    write = 3
    screenshot = 4
    hover = 5
    delete = 6
    wait = 7
    key = 8
    other = 9
    undefined = 10


verbs = {
    "click": Actions.click,
    "push": Actions.click,
    "press": Actions.click,  # Actions.key],
    "hit": Actions.click,
    "open": Actions.click,
    "close": Actions.click,
    "tap": Actions.click,
    "tick": Actions.click,
    "switch": Actions.click,
    "refresh": Actions.click,
    "check": Actions.click,
    "select": Actions.click,
    "choose": Actions.click,
    "pick": Actions.click,
    "add": Actions.write,
    "write": Actions.write,
    "type": Actions.write,
    "enter": Actions.write,
    "compose": Actions.write,
    "go": Actions.hover,
    "point": Actions.hover,
    "fix": Actions.hover,
    "pin": Actions.hover,
    "save": Actions.other,
    "cut": Actions.other,
    "copy": Actions.other,
    "paste": Actions.other,
    "undo": Actions.other,
    "redo": Actions.other,
    "scroll": Actions.drag,
    "drag": Actions.drag,
    "drop": Actions.drag,
    "move": Actions.drag,
    "delete": Actions.delete,
    "remove": Actions.delete,
    "wait": Actions.wait
}


objects =\
    [
        "cursor",
        "home",
        "option",
        "object",
        "target",
        "element",
        "item",
        "one",
        "screen",
        "page",
        "window",
        "program",
        "application",
        "app",
        "mouse",
        "keyboard",
        "file",
        "directory",
        "corner",
        "empty",
        "key",
        "part",
        "field"
    ]

absPositions =\
[
    "top",
    "bottom",
    "middle",
    "left",
    "right",
    "up",
    "down",
    "next",
    "east",
    "west",
    "upper",
    "lower",
    "swipe"

]

colorAdj = ["light", "dark"]



# elementsMatcher = {
#     "button": 0,
#     "label": 1,
#     "radio_button": 2,
#     "textbox": 3,
#     "checkbox": 4,
#     "combobox": 5,
#     "spinbox": 6,
#     "menu": 7,
#     "submenu": 8,
#     "scrollbar": 9,
#     "progressbar": 10,
#     "dial": 11,
#     "tab": 12,
#     "tab_bar": 13,
#     "table": 14,
#     "slider": 15,
#     "calendar": 16,
#     "link": 17,
#     "switch": 18,
#     "icon_button": 19,
#     "dialogbox": 20,
#     "textarea": 21,
#     "close": 22,
#     "save": 23,
#     "load": 24,
#     "redo": 25,
#     "undo": 26,
#     "export": 27,
#     "new": 28,
#     "info": 29,
#     "search": 30,
#     "settings": 31,
#     "max_min": 32,
#     "dropdown": 33,
#     "text_combobox": 34,
#     "button_combobox": 35
# }


