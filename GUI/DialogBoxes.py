from GUI_Imports import *
from global_imports import *

class NewProjectWidget(QWidget):
    create_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'Create Project'
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 400
        self.setFixedSize(600, 400)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowMinimizeButtonHint))
        self.default_folder_found = False
        self.DEF_DIR = os.path.expanduser('~/Documents')
        dir_list = self.DEF_DIR.split('/')
        self.DEF_DIR = dir_list[0] + "\\Documents"
        self.default_path = self.DEF_DIR + "\\Dexter Projects"
        self.CheckDefaultPath(self.default_path)
        #print(self.default_path)
        self.folders = os.walk(self.default_path)
        self.folders = list(self.folders)[0][1]
        self.taken_array = self.FixDirectory()
        self.index = self.GetIndex()
        self.default_project_name = "untitled"
        self.project_path = self.SetProjectPath()
        self.created_project_path = ""

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
        label = QLabel(self)
        font = QFont()
        font.setPointSize(9)
        label.setFont(font)
        label.setText("Location:")
        label.setAlignment(Qt.AlignLeft)
        label.move(25, 27)

        self.path_textbox = QLineEdit(self)
        self.path_textbox.move(90, 22)
        self.path_textbox.setText(self.project_path)
        self.path_textbox.setFixedWidth(480)
        self.path_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                }"""
        self.path_textbox.setStyleSheet(qss)
        self.path_textbox.setSelection(len(self.default_path)+1, len(self.project_path))

        open_button = QPushButton("", self)
        open_button.clicked.connect(self.OpenBtnClicked)
        open_button.move(542, 26)
        #open_button.setMinimumWidth(80)
        open_button.setIcon(QtGui.QIcon("imgs/open-folder.png"))
        qss = """
                        QPushButton {
                            background-color: rgba(0,0,0,0);
                            border: none;
                        }"""
        open_button.setStyleSheet(qss)


        create_button = QPushButton("Create", self)
        create_button.clicked.connect(self.CreatBtnClicked)
        create_button.move(485, 355)
        create_button.setMinimumWidth(80)
        qss = """
                QPushButton {
                    background-color: #cc1db9;
                    border: 5px solid #cc1db9;
                    border-radius: 10px;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                }"""
        create_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 330)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(600)

    def CheckDefaultPath(self, path):
        check = os.path.exists(path)
        if check == False:
            access_rights = 0o755
            try:
                os.mkdir(path, access_rights)
            except OSError:
                print("Creation of the main directory %s failed" % path)
            else:
                print("Successfully created the main directory %s" % path)

    def FixDirectory(self):
        array = []
        for folder in self.folders:
            if folder == "untitled":
                self.default_folder_found = True
                pass
            elif 'untitled'in folder:
                folder = folder[8:]
                if folder[0].isdigit():
                    array.append(int(folder))
                    #print(folder)
        #print(array)
        return array

    def GetIndex(self):
        if self.taken_array == []:
            index = 1
        else:
            index = self.taken_array[len(self.taken_array)-1]+1
            if self.taken_array[0] != 1:
                index = 1
            else:
                for i in range(len(self.taken_array)-1):
                    if self.taken_array[i] + 1 != self.taken_array[i+1]:
                        index = self.taken_array[i] + 1
        #print(index)
        return index

    def SetProjectPath(self):
        if not self.default_folder_found:
            path = self.default_path + "\\" + self.default_project_name
        else:
            path = self.default_path + "\\" + self.default_project_name + str(self.index)
        return path

    def CreatBtnClicked(self):
        access_rights = 0o755
        path = self.path_textbox.text()
        try:
            os.mkdir(path, access_rights)
        except OSError:
            self.hide()
            #print("Creation of the directory %s failed" % path)
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10,10,0,0)
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("The directory " + path + "is not empty. Would you like to create a project in another directory instead?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setWindowTitle("Directory Error")
            choice = msg.exec_()
            if choice == 65536:
                self.close()
            else:
                self.show()
        else:
            #print("Successfully created the directory %s" % path)
            self.project_path = path
            self.parent.project_path = path
            self.create_signal.emit()
            self.close()

    def OpenBtnClicked(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory", self.default_path))
        if path!="":
            self.project_path = path
        self.path_textbox.setText(self.project_path)


class ImportWidget(QWidget):
    import_signal = QtCore.pyqtSignal(str, str, str)
    open_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'Import test case'
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 350
        self.setFixedSize(600, 350)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowMinimizeButtonHint))

        self.project_path = ""
        self.imported_path = ""
        self.file_name = ""
        self.type = "steps"
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
        self.path_textbox = QLineEdit(self)
        self.path_textbox.move(27, 22)
        self.path_textbox.setText(self.imported_path)
        self.path_textbox.setFixedWidth(543)
        self.path_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                }"""
        self.path_textbox.setStyleSheet(qss)

        open_button = QPushButton("", self)
        open_button.clicked.connect(self.OpenBtnClicked)
        open_button.move(542, 26)
        #open_button.setMinimumWidth(80)
        open_button.setIcon(QtGui.QIcon("imgs/open-folder.png"))
        qss = """
                        QPushButton {
                            background-color: rgba(0,0,0,0);
                            border: none;
                        }"""
        open_button.setStyleSheet(qss)

        label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        label.setFont(font)
        label.setText("Import name:")
        label.setAlignment(Qt.AlignLeft)
        label.move(35, 85)

        self.import_name_txtbox = QLineEdit(self)
        self.import_name_txtbox.move(110, 80)
        #self.import_name_txtbox.setText(self.imported_path)
        self.import_name_txtbox.setFixedWidth(300)
        self.import_name_txtbox.setMinimumHeight(25)
        qss = """
                                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                                }"""
        self.import_name_txtbox.setStyleSheet(qss)

        self.arrow_button = QPushButton("", self)
        self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        self.arrow_button.setIconSize(QSize(10,10))
        self.arrow_button.clicked.connect(self.Expand)
        self.arrow_button.move(25, 144)
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
        label.setText("Set test case file type:")
        label.setAlignment(Qt.AlignLeft)
        label.move(46, 142)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(162, 146)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(400)

        self.steps_rbtn = QRadioButton("Test steps", self)
        self.steps_rbtn.setChecked(True)
        self.steps_rbtn.type = "steps"
        self.steps_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.steps_rbtn.move(60, 185)
        self.steps_rbtn.hide()

        self.check_rbtn = QRadioButton("Check", self)
        self.check_rbtn.type = "check"
        self.check_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.check_rbtn.move(175, 185)
        self.check_rbtn.hide()

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
        self.warning_label.hide()

        import_button = QPushButton("Import", self)
        import_button.clicked.connect(self.ImportBtnClicked)
        import_button.move(488, 315)
        import_button.setMinimumWidth(80)
        qss = """
                        QPushButton {
                            background-color: #cc1db9;
                            border: 5px solid #cc1db9;
                            border-radius: 10px;
                            color: white;
                            font-size: 12px;
                            font-weight: bold;
                        }"""
        import_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 299)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(600)

    def ImportBtnClicked(self):
        self.file_name = self.import_name_txtbox.text()
        path = self.path_textbox.text()
        path_arr = path.split("/")
        new_path = ""
        for str in path_arr:
            new_path = new_path + str + "\\"
        new_path = new_path[:len(new_path) - 1]
        if self.path_textbox.text() == "":
            self.warning_label.setText("File name can't be empty.")
            self.warning_label.show()
            self.warning_button.show()
        elif not os.path.isfile(self.path_textbox.text()):
            self.warning_label.setText("File doesn't exist.")
            self.warning_label.show()
            self.warning_button.show()
        elif self.project_path in new_path:
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("The chosen file is in the same project directory: " + self.project_path + ". Would you like to open it instead?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setWindowTitle("Directory Error")
            choice = msg.exec_()
            if choice == 65536:
                self.close()
            else:
                self.open_signal.emit()
                self.close()
        else:
            self.imported_path = new_path
            self.import_signal.emit(self.imported_path, self.type, self.file_name)
            self.close()

    def OpenBtnClicked(self):
        self.warning_label.hide()
        self.warning_button.hide()
        path, _ = QFileDialog.getOpenFileName(self, "Import file", self.project_path, "Text documents (*.txt)")
        if path:
            path_arr = path.split("/")
            self.file_name = path_arr[len(path_arr) - 1]
            self.imported_path = path
        self.path_textbox.setText(self.imported_path)
        self.import_name_txtbox.setText(self.file_name)

    def Expand(self):
        if self.expand_check == True:
            self.steps_rbtn.hide()
            self.check_rbtn.hide()
            self.expand_check =False
            self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        else:
            self.steps_rbtn.show()
            self.check_rbtn.show()
            self.expand_check = True
            self.arrow_button.setIcon(QIcon('imgs/down-arrow.png'))

    def OnRadioBtnClick(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            #print("Type is %s" % (radioButton.type))
            self.type = radioButton.type

class NewFileWidget(QWidget):
    new_file_signal = QtCore.pyqtSignal(str, str)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'Import test case'
        self.top = 0
        self.left = 0
        self.width = 350
        self.height = 120
        self.setFixedSize(350, 120)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setFocus()
        QtWidgets.qApp.focusChanged.connect(self.OnFocusChanged)

        self.project_path = ""
        self.type = "steps"
        self.qss_normal = """
                        QPushButton {
                            background-color: white;
                            border: 1px solid;
                            border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                            color: black;
                            font-size: 11px;
                        }"""
        self.qss_selected = """
                        QPushButton {
                            background-color: #e16cd5;
                            border: 1px solid;
                            border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                            color: white;
                            font-size: 11px;
                        }"""

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
        label = QLabel(self)
        font = QFont()
        font.setPointSize(9)
        label.setFont(font)
        label.setText("New Testcase File")
        label.setAlignment(Qt.AlignLeft)
        label.move(120, 10)

        self.name_textbox = QLineEdit(self)
        self.name_textbox.move(0, 35)
        self.name_textbox.setFixedWidth(350)
        self.name_textbox.setMinimumHeight(35)
        qss = """
                QLineEdit {background: white; border: none; padding: 0px 0px 0px 30px;
                }"""
        self.name_textbox.setStyleSheet(qss)
        self.name_textbox.setPlaceholderText("Name")
        font = QFont()
        font.setPointSize(9)
        self.name_textbox.setFont(font)
        self.name_textbox.returnPressed.connect(self.EnterKeyPressed)

        file_button = QPushButton("", self)
        file_button.move(5, 44)
        file_button.setIcon(QtGui.QIcon("imgs/session.png"))
        file_button.setIconSize(QSize(17, 17))
        qss = """
                QPushButton {
                    background-color: rgba(0,0,0,0);
                    border: none;
                }"""
        file_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, -4)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(350)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 65)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(350)

        self.steps_button = QPushButton("Test Steps file", self)
        self.steps_button.clicked.connect(self.ToggleStepsBtn)
        self.steps_button.move(0, 70)
        self.steps_button.setMinimumWidth(350)
        qss = """
                QPushButton {
                    background-color: #e16cd5;
                    border: 1px solid;
                    border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                    color: white;
                    font-size: 11px;
                }"""
        self.steps_button.setStyleSheet(qss)
        self.steps_button.setMinimumHeight(25)

        self.check_button = QPushButton("Check file", self)
        self.check_button.clicked.connect(self.ToggleCheckBtn)
        self.check_button.move(0, 95)
        self.check_button.setMinimumWidth(350)
        qss = """
                QPushButton {
                    background-color: white;
                    border: 1px solid;
                    border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                    color: black;
                    font-size: 11px;
                }"""
        self.check_button.setStyleSheet(qss)
        self.check_button.setMinimumHeight(25)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb;}")
        v_line.move(0, 0)
        v_line.setMinimumHeight(120)
        v_line.setMinimumWidth(5)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0)  #cbcbcb rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);}")
        v_line.move(250, 0)
        v_line.setMinimumHeight(120)
        v_line.setMinimumWidth(5)

    def ToggleStepsBtn(self):
        self.check_button.setStyleSheet(self.qss_normal)
        self.steps_button.setStyleSheet(self.qss_selected)
        self.type = "step"

    def ToggleCheckBtn(self):
        self.steps_button.setStyleSheet(self.qss_normal)
        self.check_button.setStyleSheet(self.qss_selected)
        self.type = "check"

    def EnterKeyPressed(self):
        if self.name_textbox.text() != "":
            if not os.path.isfile(self.project_path + "\\" + self.name_textbox.text() + ".txt"):
                self.new_file_signal.emit(self.name_textbox.text(), self.type)
                self.close()
            else:
                self.close()
                msg = QMessageBox(self)
                msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                msg.setContentsMargins(10, 10, 0, 0)
                msg.setIcon(QMessageBox.Critical)
                msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                msg.setText("Cannot create file: " + self.project_path + "\\" + self.name_textbox.text() + ".txt" + ". File already exists.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("File Error")
                msg.exec_()

    @QtCore.pyqtSlot("QWidget*", "QWidget*")
    def OnFocusChanged(self, old, now):
        if self.isActiveWindow() == False:
            self.close()
        '''if now == None:
            self.close()'''


class RenameFileWidget(QWidget):
    rename_file_signal = QtCore.pyqtSignal(str, int)
    def __init__(self, type, parent=None):
        super().__init__()
        self.parent = parent
        self.top = 0
        self.left = 0
        self.width = 350
        self.height = 70
        self.setFixedSize(350, 70)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setFocus()
        QtWidgets.qApp.focusChanged.connect(self.OnFocusChanged)

        self.project_path = ""
        self.type = type #0 for .txt and 1 for .ssf

        self.Initialize()
        self.AddItems()

    def Initialize(self):
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def AddItems(self):
        label = QLabel(self)
        font = QFont()
        font.setPointSize(9)
        label.setFont(font)
        label.setText("Rename File")
        label.setAlignment(Qt.AlignLeft)
        label.move(120, 10)

        self.name_textbox = QLineEdit(self)
        self.name_textbox.move(0, 35)
        self.name_textbox.setFixedWidth(350)
        self.name_textbox.setMinimumHeight(35)
        qss = """
                QLineEdit {background: white; border: none; padding: 0px 0px 0px 30px;
                }"""
        self.name_textbox.setStyleSheet(qss)
        self.name_textbox.setPlaceholderText("Name")
        font = QFont()
        font.setPointSize(9)
        self.name_textbox.setFont(font)
        self.name_textbox.returnPressed.connect(self.EnterKeyPressed)

        file_button = QPushButton("", self)
        file_button.move(5, 44)
        file_button.setIcon(QtGui.QIcon("imgs/session.png"))
        file_button.setIconSize(QSize(17, 17))
        qss = """
                QPushButton {
                    background-color: rgba(0,0,0,0);
                    border: none;
                }"""
        file_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, -4)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(350)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 65)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(350)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb;}")
        v_line.move(0, 0)
        v_line.setMinimumHeight(120)
        v_line.setMinimumWidth(5)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0)  #cbcbcb rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);}")
        v_line.move(250, 0)
        v_line.setMinimumHeight(120)
        v_line.setMinimumWidth(5)

    def EnterKeyPressed(self):
        if self.name_textbox.text() != "":
            if self.type == 0:
                if not os.path.isfile(self.project_path + "\\" + self.name_textbox.text() + ".txt"):
                    self.rename_file_signal.emit(self.name_textbox.text(), self.type)
                    self.close()
                else:
                    self.close()
                    msg = QMessageBox(self)
                    msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                    msg.setContentsMargins(10, 10, 0, 0)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                    msg.setText("Cannot rename file: " + self.project_path + "\\" + self.name_textbox.text() + ".txt" + ". File name already exists.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setWindowTitle("Rename file Error")
                    msg.exec_()
            elif self.type == 1:
                if not os.path.isfile(self.project_path + "\\" + self.name_textbox.text() + ".ssf"):
                    self.rename_file_signal.emit(self.name_textbox.text(), self.type)
                    self.close()
                else:
                    self.close()
                    msg = QMessageBox(self)
                    msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                    msg.setContentsMargins(10, 10, 0, 0)
                    msg.setIcon(QMessageBox.Critical)
                    msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                    msg.setText("Cannot rename file: " + self.project_path + "\\" + self.name_textbox.text() + ".txt" + ". File name already exists.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setWindowTitle("Rename file Error")
                    msg.exec_()

    @QtCore.pyqtSlot("QWidget*", "QWidget*")
    def OnFocusChanged(self, old, now):
        if self.isActiveWindow() == False:
            self.close()
        '''if now == None:
            self.close()'''


class NewSessionWidget(QWidget):
    create_signal = QtCore.pyqtSignal(str, str, str, str) #session name, type, app path, model
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'New Session'
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 350
        self.setFixedSize(600, 350)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowMinimizeButtonHint))

        self.project_path = ""
        self.app_path = ""
        self.session_name = ""
        self.type = "testing"
        self.model_path = ""
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
        label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        label.setFont(font)
        label.setText("Session name:")
        label.setAlignment(Qt.AlignLeft)
        label.move(30, 30)

        self.session_name_txtbox = QLineEdit(self)
        self.session_name_txtbox.move(115, 25)
        #self.import_name_txtbox.setText(self.imported_path)
        self.session_name_txtbox.setFixedWidth(300)
        self.session_name_txtbox.setMinimumHeight(25)
        qss = """
                                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                                }"""
        self.session_name_txtbox.setStyleSheet(qss)

        self.path_textbox = QLineEdit(self)
        self.path_textbox.move(27, 83)
        self.path_textbox.setText(self.app_path)
        self.path_textbox.setFixedWidth(543)
        self.path_textbox.setMinimumHeight(25)
        self.path_textbox.setPlaceholderText("App Path")
        qss = """
                        QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                        }"""
        self.path_textbox.setStyleSheet(qss)

        open_button = QPushButton("", self)
        open_button.clicked.connect(self.OpenBtnClicked)
        open_button.move(542, 87)
        # open_button.setMinimumWidth(80)
        open_button.setIcon(QtGui.QIcon("imgs/open-folder.png"))
        qss = """
                                QPushButton {
                                    background-color: rgba(0,0,0,0);
                                    border: none;
                                }"""
        open_button.setStyleSheet(qss)

        self.arrow_button = QPushButton("", self)
        self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        self.arrow_button.setIconSize(QSize(10,10))
        self.arrow_button.clicked.connect(self.Expand)
        self.arrow_button.move(25, 144)
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
        label.setText("Set session type:")
        label.setAlignment(Qt.AlignLeft)
        label.move(46, 142)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(142, 146)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(420)

        self.testing_rbtn = QRadioButton("Testing", self)
        self.testing_rbtn.setChecked(True)
        self.testing_rbtn.type = "testing"
        self.testing_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.testing_rbtn.move(60, 185)
        self.testing_rbtn.hide()

        self.model_textbox = QLineEdit(self)
        self.model_textbox.move(80, 225)
        self.model_textbox.setText(self.model_path)
        self.model_textbox.setFixedWidth(400)
        self.model_textbox.setMinimumHeight(25)
        self.model_textbox.setPlaceholderText("Model Path")
        qss = """
                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                }"""
        self.model_textbox.setStyleSheet(qss)
        self.model_textbox.hide()

        self.open_model_button = QPushButton("", self)
        self.open_model_button.clicked.connect(self.OpenModelBtnClicked)
        self.open_model_button.move(455, 229)
        self.open_model_button.setIcon(QtGui.QIcon("imgs/open-folder.png"))
        qss = """
                QPushButton {
                    background-color: rgba(0,0,0,0);
                    border: none;
                }"""
        self.open_model_button.setStyleSheet(qss)
        self.open_model_button.hide()

        self.training_rbtn = QRadioButton("Training", self)
        self.training_rbtn.type = "training"
        self.training_rbtn.toggled.connect(self.OnRadioBtnClick)
        self.training_rbtn.move(175, 185)
        self.training_rbtn.hide()

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
        self.warning_label.hide()

        create_button = QPushButton("Create", self)
        create_button.clicked.connect(self.CreateBtnClicked)
        create_button.move(488, 315)
        create_button.setMinimumWidth(80)
        qss = """
                        QPushButton {
                            background-color: #cc1db9;
                            border: 5px solid #cc1db9;
                            border-radius: 10px;
                            color: white;
                            font-size: 12px;
                            font-weight: bold;
                        }"""
        create_button.setStyleSheet(qss)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 299)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(600)

    def CreateBtnClicked(self):
        self.session_name = self.session_name_txtbox.text()
        path = self.path_textbox.text()
        if self.path_textbox.text() == "":
            self.warning_label.setText("App path can't be empty.")
            self.warning_label.show()
            self.warning_button.show()
        elif not os.path.isfile(self.path_textbox.text()):
            self.warning_label.setText("Incorrect app path.")
            self.warning_label.show()
            self.warning_button.show()
        elif os.path.isfile(self.project_path + "\\" + self.session_name + ".ssf"):
            self.warning_label.setText("Session name aleardy exists.")
            self.warning_label.show()
            self.warning_button.show()
        elif self.type=="testing" and self.model_textbox.text()=="":
            self.warning_label.setText("A model must be loaded for testing.")
            self.warning_label.show()
            self.warning_button.show()
        elif self.type=="testing" and not os.path.isfile(self.model_textbox.text()):
            self.warning_label.setText("Invalid model path.")
            self.warning_label.show()
            self.warning_button.show()
        else:
            self.app_path = path
            self.create_signal.emit(self.session_name, self.type, self.app_path, self.model_path)
            self.close()

    def OpenBtnClicked(self):
        self.warning_label.hide()
        self.warning_button.hide()
        path, _ = QFileDialog.getOpenFileName(self, "Choose App", "C://", "Executable (*.exe)")
        if path:
            path_arr = path.split("/")
            if self.session_name == "":
                self.session_name = path_arr[len(path_arr) - 1].split(".")[0]
                self.session_name_txtbox.setText(self.session_name)
            self.app_path = path
        self.path_textbox.setText(self.app_path)

    def OpenModelBtnClicked(self):
        self.warning_label.hide()
        self.warning_button.hide()
        path, _ = QFileDialog.getOpenFileName(self, "Choose Model", "C://", "Model (*.h5)")
        if path:
            self.model_path = path
        self.model_textbox.setText(self.model_path)

    def Expand(self):
        if self.expand_check == True:
            self.testing_rbtn.hide()
            self.training_rbtn.hide()
            self.model_textbox.hide()
            self.open_model_button.hide()
            self.expand_check =False
            self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        else:
            self.testing_rbtn.show()
            self.training_rbtn.show()
            self.model_textbox.show()
            self.open_model_button.show()
            self.expand_check = True
            self.arrow_button.setIcon(QIcon('imgs/down-arrow.png'))

    def OnRadioBtnClick(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            #print("Type is %s" % (radioButton.type))
            self.type = radioButton.type
            if self.type == "testing":
                self.model_textbox.show()
                self.open_model_button.show()

            else:
                self.model_textbox.hide()
                self.open_model_button.hide()


class PropertiesWidget(QWidget):
    def __init__(self, session_path, type, active_check, app_path, model_path, parent=None):
        super().__init__()
        self.parent = parent
        self.title = 'Session Properties'
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 350
        self.setFixedSize(600, 350)
        self.setFixedSize(self.size())
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowMinimizeButtonHint))

        self.expand_check = False
        self.app_path = app_path
        self.session_path = session_path
        self.type = type
        self.model_path = model_path
        self.active_check = active_check

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
        label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        label.setFont(font)
        label.setText("Session path:")
        label.setAlignment(Qt.AlignLeft)
        label.move(30, 35)

        session_txtbox = QLineEdit(self)
        session_txtbox.setText(self.session_path)
        session_txtbox.move(110, 30)
        session_txtbox.setFixedWidth(400)
        session_txtbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 0px;
                }"""
        session_txtbox.setStyleSheet(qss)

        label = QLabel(self)
        font = QFont()
        font.setPointSize(8)
        label.setFont(font)
        label.setText("App path:")
        label.setAlignment(Qt.AlignLeft)
        label.move(30, 90)

        app_path_textbox = QLineEdit(self)
        app_path_textbox.move(100, 85)
        app_path_textbox.setText(self.app_path)
        app_path_textbox.setFixedWidth(410)
        app_path_textbox.setMinimumHeight(25)
        app_path_textbox.setPlaceholderText("App Path")
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 0px;
                }"""
        app_path_textbox.setStyleSheet(qss)

        self.arrow_button = QPushButton("", self)
        self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        self.arrow_button.setIconSize(QSize(10, 10))
        self.arrow_button.clicked.connect(self.Expand)
        self.arrow_button.move(27, 144)
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
        label.setText("Session type:")
        label.setAlignment(Qt.AlignLeft)
        label.move(46, 142)

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(122, 146)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(425)

        self.type_button = QPushButton("", self)
        self.type_button.move(60, 180)
        self.type_button.setIconSize(QSize(20, 20))
        qss = """
                QPushButton {
                    background-color: rgba(0,0,0,0);
                    border: none;
                }"""
        self.type_button.setStyleSheet(qss)
        self.type_label = QLabel(self)
        font = QFont()
        font.setPointSize(11)
        self.type_label.setFont(font)
        self.type_label.setAlignment(Qt.AlignLeft)
        self.type_label.setStyleSheet("QLabel{font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter;}")
        self.type_label.move(92, 180)
        self.type_button.hide()
        self.type_label.hide()
        if self.type=="training":
            self.type_button.setIcon(QtGui.QIcon("imgs/training.png"))
            self.type_label.setText("Training")
        elif self.type=="testing":
            self.type_button.setIcon(QtGui.QIcon("imgs/testing.png"))
            self.type_label.setText("Testing")

            self.model_label = QLabel(self)
            font = QFont()
            font.setPointSize(8)
            self.model_label.setFont(font)
            self.model_label.setText("Model Path:")
            self.model_label.setAlignment(Qt.AlignLeft)
            self.model_label.move(65, 230)

            self.model_textbox = QLineEdit(self)
            self.model_textbox.move(140, 225)
            self.model_textbox.setText(self.model_path)
            self.model_textbox.setFixedWidth(350)
            self.model_textbox.setMinimumHeight(25)
            qss = """
                    QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 0px;
                    }"""
            self.model_textbox.setStyleSheet(qss)
            self.model_label.hide()
            self.model_textbox.hide()

        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, 299)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(600)

        if self.active_check:
            active_button = QPushButton("", self)
            active_button.setIcon(QIcon('imgs/check.png'))
            active_button.setIconSize(QSize(15, 15))
            # arrow_button.clicked.connect(self.CreatBtnClicked)
            active_button.move(27, 318)
            qss = """
                    QPushButton {
                        background-color: rgba(0,0,0,0);
                        border: none;
                    }"""
            active_button.setStyleSheet(qss)

            active_label = QLabel(self)
            active_label.setText("This session is currently active.")
            font = QFont()
            font.setPointSize(8)
            active_label.setFont(font)
            active_label.setAlignment(Qt.AlignLeft)
            active_label.move(55, 319)

    def Expand(self):
        if self.expand_check == True:
            self.type_button.hide()
            self.type_label.hide()
            if type=="testing":
                self.model_label.hide()
                self.model_textbox.hide()
            self.expand_check = False
            self.arrow_button.setIcon(QIcon('imgs/right-arrow.png'))
        else:
            self.type_button.show()
            self.type_label.show()
            if type=="testing":
                self.model_label.show()
                self.model_textbox.show()
            self.expand_check = True
            self.arrow_button.setIcon(QIcon('imgs/down-arrow.png'))


