from GUI_Imports import *

log = logging.getLogger(__name__)

class Highlighter(QtGui.QSyntaxHighlighter):
    """
    Provides a text highlighter for pointing out spelling errors in text.
    """
    WORDS = '(?iu)[\w\']+'

    def __init__(self, *args):
        super(Highlighter, self).__init__(*args)
        self.spelling_dictionary = None

    def highlightBlock(self, text):
        if not self.spelling_dictionary:
            return

        text = str(text)
        if text!="":
            check = text[0].isupper()
            if check == True:
                return

        char_format = QtGui.QTextCharFormat()
        char_format.setUnderlineColor(QtCore.Qt.red)
        char_format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)
        for word_object in re.finditer(self.WORDS, text):
            if not self.spelling_dictionary.check(word_object.group()):
                self.setFormat(word_object.start(), word_object.end() - word_object.start(), char_format)


class SpellAction(QtWidgets.QAction):
    correct = QtCore.pyqtSignal(str)
    def __init__(self, *args):
        super(SpellAction, self).__init__(*args)
        self.triggered.connect(lambda x: self.correct.emit(self.text()))