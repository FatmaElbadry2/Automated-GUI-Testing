from GUI_Imports import *
from global_imports import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class ConfigurationWidget(QWidget):
    run_signal = QtCore.pyqtSignal(str, str, str) #file type & file path & check file
    def __init__(self, session_file, steps_file, check_file, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'Run configuration'
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 350
        self.setFixedSize(600, 350)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowMinimizeButtonHint))

        self.type = "crash"
        self.session_file = session_file
        self.steps_file = steps_file
        self.check_file = check_file
        self.expand_check = False

        self.Initialize()

        self.AddItems()

    def Initialize(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def AddItems(self):
        self.arrow_button = QPushButton("", self)
        self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        self.arrow_button.setIconSize(QSize(10, 10))
        self.arrow_button.clicked.connect(self.Expand)
        self.arrow_button.move(25, 30)
        qss = """
                        QPushButton {
                            background-color: rgba(0,0,0,0);
                            border: none;
                        }"""
        self.arrow_button.setStyleSheet(qss)
        self.arrow_button.setCursor(QCursor(Qt.PointingHandCursor))

        label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        label.setFont(font)
        label.setText("Set run configurations:")
        label.setAlignment(Qt.AlignLeft)
        label.move(46, 28)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(162, 32)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(400)

        self.crash_rbtn = QRadioButton("Find crashes", self)
        self.crash_rbtn.setChecked(True)
        self.crash_rbtn.type = "crash"
        self.crash_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.crash_rbtn.move(60, 73)
        self.crash_rbtn.hide()

        self.test_rbtn = QRadioButton("Run a test case", self)
        self.test_rbtn.type = "test"
        self.test_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.test_rbtn.move(185, 73)
        self.test_rbtn.hide()

        self.session_label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        self.session_label.setFont(font)
        self.session_label.setText("Session path:")
        self.session_label.setAlignment(Qt.AlignLeft)
        self.session_label.move(81, 120)
        self.session_label.hide()

        self.path_textbox = QLineEdit(self)
        self.path_textbox.move(160, 115)
        self.path_textbox.setText(self.session_file)
        self.path_textbox.setFixedWidth(380)
        self.path_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 5px;
                }"""
        self.path_textbox.setStyleSheet(qss)
        self.path_textbox.hide()

        self.check_1 = QCheckBox("", self)
        self.check_1.move(81, 120)
        self.check_1.hide()
        self.steps_textbox = QLineEdit(self)
        self.steps_textbox.move(115, 113)
        self.steps_textbox.setText(self.steps_file)
        self.steps_textbox.setFixedWidth(380)
        self.steps_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 5px;
                }"""
        self.steps_textbox.setStyleSheet(qss)
        self.steps_textbox.hide()


        self.check_2 = QCheckBox("", self)
        self.check_2.move(81, 180)
        self.check_2.hide()
        self.check_textbox = QLineEdit(self)
        self.check_textbox.move(115, 173)
        self.check_textbox.setText(self.steps_file)
        self.check_textbox.setFixedWidth(380)
        self.check_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 5px;
                }"""
        self.check_textbox.setStyleSheet(qss)
        self.check_textbox.hide()

        '''    
        self.warning_button = QPushButton("", self)
        self.warning_button.setIcon(QIcon('imgs/warning.png'))
        self.warning_button.setIconSize(QSize(15, 15))
        # arrow_button.clicked.connect(self.CreatBtnClicked)
        self.warning_button.move(27, 275)
        qss = """
                        QPushButton {
                            background-color: rgba(0,0,0,0);
                            border: none;
                        }"""
        self.warning_button.setStyleSheet(qss)
        self.warning_button.hide()

        self.warning_label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        self.warning_label.setFont(font)
        self.warning_label.setAlignment(Qt.AlignLeft)
        self.warning_label.move(55, 276)
        self.warning_label.hide()'''

        config_button = QPushButton("Configure", self)
        config_button.clicked.connect(self.ConfigureBtnClicked)
        config_button.move(468, 315)
        config_button.setMinimumWidth(100)
        qss = """
                QPushButton {
                    background-color: #cc1db9;
                    border: 5px solid #cc1db9;
                    border-radius: 10px;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                }"""
        config_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 299)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(600)

    def ConfigureBtnClicked(self):
        if type == "crash":
            self.run_signal.emit(self.type, self.session_file, "")
            self.close()
        elif type == "test":
            if self.check_1.isChecked():
                steps = self.steps_file
            else:
                steps = ""
            if self.check_2.isChecked():
                check = self.check_file
            else:
                check = ""
            self.run_signal.emit(self.type, steps, check)
            self.close()

    def Expand(self):
        if self.expand_check == True:
            self.crash_rbtn.hide()
            self.test_rbtn.hide()
            self.session_label.hide()
            self.path_textbox.hide()
            self.check_1.hide()
            self.check_2.hide()
            self.steps_textbox.hide()
            self.check_textbox.hide()
            self.expand_check = False
            self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        else:
            self.crash_rbtn.show()
            self.test_rbtn.show()
            self.session_label.show()
            self.path_textbox.show()
            self.check_1.hide()
            self.check_2.hide()
            self.steps_textbox.hide()
            self.check_textbox.hide()
            self.expand_check = True
            self.arrow_button.setIcon(QIcon('imgs/down-arrow.png'))

    def OnRadioBtnClick(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            #print("Type is %s" % (radioButton.type))
            self.type = radioButton.type
            if self.type == "crash":
                self.session_label.show()
                self.path_textbox.show()
                self.check_1.hide()
                self.check_2.hide()
                self.steps_textbox.hide()
                self.check_textbox.hide()
            elif self.type == "test":
                self.session_label.hide()
                self.path_textbox.hide()
                self.check_1.show()
                self.check_2.show()
                self.steps_textbox.show()
                self.check_textbox.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    session_file = "C:\\Users\\ssalma\\Documents\\Dexter Projects\\untitled7\\ElmerGUI.ssf"
    steps_file = "C:\\Users\\ssalma\\Documents\\Dexter Projects\\untitled7\\f.txt"
    check_file = "C:\\Users\\ssalma\\Documents\\Dexter Projects\\untitled7\\5.txt"

    main = ConfigurationWidget(session_file, steps_file, check_file)

    main.show()
    sys.exit(app.exec_())