# radio-button
# checkbox
# combobox
# spinbox
# menu
# submenu
# scrollbar
# progressbar
# dial
# tab
# tab-bar
# table
# slider
# calendar
# link
# switch
# icon-button
# dialogbox
# textarea
# image
# dialog-box
# close
# save
# load
# max-min
# dropdown
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
