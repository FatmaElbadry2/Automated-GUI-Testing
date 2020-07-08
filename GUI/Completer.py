from PyQt5.QtWidgets import QCompleter
from PyQt5 import QtCore

class MyCompleter(QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, autocomplete_array, parent=None):
        QCompleter.__init__(self, autocomplete_array, parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)
        self.activated.connect(self.getSelected)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        #print(self.lastSelected)
        return self.lastSelected


