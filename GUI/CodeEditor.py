from GUI_Imports import *
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtGui import QTextCursor
from Completer import *
from SpellChecker import *

try:
    import enchant
    from enchant import DictNotFoundError
    from enchant.errors import Error
    ENCHANT_AVAILABLE = True
except ImportError:
    ENCHANT_AVAILABLE = False

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, autocomplete_array, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        self.completer = MyCompleter(autocomplete_array)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insertCompletion)

        global ENCHANT_AVAILABLE
        # Default dictionary based on the current locale.
        if ENCHANT_AVAILABLE:
            try:
                self.dictionary = enchant.Dict()
                self.highlighter = Highlighter(self.document())
                self.highlighter.spelling_dictionary = self.dictionary
            except (Error, DictNotFoundError):
                ENCHANT_AVAILABLE = False
                log.debug('Could not load default dictionary')

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        tc = self.textCursor()
        if event.key() == Qt.Key_Tab and self.completer.popup().isVisible():
            self.completer.insertText.emit(self.completer.getSelected())
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            return

        QPlainTextEdit.keyPressEvent(self, event)
        tc.select(QTextCursor.WordUnderCursor)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 0:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                        + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(185)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor(Qt.lightGray).lighter(125))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is moved to the location of the pointer.
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                                      event.pos(), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtWidgets.QPlainTextEdit.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()
        actions = popup_menu.actions()
        #print(actions[len(actions)-1])
        popup_menu.removeAction(actions[len(actions)-1])
        # Select the word under the cursor.
        cursor = self.textCursor()
        # only select text if not already selected
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)
        # Add menu with available languages.
        if ENCHANT_AVAILABLE:
            lang_menu = QtWidgets.QMenu(translate('OpenLP.SpellTextEdit', 'Language'))
            for lang in enchant.list_languages():
                action = create_action(lang_menu, lang, text=lang, checked=lang == self.dictionary.tag)
                lang_menu.addAction(action)
            popup_menu.insertSeparator(popup_menu.actions()[0])
            popup_menu.insertMenu(popup_menu.actions()[0], lang_menu)
            lang_menu.triggered.connect(self.set_language)
        # Check if the selected word is misspelled and offer spelling suggestions if it is.
        if ENCHANT_AVAILABLE and self.textCursor().hasSelection():
            text = self.textCursor().selectedText()
            if not self.dictionary.check(text):
                spell_menu = QtWidgets.QMenu(translate('OpenLP.SpellTextEdit', 'Spelling Suggestions'))
                for word in self.dictionary.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correct_word)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are suggestions.
                if spell_menu.actions():
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)
        tag_menu = QtWidgets.QMenu(translate('OpenLP.SpellTextEdit', 'Formatting Tags'))
        popup_menu.exec(event.globalPos())

    def set_language(self, action):
        self.dictionary = enchant.Dict(action.text())
        self.highlighter.spelling_dictionary = self.dictionary
        self.highlighter.highlightBlock(self.toPlainText())
        self.highlighter.rehighlight()

    def correct_word(self, word):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(word)
        cursor.endEditBlock()