class ConfigurationWidget(QWidget):
    run_signal = QtCore.pyqtSignal(str, str, str, str) #file type & file path & check file & test app path
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
        self.test_case_app_path = ""

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
        self.check_1.toggled.connect(self.OnCheckBtnClick)
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
        self.check_2.toggled.connect(self.OnCheckBtnClick)
        self.check_2.hide()
        self.check_textbox = QLineEdit(self)
        self.check_textbox.move(115, 173)
        self.check_textbox.setText(self.check_file)
        self.check_textbox.setFixedWidth(380)
        self.check_textbox.setMinimumHeight(25)
        qss = """
                QLineEdit {border: 2px solid; border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0); border-radius: 8px; padding: 0px 0px 2px 5px;
                }"""
        self.check_textbox.setStyleSheet(qss)
        self.check_textbox.hide()

        self.session_app_textbox = QLineEdit(self)
        self.session_app_textbox.move(80, 233)
        self.session_app_textbox.setText(self.test_case_app_path)
        self.session_app_textbox.setFixedWidth(350)
        self.session_app_textbox.setMinimumHeight(25)
        self.session_app_textbox.setPlaceholderText("Model Path")
        qss = """
                QLineEdit {border: 2px solid; border-color: #cbcbcb; border-radius: 8px; padding: 0px 0px 0px 5px;
                }"""
        self.session_app_textbox.setStyleSheet(qss)
        self.session_app_textbox.hide()

        self.open_button = QPushButton("", self)
        self.open_button.clicked.connect(self.OpenBtnClicked)
        self.open_button.move(406, 237)
        self.open_button.setIcon(QtGui.QIcon("imgs/open-folder.png"))
        qss = """
                        QPushButton {
                            background-color: rgba(0,0,0,0);
                            border: none;
                        }"""
        self.open_button.setStyleSheet(qss)
        self.open_button.hide()

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
        self.warning_label.setMinimumWidth(400)
        self.warning_label.setAlignment(Qt.AlignLeft)
        self.warning_label.move(55, 276)
        self.warning_label.hide()

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

    def OpenBtnClicked(self):
        self.warning_label.hide()
        self.warning_button.hide()
        path, _ = QFileDialog.getOpenFileName(self, "Choose app", "C://", "Executable (*.exe)")
        if path:
            self.test_case_app_path = path
        self.session_app_textbox.setText(self.test_case_app_path)

    def ConfigureBtnClicked(self):
        if self.session_file == "" and self.check_file == "" and self.steps_file == "":
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("No active files.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Dexter")
            msg.exec_()
            self.close()
        elif self.crash_rbtn.isChecked():
            if self.session_file != "":
                self.run_signal.emit(self.type, self.session_file, "", "")
                self.close()
            elif self.session_file == "":
                self.warning_label.setText("No active session file.")
                self.warning_label.show()
                self.warning_button.show()
        elif self.test_rbtn.isChecked():
            if self.steps_file == "" and self.check_file == "":
                self.warning_label.setText("No active test case.")
                self.warning_label.show()
                self.warning_button.show()
            elif self.check_1.isChecked()==False and self.check_2.isChecked()==False:
                self.warning_label.setText("No test file chosen.")
                self.warning_label.show()
                self.warning_button.show()
            elif self.steps_file == "" and self.check_1.isChecked():
                self.warning_label.setText("No active test steps file.")
                self.warning_label.show()
                self.warning_button.show()
            elif self.check_file == "" and self.check_2.isChecked():
                self.warning_label.setText("No active check file.")
                self.warning_label.show()
                self.warning_button.show()
            elif self.session_app_textbox.text() == "":
                self.warning_label.setText("No app path chosen.")
                self.warning_label.show()
                self.warning_button.show()
            elif not os.path.isfile(self.session_app_textbox.text()):
                self.warning_label.setText("Invalid app path.")
                self.warning_label.show()
                self.warning_button.show()
            else:
                if self.check_1.isChecked():
                    steps = self.steps_file
                else:
                    steps = ""
                if self.check_2.isChecked():
                    check = self.check_file
                else:
                    check = ""
                self.run_signal.emit(self.type, steps, check, self.session_app_textbox.text())
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
            self.session_app_textbox.hide()
            self.open_button.hide()
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
            self.session_app_textbox.hide()
            self.open_button.hide()
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
                self.session_app_textbox.hide()
                self.open_button.hide()
                self.warning_label.hide()
                self.warning_button.hide()
            elif self.type == "test":
                self.session_label.hide()
                self.path_textbox.hide()
                self.check_1.show()
                self.check_2.show()
                self.steps_textbox.show()
                self.check_textbox.show()
                self.session_app_textbox.show()
                self.open_button.show()
                self.warning_label.hide()
                self.warning_button.hide()

    def OnCheckBtnClick(self):
        self.warning_label.hide()
        self.warning_button.hide()
