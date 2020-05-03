# progressbar i can't find actions to a progress bar
from enum import Enum
class actions(Enum):

    Rightclick=1
    LeftClick=2
    DoubleRightClick=3
    DoubleLeftClick=4
    Scroll=5
    RelativeDrag=6
    Drag=7
    ClickeithInterval=8
    clicks=9
    Write=10
    WriteLetters=11
    WriteNumbers=12
    WriteSpecialCha=13
    TwoKeys=14
    KeyPress=15
    ThreeKeys=16
    pressArrow=17

value = input("Please enter a string:\n")
if value=='button':
    ListOfActions={1,2,3,4}
elif value=='textbox':
    ListOfActions={1,2,3,4,10,11,12,13,14,15,16,17}
elif value=='radio-button':
    ListOfActions={1,2,3,4}
elif value=='label':
    ListOfActions={1,2,3,4}
elif value == 'checkbox':
    ListOfActions = {2,4}
elif value == 'combobox':
    ListOfActions = {2,4}
elif value == 'spinbox':
    ListOfActions = {1,2,3,4}
elif value == 'menu' or value=='submenu':
    ListOfActions = {2}
elif value == 'scrollbar':
    ListOfActions = {1,2,4,5,6,7,9}
elif value == 'close' or value=='save' or 'load':
    ListOfActions = {1,2}
elif value == 'dial':
    ListOfActions = {2,4,6,7,9}
elif value=='tab' or value=='tab-bar' or value=='switch':
    ListOfActions={2}
elif value=='icon-button':
    ListOfActions={1,2}
elif value=='textarea':
    ListOfActions={1,2,6,7,10,11,12,13,14,15,16,17}
elif value=='dropdown':
    ListOfActions={1,2}
elif value=='dialog-box':
    ListOfActions={2}
elif value == 'slider':
    ListOfActions = {1,2,4,6,7,9}
elif value=='link':
    ListOfActions={1,2}
elif value=='max-min':
    ListOfActions={2,4,6,7,8,9}
elif value=='table':
    ListOfActions = {1,2,4,5,6,7,9,10,11,12,13,14,15,16,17}
elif value=='calendar':
    ListOfActions = {1,2,4,5,6,7,9,10,11,12,13,17}
elif value=='image':
    ListOfActions = {1,2}



