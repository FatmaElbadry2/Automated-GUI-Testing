from GUI_Imports import *
from RotatedButton import *
import GUIUtils as utils
from CodeEditor import *
from DialogBoxes import *
from VoiceCommands import *
from StatisticsWidget import *
import _thread
from RL.RLInterface import *
from NLP.NLPInterface import *

class Window(QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, geometry, bug_array):
        super().__init__()

        self.title = "Dexter"
        self.top = 0
        self.left = 0
        self.width = 1600
        self.height = 800
        self.geometry = geometry
        self.bug_array = bug_array
        #--------------Parameters---------------
        #self.path = "fileName [C:\...] - Dexter"
        self.project_path = ""
        self.cfg_file = ""
        self.sidebar_hidden = False
        self.project_created = False
        self.project_opened = False
        self.checkMaximized = False
        self.autocomplete_array = ["menu", "click", "button", "icon", "iconbutton", "textbox", "combobox", "label", "window", "screen", "file", "open", "save"]
        self.current_steps_file = ""
        #self.current_steps_file = "Files\\steps.txt"
        #self.steps_prev_text = self.GetFileText(self.current_steps_file)
        self.current_check_file = ""
        #self.current_check_file = "Files\\check.txt"
        #self.check_prev_text = self.GetFileText(self.current_check_file)

        self.current_session_path = ""
        self.current_app_path = ""
        self.current_session_type = ""
        self.loaded_model_path = ""

        self.run_type = ""
        self.run_session_file = ""
        self.run_steps_file = ""
        self.run_check_file = ""
        self.run_test_app_path = ""

        self.cb = QApplication.clipboard()

        self.main_layout = QHBoxLayout(self)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.resized.connect(self.ResizeEventHandler)

        self.InitializeMainWidget()
        '''self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("QStatusBar{margin-bottom: 10px; margin-left: 50px;}")
        self.setStatusBar(self.statusBar)'''

        self.show()

    def InitializeMainWidget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.CreateMenuBar()
        self.CreateRotatedToggleBtn()
        self.CreateHorizontalLines()
        self.CreateVerticalLines()
        self.CreateSplitFrames()
        self.CreateSidebar(self.upper_frame)
        self.CreateTextEditors()
        self.CreateToolbar()
        self.CreateLog()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    def ResizeEventHandler(self):
        new_width = self.frameGeometry().width()
        new_height = self.frameGeometry().height()
        self.h_line.setFixedWidth(new_width)
        self.v_line.setFixedHeight(new_height-92)
        self.left_v_line.move(new_width - 21, 42)
        self.tree_widget.setFixedHeight(new_height)
        self.left_v_line.setFixedHeight(new_height-92)
        self.upper_frame.setMaximumHeight(new_height * 0.82)
        self.lower_frame.setMaximumHeight(new_height * 0.8)
        self.generate_report.move(new_width - 190, 10)
        self.text_editors_widget.setFixedHeight(new_height)
        self.text_editors_widget.setFixedWidth(new_width-282)
        self.steps_text_editor.setMaximumWidth(new_width*0.8)
        self.check_text_editor.setMaximumWidth(new_width*0.8)
        self.log_h_bar.setFixedWidth(new_width-70)
        self.log.setFixedWidth(new_width - 53)
        self.log.setFixedHeight(new_height*0.9)
        self.h_log_line.move(32, new_height - 55)
        self.h_log_line.setFixedWidth(new_width - 52)
        #self.tab_widget.bottom_h_widget.setMaximumHeight(new_height*0.2)
        if self.sidebar_hidden:
            self.h_toolbar_line.setFixedWidth(new_width - 52)
        elif not self.sidebar_hidden:
            self.h_toolbar_line.setFixedWidth(new_width - 293)

    def CreateHorizontalLines(self):
        self.h_line = QFrame(self)
        self.h_line.setFrameShape(QFrame.StyledPanel)
        self.h_line.setLineWidth(0.6)
        self.h_line.setFrameShape(QFrame.StyledPanel)
        self.h_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        self.h_line.move(0, 24)
        self.h_line.setMaximumHeight(5)
        self.h_line.setMinimumWidth(self.width)

        self.h_toolbar_line = QFrame(self)
        self.h_toolbar_line.setFrameShape(QFrame.StyledPanel)
        self.h_toolbar_line.setLineWidth(0.6)
        self.h_toolbar_line.setFrameShape(QFrame.StyledPanel)
        self.h_toolbar_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        self.h_toolbar_line.move(272, 84)
        self.h_toolbar_line.setMaximumHeight(5)
        self.h_toolbar_line.setFixedWidth(self.width-293)

        self.h_log_line = QFrame(self)
        self.h_log_line.setFrameShape(QFrame.StyledPanel)
        self.h_log_line.setLineWidth(0.6)
        self.h_log_line.setFrameShape(QFrame.StyledPanel)
        self.h_log_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        self.h_log_line.move(32, self.height-22)
        self.h_log_line.setMaximumHeight(5)
        self.h_log_line.setFixedWidth(self.width - 50)

    def CreateVerticalLines(self):
        hSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.main_layout.addSpacerItem(hSpacer)
        self.v_line = QFrame(self)
        self.v_line.setFrameShape(QFrame.StyledPanel)
        self.v_line.setLineWidth(0.6)
        self.v_line.setMaximumWidth(1)
        self.v_line.setFrameShape(QFrame.StyledPanel)
        self.v_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0)  rgba(0, 0, 0, 0) #cbcbcb;}")
        self.v_line.move(32, 42)
        self.v_line.setFixedHeight(self.height-60)
        self.left_v_line = QFrame(self)
        self.left_v_line.setFrameShape(QFrame.StyledPanel)
        self.left_v_line.setLineWidth(0.6)
        self.left_v_line.setFrameShape(QFrame.StyledPanel)
        self.left_v_line.setStyleSheet(
            "QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0)  rgba(0, 0, 0, 0) #cbcbcb;}")
        self.left_v_line.move(self.width-19, 42)
        self.left_v_line.setFixedHeight(self.height-60)
        self.left_v_line.setMaximumWidth(1)

    def CreateRotatedToggleBtn(self):
        self.project_button = RotatedButton("Project", self, orientation="west")
        self.project_button.setMaximumWidth(20)
        self.project_button.setFixedHeight(58)
        self.project_button.move(13, 41)
        qss = """
                        QPushButton {
                            border: 1px solid; 
                            border-color: #cbcbcb #cbcbcb rgba(0,0,0,0) #cbcbcb;
                        }
                        """
        self.project_button.setStyleSheet(qss)
        self.project_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.project_button.clicked.connect(self.ToggleSidebar)

    def CreateSplitFrames(self):
        # setting the hierarchy
        main_h_layout = QVBoxLayout(self.main_widget)
        main_h_widget = QWidget(self.main_widget)

        self.upper_frame = QFrame(self.main_widget)
        self.upper_frame.setFrameShape(QFrame.StyledPanel)
        self.upper_frame.setMaximumHeight(self.height*0.85)
        self.upper_frame.showNormal()
        qss = """
                        QFrame {
                            border: 1px solid; 
                            border-color: #cbcbcb #cbcbcb rgba(0,0,0,0) rgba(0,0,0,0);
                        }
                        """
        self.upper_frame.setStyleSheet(qss)

        qss = """
                        QFrame {
                            border: 1px solid; 
                            border-color: #cbcbcb #cbcbcb #cbcbcb rgba(0,0,0,0);
                        }
                        """
        self.lower_frame = QFrame(self.main_widget)
        self.lower_frame.setFrameShape(QFrame.StyledPanel)
        self.lower_frame.setMaximumHeight(self.height*0.8)
        self.lower_frame.setStyleSheet(qss)

        splitter = QSplitter(Qt.Vertical)
        #self.connect(splitter, QtCore.SIGNAL("splitterMoved(int, int)"), lambda x : self.splitterMoved(splitter))

        # splitter.setStyleSheet('background-color:red')
        splitter.addWidget(self.upper_frame)
        splitter.addWidget(self.lower_frame)
        splitter.setSizes([200, 80])

        main_h_layout.addWidget(splitter)
        main_h_widget.setLayout(main_h_layout)

        self.main_layout.addWidget(main_h_widget)

    def CreateSidebar(self, widget):
        self.btn_memu, self.new_session_btn, self.open_session_btn = utils.CreateSidebarMenu(widget)
        self.btn_memu.move(0,1)
        self.tree_widget, self.tree_project_name, self.tree_sessions, self.tree_test_steps, self.tree_check = utils.CreateSidebar(widget)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.TreeContextMenu)
        #self.tree_test_steps.itemDoubleClicked.connect(self.TestStepsFileDoubleClick)
        #self.tree_check.itemDoubleClicked.connect(self.TestStepsFileDoubleClick)
        self.tree_widget.move(0,47)
        self.new_session_btn.setDisabled(True)
        self.open_session_btn.setDisabled(True)
        self.new_session_btn.clicked.connect(self.NewSessionWidget)
        self.open_session_btn.clicked.connect(self.OpenSession)

    def TreeContextMenu(self, point):
        # Infos about the node selected.
        index = self.tree_widget.indexAt(point)
        if not index.isValid():
            return
        item = self.tree_widget.itemAt(point)
        self.current_tree_child = item
        name = item.text(0)  # The text of the node.
        self.clicked_file = self.project_path + "\\" + name
        if ".txt" in name:
            menu = QtWidgets.QMenu()
            menu.setMinimumWidth(200)
            action = menu.addAction("Open")
            action.setIcon(QtGui.QIcon("imgs/cmenu-open.png"))
            if item.parent().text(0) == "Test Steps":
                self.clicked_steps_file = self.project_path + "\\" + name
                action.triggered.connect(self.OpenFileCMenuSteps)
            elif item.parent().text(0) == "Check":
                self.clicked_check_file = self.project_path + "\\" + name
                action.triggered.connect(self.OpenFileCMenuCheck)
            menu.addSeparator()
            '''action = menu.addAction("Save as")
            #action.triggered.connect(self.SaveFileC)
            action.setIcon(QtGui.QIcon("imgs/cmenu-save.png"))
            menu.addSeparator()'''
            action_1 = menu.addAction("Copy path")
            action_1.triggered.connect(self.CopyPath)
            action_2 = menu.addAction("Rename...")
            action_2.triggered.connect(self.RenameTxt)
            action_3 = menu.addAction("Delete")
            action_3.triggered.connect(self.Delete)
            action_3.setIcon(QtGui.QIcon("imgs/cmenu-delete.png"))
            menu.exec_(self.tree_widget.mapToGlobal(point))
        if ".ssf" in name:
            menu = QtWidgets.QMenu()
            menu.setMinimumWidth(200)
            action = menu.addAction("Set as active session")
            action.setIcon(QtGui.QIcon("imgs/cmenu-check.png"))
            action.triggered.connect(self.SetActiveSession)
            menu.addSeparator()
            action_1 = menu.addAction("Copy path")
            action_1.triggered.connect(self.CopyPath)
            action_2 = menu.addAction("Rename...")
            action_2.triggered.connect(self.RenameSsf)
            action_3 = menu.addAction("Delete")
            action_3.triggered.connect(self.Delete)
            action_3.setIcon(QtGui.QIcon("imgs/cmenu-delete.png"))
            menu.addSeparator()
            action = menu.addAction("Session properties")
            action.setIcon(QtGui.QIcon("imgs/cmenu-proeprties.png"))
            action.triggered.connect(self.PropertiesWidget)
            menu.exec_(self.tree_widget.mapToGlobal(point))

    def CreateToolbar(self):
        # ------------------------------------generate report button-------------------------------------
        qss = """
            QPushButton {
                background-color: #cc1db9;
                border: 5px solid #cc1db9;
                border-radius: 10px;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }"""
        self.generate_report = QPushButton(self.upper_frame)
        self.generate_report.setStyleSheet(qss)
        self.generate_report.setText("Generate Report")
        self.generate_report.setMinimumHeight(28)
        self.generate_report.setFixedWidth(125)
        self.generate_report.move(self.width-190, 10)
        self.generate_report.clicked.connect(self.CreateStatisticsWidget)
        self.toolbar = utils.CreateToolbar(self.upper_frame)
        actions = self.toolbar.actions()
        actions[0].triggered.connect(self.NewFile)
        actions[1].triggered.connect(self.OpenFile)
        actions[2].triggered.connect(self.SaveFile)
        actions[3].triggered.connect(self.Copy)
        actions[4].triggered.connect(self.Cut)
        actions[5].triggered.connect(self.Paste)
        actions[6].triggered.connect(self.Undo)
        actions[7].triggered.connect(self.Redo)

        self.toolbar.move(250, 16)

    def CreateTextEditors(self):
        h_layout = QHBoxLayout(self.upper_frame)
        self.text_editors_widget = QWidget(self.upper_frame)

        self.steps_text_file_path = None
        #self.steps_text_editor = QPlainTextEdit(self.text_editors_widget)
        self.steps_text_editor = QCodeEditor(self.autocomplete_array, self)
        self.steps_text_editor.hide()
        #self.steps_text_editor.textChanged.connect(self.StepsTextChanged)
        self.steps_text_editor.setPlaceholderText("Test steps:")
        self.steps_text_editor.setStyleSheet("QPlainTextEdit{background: white; border: 1px solid; border-color: rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);}")
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(11)
        self.steps_text_editor.setFont(font)
        self.steps_text_editor.setFrameShape(QFrame.StyledPanel)
        self.steps_text_editor.setMaximumWidth(self.width*0.8)
        #self.steps_text_editor.setMinimumWidth(20)

        self.check_text_file_path = None
        self.check_text_editor = QCodeEditor(self.autocomplete_array, self)
        self.check_text_editor.hide()
        #self.check_text_editor.textChanged.connect(self.CheckTextChanged)
        self.check_text_editor.setPlaceholderText("Check:")
        self.check_text_editor.setStyleSheet(
            "QPlainTextEdit{background: white; border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb;}")
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(11)
        self.check_text_editor.setFont(font)
        self.check_text_editor.setFrameShape(QFrame.StyledPanel)
        self.check_text_editor.setMaximumWidth(self.width*0.8)
        #self.check_text_editor.setMinimumWidth(20)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter{border: none;}")

        # self.connect(splitter, QtCore.SIGNAL("splitterMoved(int, int)"), lambda x : self.splitterMoved(splitter))

        # splitter.setStyleSheet('background-color:red')
        splitter.addWidget(self.steps_text_editor)
        splitter.addWidget(self.check_text_editor)
        splitter.setSizes([200, 200])

        self.text_editors_widget.setStyleSheet("QWidget{border: none;}")
        h_layout.addWidget(splitter)
        self.text_editors_widget.setLayout(h_layout)

        self.text_editors_widget.move(232, 40)
        self.text_editors_widget.setFixedHeight(900)
        self.text_editors_widget.setFixedWidth(1350)

        h_layout.addWidget(splitter)

        '''if self.steps_prev_text != "":
            for line in self.steps_prev_text:
                self.steps_text_editor.appendPlainText(line)
        if self.check_prev_text != "":
            for line in self.check_prev_text:
                self.check_text_editor.appendPlainText(line)'''

    def GetFileText(self, file_path):
        f = open(file_path, "r")
        file_lines = f.readlines()
        return file_lines

    def CreateLog(self):
        self.log_h_bar, self.record_btn, self.config_btn, self.voice_record_btn, self.session_name_label = utils.CreateLogHBar(self.lower_frame)
        self.log_h_bar.setFixedWidth(1540)
        self.log_h_bar.setFixedHeight(35)
        self.log_h_bar.move(0, 3)
        self.config_btn.clicked.connect(self.ConfigureWidget)
        self.config_btn.setDisabled(True)
        self.voice_record_btn.setDisabled(True)
        self.voice_record_btn.clicked.connect(self.VoiceCommands)

        self.log_v_bar, self.run, self.stop, clear = utils.CreateLogVBar(self.lower_frame)
        self.log_v_bar.setFixedWidth(30)
        self.log_v_bar.setFixedHeight(175)
        self.log_v_bar.move(0, 40)
        self.run.clicked.connect(self.ToggleRunBtn)
        self.stop.clicked.connect(self.ToggleStopBtn)
        clear.clicked.connect(self.ClearLog)
        self.run.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop.setCursor(QCursor(Qt.PointingHandCursor))
        clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.run.setDisabled(True)

        self.hline_vbar = utils.CreateHLineVLogBar(self.lower_frame)
        self.hline_vbar.move(0, 110)

        self.log = utils.CreateLogArea(self.lower_frame)
        self.log.setFixedWidth(1600 - 53)
        self.log.setFixedHeight(175)
        self.log.move(30, 40)

    def WriteToLog(self, text):
        self.log.append(">> "+text+"\n")

    def ClearLog(self):
        self.log.setText("")

    def CreateMenuBar(self):
        menubar = QMenuBar(self)
        menubar.setStyleSheet("QMenuBar {background-color: #efefef; color: black; font-size:10pt;} QMenuBar::item:selected{background:#cbcbcb; color: white;}")
        self.setMenuBar(menubar)
        menubar.setMinimumWidth(self.width)

        new_project, self.new_session, open, self.save, import_action, self.export_action, self.close_action, exit_action = utils.CreateFileMenu(self, menubar)
        new_project.triggered.connect(self.ShowNewProjectWidget)
        import_action.triggered.connect(self.ImportWidget)
        self.close_action.setDisabled(True)
        self.close_action.triggered.connect(self.CloseProject)
        self.export_action.setDisabled(True)
        self.export_action.triggered.connect(self.Export)
        self.new_session.setDisabled(True)
        self.save.setDisabled(True)
        open.triggered.connect(self.OpenProject)
        self.save.triggered.connect(self.SaveAll)
        self.new_session.triggered.connect(self.NewSessionWidget)

        utils.CreateEditMenu(self, menubar)
        utils.CreateViewMenu(self,menubar)
        utils.CreateRunMenu(self, menubar)
        utils.CreateToolsMenu(self, menubar)
        utils.CreateHelpMenu(self, menubar)

    #--------------------------------------Connecter Functions---------------------------------------------
    def ToggleSidebar(self):
        new_width = self.frameGeometry().width()
        if self.sidebar_hidden == False:
            self.sidebar_hidden = True
            self.tree_widget.hide()
            self.btn_memu.hide()
            self.toolbar.move(3, 16)
            self.h_toolbar_line.move(32, 84)
            self.h_toolbar_line.setFixedWidth(new_width - 52)
            self.text_editors_widget.setFixedWidth(new_width - 42)
            self.text_editors_widget.move(-6, 40)
        else:
            self.sidebar_hidden = False
            self.toolbar.move(250, 16)
            self.h_toolbar_line.move(272, 84)
            self.h_toolbar_line.setFixedWidth(new_width - 293)
            self.text_editors_widget.setFixedWidth(new_width - 282)
            self.text_editors_widget.move(232, 40)
            self.tree_widget.show()
            self.btn_memu.show()

    def CreateStatisticsWidget(self):
        print(self.geometry)
        self.stat_widget = StatisticsWidget(self, self.geometry, self.bug_array)
        self.stat_widget.show()

    def ShowNewProjectWidget(self):
        self.new_proj_widget = NewProjectWidget(self)
        self.new_proj_widget.create_signal.connect(self.CreateSignalReceived)
        self.new_proj_widget.show()

    def CheckCfgFile(self, cfg_file):
        with open(cfg_file, 'r+') as f:
            file_lines = f.readlines()
        for file in file_lines:
            try:
                file = file.split(",")
                type = file[0]
                file_path = file[1]
                file_path = file_path.split("\n")[0]
            except:
                return False
            else:
                if type != "0" and type != "1" and type != "2" and type != "3":
                    return False
                elif not os.path.isfile(file_path):
                    return False
        return True

    def OpenProject(self):
        DEF_DIR = os.path.expanduser('~/Documents')
        dir_list = DEF_DIR.split('/')
        DEF_DIR = dir_list[0] + "\\Documents"
        default_path = DEF_DIR + "\\Dexter Projects"
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory", default_path))
        path_array = path.split("/")
        if path != "":
            self.close_action.setDisabled(False)
            self.export_action.setDisabled(False)
            self.new_session.setDisabled(False)
            self.save.setDisabled(False)
            self.new_session_btn.setDisabled(False)
            self.open_session_btn.setDisabled(False)
            self.config_btn.setDisabled(False)
            self.voice_record_btn.setDisabled(False)
            self.run.setDisabled(False)
            self.project_opened = True
            cfg_file = path + "/" + path_array[len(path_array)-1] +".cfg"
            with open(cfg_file, 'r+') as f:
                file_lines = f.readlines()
            if self.CheckCfgFile(cfg_file):
                self.cfg_file = path + "/" + path_array[len(path_array) - 1] + ".cfg"
                for file in file_lines:
                    file = file.split(",")
                    file_path = file[1].split("\\")
                    self.tree_project_name.setText(0, file_path[len(file_path)-2])
                    file_path = (file_path[len(file_path)-1]).split("\n")
                    if int(file[0]) == 0:
                        t1_child = QTreeWidgetItem([file_path[0]])
                        t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                        self.tree_test_steps.addChild(t1_child)
                    elif int(file[0]) == 1:
                        t1_child = QTreeWidgetItem([file_path[0]])
                        t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                        self.tree_check.addChild(t1_child)
                    elif int(file[0]) == 2 or int(file[0]) == 3:
                        #print(file[0])
                        #print(file_path[0])
                        t1_child = QTreeWidgetItem([file_path[0]])
                        t1_child.setIcon(0, QIcon('imgs/session.png'))
                        self.tree_sessions.addChild(t1_child)
                    self.tree_widget.expandToDepth(2)
                    #print("crash")
                self.steps_text_editor.show()
                self.check_text_editor.show()
                #print(path_array)
                self.project_path = default_path + "\\" + path_array[len(path_array)-1]
            else:
                msg = QMessageBox(self)
                msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                msg.setContentsMargins(10, 10, 0, 0)
                msg.setIcon(QMessageBox.Critical)
                msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                msg.setText("Error loading project, the configuartion file is corrupted.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowTitle("Dexter")
                msg.exec_()

    def NewSessionWidget(self):
        self.new_session_widget = NewSessionWidget(self)
        self.new_session_widget.project_path = self.project_path
        self.new_session_widget.create_signal.connect(self.NewSessionSignalReceived)
        self.new_session_widget.show()

    def SessionExistsError(self):
        msg = QMessageBox(self)
        msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
        msg.setContentsMargins(10, 15, 0, 0)
        msg.setIcon(QMessageBox.Critical)
        msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
        msg.setText("Session already exists.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Dexter")
        msg.exec_()

    def OpenSession(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose Session", self.project_path, "Executable (*.ssf)")
        if path:
            path_arr = path.split("/")
            new_path = ""
            for str in path_arr:
                new_path = new_path + str + "\\"
            new_path = new_path[:len(new_path) - 1]
            check = False
            count = self.tree_sessions.childCount()
            if count != 0:
                for i in range(count):
                    child = self.tree_sessions.child(i)
                    child_name = child.text(0)
                    print(child_name)
                    if child_name == path_arr[len(path_arr) - 1]:
                        self.SessionExistsError()
                        check = True
                        break
            if check == False:
                with open(path, 'rU') as f:
                    lines = f.readlines()
                f.close()
                line = lines[0].split(",")
                name = line[0]
                type = line[1]
                app_path = line[2]
                model_path = line[3]
                self.current_session_path = new_path
                self.current_app_path = app_path
                self.current_session_type = type
                self.loaded_model_path = model_path
                if type=="testing":
                    with open(self.cfg_file, 'a') as f:
                        f.write("2," + new_path + "\n")
                    f.close()
                elif type=="training":
                    with open(self.cfg_file, 'a') as f:
                        f.write("3," + new_path + "\n")
                    f.close()
                t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                t1_child.setIcon(0, QIcon('imgs/session.png'))
                t1_child.setSelected(True)
                self.tree_sessions.addChild(t1_child)
                self.tree_widget.expandToDepth(2)

    def SaveAll(self):
        if self.current_steps_file == "":
            self.SaveAsFile(0)
        else:
            self._save_to_path(self.current_steps_file, 0)
            self.WriteToLog("File saved. Path: " + self.current_steps_file)

        if self.current_check_file == "":
            self.SaveAsFile(1)
        else:
            self._save_to_path(self.current_check_file, 1)
            self.WriteToLog("File saved. Path: " + self.current_check_file)

    def ImportWidget(self):
        if self.project_created == True or self.project_opened == True:
            if self.steps_text_editor.hasFocus():
                if self.steps_text_editor.toPlainText() != "":
                    with open(self.current_steps_file, 'rU') as f:
                        text = f.read()
                    if self.steps_text_editor.toPlainText() != text:
                        value = self.GeneralSaveMsgBox()
                        if value == 1:
                            return
            if self.check_text_editor.hasFocus():
                if self.check_text_editor.toPlainText() != "":
                    with open(self.current_check_file, 'rU') as f:
                        text = f.read()
                    if self.check_text_editor.toPlainText() != text:
                        value = self.GeneralSaveMsgBox()
                        if value == 1:
                            return
            self.import_widget = ImportWidget(self)
            self.import_widget.project_path = self.project_path
            self.import_widget.import_signal.connect(self.ImportSignalReceived)
            self.import_widget.open_signal.connect(self.OpenSignalReceived)
            self.import_widget.show()
        else:
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("No project has been created. Would you like to create one?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            #msg.addButton("Open project", QMessageBox.Ok)
            msg.setWindowTitle("Directory Error")
            choice = msg.exec_()
            if choice == 65536:
                msg.close()
            else:
                self.new_proj_widget = NewProjectWidget(self)
                self.new_proj_widget.create_signal.connect(self.CreateSignalReceived)
                self.new_proj_widget.show()

    def Export(self):
        if self.project_created or self.project_opened:
            path, _ = QFileDialog.getSaveFileName(self, "Export file", self.project_path + "\\.txt", "Text documents (*.txt)")
            if not path:
                return
            path_arr = path.split("/")
            new_path = ""
            for str in path_arr:
                new_path = new_path + str + "\\"
            new_path = new_path[:len(new_path) - 1]
            if self.project_path in new_path:
                msg = QMessageBox(self)
                msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                msg.setContentsMargins(10, 10, 0, 0)
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                msg.setText("Can't export file in same directory. Would you like to save it instead?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setWindowTitle("Directory Error")
                choice = msg.exec_()
                if choice == 65536:
                    pass
                else:
                    if self.steps_text_editor.hasFocus():
                        self._save_to_path(path, 0)
                        t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                        t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                        t1_child.setSelected(True)
                        self.tree_test_steps.addChild(t1_child)
                        self.tree_widget.expandToDepth(2)
                    elif self.check_text_editor.hasFocus():
                        self._save_to_path(path, 1)
                        t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                        t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                        t1_child.setSelected(True)
                        self.tree_check.addChild(t1_child)
                        self.tree_widget.expandToDepth(2)
                    self.WriteToLog("File saved successfully. Path: " + path)
            else:
                msg = QMessageBox(self)
                msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
                msg.setContentsMargins(10, 10, 0, 0)
                msg.setIcon(QMessageBox.Information)
                msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
                msg.setText("Export: " + path_arr[len(path_arr) - 1] + " to the chosen location?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setWindowTitle("Dexter")
                choice = msg.exec_()
                if choice == 65536:
                    pass
                else:
                    if self.steps_text_editor.hasFocus():
                        #print(path)
                        self._save_to_path(path, 0)
                        self.current_steps_file = ""
                    elif self.check_text_editor.hasFocus():
                        self._save_to_path(path, 1)
                        self.current_check_file = ""
                self.WriteToLog("File exported successfully. Path: " + path)

    def CloseProject(self):
        if self.project_created or self.project_opened:
            self.steps_text_editor.setPlainText("")
            self.check_text_editor.setPlainText("")
            self.steps_text_editor.hide()
            self.check_text_editor.hide()
            self.project_opened = False
            self.project_created = False
            self.current_steps_file = ""
            self.current_check_file = ""
            self.tree_project_name.setText(0, "Project")

            self.close_action.setDisabled(True)
            self.export_action.setDisabled(True)
            self.new_session.setDisabled(True)
            self.save.setDisabled(True)
            self.new_session_btn.setDisabled(True)
            self.open_session_btn.setDisabled(True)
            self.config_btn.setDisabled(True)
            self.voice_record_btn.setDisabled(True)
            self.run.setDisabled(True)

            count = self.tree_test_steps.childCount()
            if count !=0:
                for i in range(count, 0 , -1):
                    child = self.tree_test_steps.child(i-1)
                    self.tree_test_steps.removeChild(child)

            count = self.tree_check.childCount()
            if count != 0:
                for i in range(count, 0, -1):
                    child = self.tree_check.child(i-1)
                    self.tree_check.removeChild(child)

            count = self.tree_sessions.childCount()
            if count != 0:
                for i in range(count, 0, -1):
                    child = self.tree_sessions.child(i - 1)
                    self.tree_sessions.removeChild(child)

    def NewFile(self):
        if self.project_opened or self.project_created:
            self.new_file_widget = NewFileWidget(self)
            self.new_file_widget.project_path = self.project_path
            self.new_file_widget.new_file_signal.connect(self.NewFileSignalReceived)
            self.new_file_widget.show()

    def OpenFileDirectoryError(self):
        msg = QMessageBox(self)
        msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
        msg.setContentsMargins(10, 15, 0, 0)
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
        msg.setText(
            "The chosen file does not belong to the current project directory. Would you like to import it?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setWindowTitle("Project Directory Error")
        choice = msg.exec_()
        if choice != 65536:
            # open import file dialog
            pass

    def OpenFile(self):
        if self.steps_text_editor.hasFocus():
            if self.steps_text_editor.toPlainText() != "":
                with open(self.current_steps_file, 'rU') as f:
                    text = f.read()
                if self.steps_text_editor.toPlainText() != text:
                    value = self.GeneralSaveMsgBox()
                    if value == 1:
                        return
            path, _ = QFileDialog.getOpenFileName(self, "Open file", self.project_path, "Text documents (*.txt)")
            path_arr = path.split("/")
            new_path = ""
            for str in path_arr:
                new_path = new_path + str + "\\"
            new_path = new_path[:len(new_path)-1]
            if path:
                if self.project_path in new_path:
                    try:
                        with open(path, 'rU') as f:
                            text = f.read()
                    except Exception as e:
                        self.dialog_critical(str(e))
                    else:
                        check = False
                        count = self.tree_test_steps.childCount()
                        if count != 0:
                            for i in range(count):
                                child = self.tree_test_steps.child(i)
                                child_name = child.text(0)
                                print(child_name)
                                if child_name == path_arr[len(path_arr) - 1]:
                                    print("file already exists")
                                    check = True
                                    break
                        if check == False:
                            with open(self.cfg_file, 'a') as f:
                                f.write("0," + new_path + "\n")
                            f.close()
                            t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                            t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                            t1_child.setSelected(True)
                            self.tree_test_steps.addChild(t1_child)
                            self.tree_widget.expandToDepth(2)
                        self.current_steps_file = path
                        self.steps_text_editor.setPlainText(text)
                else:
                    self.OpenFileDirectoryError()
        elif self.check_text_editor.hasFocus():
            if self.check_text_editor.toPlainText() != "":
                with open(self.current_check_file, 'rU') as f:
                    text = f.read()
                if self.check_text_editor.toPlainText() != text:
                    value = self.GeneralSaveMsgBox()
                    if value == 1:
                        return
            path, _ = QFileDialog.getOpenFileName(self, "Open file", self.project_path, "Text documents (*.txt)")
            path_arr = path.split("/")
            new_path = ""
            for str in path_arr:
                new_path = new_path + str + "\\"
            new_path = new_path[:len(new_path) - 1]
            if path:
                if self.project_path in new_path:
                    try:
                        with open(path, 'rU') as f:
                            text = f.read()
                    except Exception as e:
                        self.dialog_critical(str(e))
                    else:
                        check = False
                        count = self.tree_check.childCount()
                        if count != 0:
                            for i in range(count):
                                child = self.tree_check.child(i)
                                child_name = child.text(0)
                                if child_name == path_arr[len(path_arr) - 1]:
                                    print("file already exists")
                                    check = True
                                    break
                        if check == False:
                            with open(self.cfg_file, 'a') as f:
                                f.write("1," + new_path + "\n")
                            f.close()
                            t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                            t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                            t1_child.setSelected(True)
                            self.tree_check.addChild(t1_child)
                            self.tree_widget.expandToDepth(2)
                        self.current_check_file = path
                        self.check_text_editor.setPlainText(text)
                else:
                    self.OpenFileDirectoryError()

    def SaveFile(self):
        if self.steps_text_editor.hasFocus():
            if self.current_steps_file == "":
                # If we do not have a path, we need to use Save As.
                return self.SaveAsFile(0)
            self._save_to_path(self.current_steps_file, 0)
            self.WriteToLog("File saved. Path: " + self.current_steps_file)

        elif self.check_text_editor.hasFocus():
            if self.current_check_file == "":
                # If we do not have a path, we need to use Save As.
                return self.SaveAsFile(1)
            self._save_to_path(self.current_check_file, 1)
            self.WriteToLog("File saved. Path: " + self.current_check_file)

    def SaveAsFile(self, type):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", self.project_path+"\\.txt", "Text documents (*.txt)")
        if not path:
            return
        path_arr = path.split("/")
        new_path = ""
        for str in path_arr:
            new_path = new_path + str + "\\"
        new_path = new_path[:len(new_path) - 1]
        if path_arr[len(path_arr)-1]==".txt":
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("Invalid file name.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Dexter")
            msg.exec_()
            return
        if self.project_path not in new_path:
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("Can't save file in an external directory. Would you like to export it instead?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setWindowTitle("Directory Error")
            choice = msg.exec_()
            if choice == 65536:
                pass
            else:
                self._save_to_path(path, type)
                if type == 0:
                    self.current_steps_file = ""
                elif type == 1:
                    self.current_check_file = ""
                self.WriteToLog("File exported successfully. Path:" + path)
        else:
            self._save_to_path(path, type)
            self.WriteToLog("File saved successfully. Path: " + path)
            if type == 0:
                with open(self.cfg_file, 'a') as f:
                    f.write("0,"+ new_path +"\n")
                f.close()
                self.current_steps_file = path
                t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                t1_child.setSelected(True)
                self.tree_test_steps.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
            elif type==1:
                with open(self.cfg_file, 'a') as f:
                    f.write("1,"+new_path+"\n")
                f.close()
                self.current_check_file = path
                t1_child = QTreeWidgetItem([path_arr[len(path_arr) - 1]])
                t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                t1_child.setSelected(True)
                self.tree_check.addChild(t1_child)
                self.tree_widget.expandToDepth(2)

    def _save_to_path(self, path, type):
        if type == 0:
            text = self.steps_text_editor.toPlainText()
        elif type == 1:
            text = self.check_text_editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
            f.close()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            if type == 0:
                self.current_steps_file = path
            elif type == 1:
                self.current_steps_file = path

    def Copy(self):
        if self.steps_text_editor.hasFocus():
            self.steps_text_editor.copy()
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.copy()

    def Cut(self):
        if self.steps_text_editor.hasFocus():
            self.steps_text_editor.cut()
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.cut()

    def Paste(self):
        if self.steps_text_editor.hasFocus():
            self.steps_text_editor.paste()
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.paste()

    def Undo(self):
        if self.steps_text_editor.hasFocus():
            self.steps_text_editor.undo()
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.undo()

    def Redo(self):
        if self.steps_text_editor.hasFocus():
            self.steps_text_editor.redo()
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.redo()

    def StepsTextChanged(self):
        Palette = QtGui.QPalette()
        Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
        self.steps_text_editor.setPalette(Palette)
        if os.path.isfile(self.current_steps_file):
            text = self.steps_text_editor.toPlainText()
            with open(self.current_steps_file, 'w') as f:
                f.write(text)
            f.close()

    def CheckTextChanged(self):
        Palette = QtGui.QPalette()
        Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
        self.check_text_editor.setPalette(Palette)
        if os.path.isfile(self.current_check_file):
            text = self.check_text_editor.toPlainText()
            with open(self.current_check_file, 'w') as f:
                f.write(text)
            f.close()

    def ToggleRunBtn(self):
        if self.run_type=="crash":
            self.stop.setEnabled(True)
            self.run.setDisabled(True)
            if self.run_session_file != "":
                #read session file configs and run
                with open(self.current_session_path, 'rU') as f:
                    lines = f.readlines()
                f.close()
                line = lines[0].split(",")
                name = line[0]
                type = line[1]
                app_path = line[2]
                model_path = line[3]
                if type == "training":
                    self.InvokeTraining(app_path)
                    self.WriteToLog("Training session started.")
                    #print(name, type, app_path, model_path)
                    pass
                elif type == "testing":
                    self.InvokeTesting(app_path, model_path)
                    self.WriteToLog("Testing session started.")
                    #print(name, type, app_path, model_path)
                    pass
        elif self.run_type=="test":
            self.stop.setEnabled(True)
            self.run.setDisabled(True)
            self.WriteToLog("Started running test case.")
            if self.run_steps_file != "" and self.run_test_app_path != "":
                self.ExecuteTestCase()
                pass
            if self.run_check_file != "":
                pass
        else:
            msg = QMessageBox(self)
            msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
            msg.setContentsMargins(10, 10, 0, 0)
            msg.setIcon(QMessageBox.Critical)
            msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
            msg.setText("No configurations were made for this run.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Dexter")
            msg.exec_()

    def ToggleStopBtn(self):
        self.run.setEnabled(True)
        self.stop.setDisabled(True)

    def CreateSaveMsgBox(self, type, file_name):
        msg = QMessageBox(self)
        msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
        msg.setContentsMargins(10, 10, 0, 0)
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
        msg.setText("Do you want to save your changes before creating a new file?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)
        msg.setWindowTitle("Dexter")
        choice = msg.exec_()
        #print(choice)
        if choice == 2048:
            file_path = self.project_path + "\\" + file_name + ".txt"
            with open(file_path, 'w') as f:
                f.write("")
            f.close()
            #if file already exists overwrite, if it doesn't create it
            if type == "steps":
                text = self.steps_text_editor.toPlainText()
                with open(self.current_steps_file, 'w') as f:
                    f.write(text)
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("0,"+file_path+"\n")
                f.close()
                self.current_steps_file = file_path
                self.steps_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name + ".txt"])
                t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                t1_child.setSelected(True)
                self.tree_test_steps.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
            elif type == "check":
                text = self.check_text_editor.toPlainText()
                with open(self.current_check_file, 'w') as f:
                    f.write(text)
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("1,"+file_path+"\n")
                f.close()
                self.current_check_file = file_path
                self.check_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name + ".txt"])
                t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                t1_child.setSelected(True)
                self.tree_check.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
        elif choice == 2097152:
            file_path = self.project_path + "\\" + file_name + ".txt"
            with open(file_path, 'w') as f:
                f.write("")
            f.close()
            if type == "steps":
                with open(self.cfg_file, 'a') as f:
                    f.write("0,"+file_path+"\n")
                f.close()
                self.current_steps_file = file_path
                self.steps_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name + ".txt"])
                t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                t1_child.setSelected(True)
                self.tree_test_steps.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
            elif type == "check":
                with open(self.cfg_file, 'a') as f:
                    f.write("1,"+file_path+"\n")
                f.close()
                self.current_check_file = file_path
                self.check_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name + ".txt"])
                t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                t1_child.setSelected(True)
                self.tree_check.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
        elif choice == 4194304:
            pass

    def GeneralSaveMsgBox(self):
        msg = QMessageBox(self)
        msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
        msg.setContentsMargins(10, 10, 0, 0)
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
        msg.setText("Do you want to save your changes first?")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel)
        msg.setWindowTitle("Dexter")
        choice = msg.exec_()
        #print(choice)
        if choice == 2048:
            self.SaveFile()
            return 0
        elif choice == 2097152:
            return 0
        elif choice == 4194304:
            return 1

    def OpenFileCMenuSteps(self):
        if self.steps_text_editor.toPlainText() != "":
            with open(self.current_steps_file, 'rU') as f:
                text = f.read()
            f.close()
            if self.steps_text_editor.toPlainText() != text:
                value = self.GeneralSaveMsgBox()
                if value == 1:
                    return
        try:
            with open(self.clicked_steps_file, 'rU') as f:
                text = f.read()
            f.close()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.steps_text_editor.setPlainText(text)
            self.current_steps_file = self.clicked_steps_file

    def OpenFileCMenuCheck(self):
        if self.check_text_editor.toPlainText() != "":
            with open(self.current_check_file, 'rU') as f:
                text = f.read()
            f.close()
            if self.check_text_editor.toPlainText() != text:
                value = self.GeneralSaveMsgBox()
                if value == 1:
                    return
        try:
            with open(self.clicked_check_file, 'rU') as f:
                text = f.read()
            f.close()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.check_text_editor.setPlainText(text)
            self.current_check_file = self.clicked_check_file

    def CopyPath(self):
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.clicked_file, mode=self.cb.Clipboard)
        self.WriteToLog("Path copied: " + self.clicked_file)

    def RenameTxt(self):
        self.rename_file_widget = RenameFileWidget(0, self)
        self.rename_file_widget.rename_file_signal.connect(self.RenameFileSignalReceived)
        self.rename_file_widget.show()

    def RenameSsf(self):
        self.rename_file_widget = RenameFileWidget(1, self)
        self.rename_file_widget.rename_file_signal.connect(self.RenameFileSignalReceived)
        self.rename_file_widget.show()

    def SetActiveSession(self):
        with open(self.clicked_file, 'rU') as f:
            lines = f.readlines()
        f.close()
        line = lines[0].split(",")
        name = line[0]
        type = line[1]
        app_path = line[2]
        model_path = line[3]
        self.current_session_path = self.clicked_file
        self.current_app_path = app_path
        self.current_session_type = type
        self.loaded_model_path = model_path
        self.session_name_label.setText("  "+name)
        self.WriteToLog("Active session: " + name)
        self.WriteToLog("App path: " + app_path)
        if type=="testing":
            self.WriteToLog("Model path: " + model_path)

    def PropertiesWidget(self):
        with open(self.clicked_file, 'rU') as f:
            lines = f.readlines()
        f.close()
        line = lines[0].split(",")
        name = line[0]
        type = line[1]
        app_path = line[2]
        model_path = line[3]
        if self.current_session_path == self.clicked_file:
            active_check = True
        else:
            active_check = False
        self.properties_widget = PropertiesWidget(self.clicked_file, type, active_check, app_path, model_path)
        self.properties_widget.show()


    def Delete(self):
        msg = QMessageBox(self)
        msg.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))
        msg.setContentsMargins(10, 10, 0, 0)
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("QMessageBox{Background: #f0f0f0; padding: 0px 0px 0px 50px;}")
        msg.setText("Delete file " + self.clicked_file + "?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setWindowTitle("Directory Error")
        choice = msg.exec_()
        if choice == 65536:
            return
        else:
            parent = self.current_tree_child.parent()
            parent.removeChild(self.current_tree_child)
            if parent.text(0) == "Test Steps":
                self.steps_text_editor.setPlainText("")
            else:
                self.check_text_editor.setPlainText("")
            os.remove(self.clicked_file)
            with open(self.cfg_file, 'r+') as f:
                file_lines = f.readlines()
            f.close()
            #print(self.clicked_file)
            new_filelines = []
            for file in file_lines:
                split_file = file.split(",")
                if self.clicked_file in split_file[1]:
                    #print(file)
                    pass
                else:
                    new_filelines.append(file)
            with open(self.cfg_file, 'w') as f:
                for file in new_filelines:
                    f.write(file)
            f.close()

    def ConfigureWidget(self):
        self.config_widget = ConfigurationWidget(self.current_session_path, self.current_steps_file, self.current_check_file, self)
        self.config_widget.run_signal.connect(self.ConfigureRunSignalReceived)
        self.config_widget.show()

    def InvokeTraining(self, app_path):
        action_space = np.empty(2501)
        action_space.fill(-1)
        action_count = np.zeros(2501)
        tree = []
        img_states = {}
        states = {}
        unique_states = {}
        element_ex_count = {}

        app_path = app_path.split("/")
        app_name = app_path[len(app_path)-1]
        print(app_name)
        new_app_path = ""
        for str in app_path[:len(app_path)-1]:
            new_app_path = new_app_path + str + "\\"
        new_app_path = new_app_path[:len(new_app_path)-1]
        print(new_app_path)

        Training(new_app_path, app_name, action_space, action_count, tree, img_states, states, unique_states, element_ex_count)


    def InvokeTesting(self, app_path, model_path):
        pass

    def ExecuteTestCase(self,):
        app_path = self.run_test_app_path.split("/")
        app_name = app_path[len(app_path) - 1]
        print(app_name)
        new_app_path = ""
        for str in app_path[:len(app_path) - 1]:
            new_app_path = new_app_path + str + "\\"
        new_app_path = new_app_path[:len(new_app_path) - 1]
        print(new_app_path)

        with open(self.run_steps_file, 'rU') as f:
            text = f.read()
        f.close()

        NLP(new_app_path, app_name, text)

    def VoiceCommands(self):
        print("innnn")
        self.voice_widget = VoiceCommandsWidget(self)
        self.voice_widget.recorded_text_signal.connect(self.RecordedTextReceived)
        self.voice_widget.show()

    #---------------------------------Signal Handlers----------------------------------
    @QtCore.pyqtSlot()
    def CreateSignalReceived(self):
        #print(self.project_path)
        self.project_created = True
        self.steps_text_editor.show()
        self.check_text_editor.show()
        self.close_action.setDisabled(False)
        self.export_action.setDisabled(False)
        self.new_session.setDisabled(False)
        self.save.setDisabled(False)
        self.new_session_btn.setDisabled(False)
        self.open_session_btn.setDisabled(False)
        self.config_btn.setDisabled(False)
        self.voice_record_btn.setDisabled(False)
        self.run.setDisabled(False)
        project_path = self.project_path.split("\\")
        self.tree_project_name.setText(0, project_path[len(project_path)-1])
        self.cfg_file = self.project_path + "\\" + project_path[len(project_path)-1] + ".cfg"
        with open(self.cfg_file, 'w') as f:
            f.write("")
        f.close()


    @QtCore.pyqtSlot(str, str, str)
    def ImportSignalReceived(self, path, type, file_name):
        print(path)
        file_path = self.project_path + "\\" + file_name
        if type == "steps":
            try:
                with open(path, 'rU') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                with open(self.project_path + "\\" + file_name, 'w') as f:
                    f.write(text)
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("0,"+file_path+"\n")
                f.close()
                self.current_steps_file = path
                self.steps_text_editor.setPlainText(text)
                t1_child = QTreeWidgetItem([file_name])
                t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                t1_child.setSelected(True)
                self.tree_test_steps.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
        elif type == "check":
            try:
                with open(path, 'rU') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                with open(self.project_path + "\\" + file_name, 'w') as f:
                    f.write(text)
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("1,"+file_path+"\n")
                f.close()
                self.current_check_file = path
                self.check_text_editor.setPlainText(text)
                t1_child = QTreeWidgetItem([file_name])
                t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                t1_child.setSelected(True)
                self.tree_check.addChild(t1_child)
                self.tree_widget.expandToDepth(2)

    @QtCore.pyqtSlot()
    def OpenSignalReceived(self):
        print("Open clicked")
        self.OpenFile()

    @QtCore.pyqtSlot(str, str)
    def NewFileSignalReceived(self, file_name, type):
        if type == "steps":
            if self.steps_text_editor.toPlainText() == "":
                file_path = self.project_path + "\\" + file_name + ".txt"
                with open(file_path, 'w') as f:
                    f.write("")
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("0,"+ file_path +"\n")
                f.close()
                self.current_steps_file = file_path
                self.steps_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name+".txt"])
                t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                t1_child.setSelected(True)
                self.tree_test_steps.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
            else:
                with open(self.current_steps_file, 'rU') as f:
                    text = f.read()
                if self.steps_text_editor.toPlainText() != text:
                    self.CreateSaveMsgBox(type, file_name)
                else:
                    file_path = self.project_path + "\\" + file_name + ".txt"
                    with open(file_path, 'w') as f:
                        f.write("")
                    f.close()
                    self.current_steps_file = file_path
                    self.steps_text_editor.setPlainText("")
                    t1_child = QTreeWidgetItem([file_name + ".txt"])
                    t1_child.setIcon(0, QIcon('imgs/steps-file.png'))
                    t1_child.setSelected(True)
                    self.tree_test_steps.addChild(t1_child)
                    self.tree_widget.expandToDepth(2)
        elif type == "check":
            if self.check_text_editor.toPlainText() == "":
                file_path = self.project_path + "\\" + file_name + ".txt"
                with open(file_path, 'w') as f:
                    f.write("")
                f.close()
                with open(self.cfg_file, 'a') as f:
                    f.write("1,"+ file_path +"\n")
                f.close()
                self.current_check_file = file_path
                self.check_text_editor.setPlainText("")
                t1_child = QTreeWidgetItem([file_name+".txt"])
                t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                t1_child.setSelected(True)
                self.tree_check.addChild(t1_child)
                self.tree_widget.expandToDepth(2)
            else:
                with open(self.current_check_file, 'rU') as f:
                    text = f.read()
                if self.check_text_editor.toPlainText() != text:
                    self.CreateSaveMsgBox(type, file_name)
                else:
                    file_path = self.project_path + "\\" + file_name + ".txt"
                    with open(file_path, 'w') as f:
                        f.write("")
                    f.close()
                    self.current_check_file = file_path
                    self.check_text_editor.setPlainText("")
                    t1_child = QTreeWidgetItem([file_name + ".txt"])
                    t1_child.setIcon(0, QIcon('imgs/check-file.png'))
                    t1_child.setSelected(True)
                    self.tree_check.addChild(t1_child)
                    self.tree_widget.expandToDepth(2)

    @QtCore.pyqtSlot(str, int)
    def RenameFileSignalReceived(self, file_name, type):
        if type == 0:
            file_name = file_name + ".txt"
        elif type == 1:
            file_name = file_name + ".ssf"
        old_file = self.clicked_file
        new_file = self.project_path + "\\" + file_name
        old_file_arr = old_file.split("\\")
        old_file = old_file_arr[0]
        for i in old_file_arr[1:]:
            old_file = old_file + "/" + i
        new_file_arr = new_file.split("\\")
        new_file = new_file_arr[0]
        for i in new_file_arr[1:]:
            new_file = new_file + "/" + i
        try:
            os.rename(old_file, new_file)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.current_tree_child.setText(0, new_file_arr[len(new_file_arr)-1])
            with open(self.cfg_file, 'r+') as f:
                file_lines = f.readlines()
            f.close()
            new_filelines = []
            for file in file_lines:
                split_file = file.split(",")
                if self.clicked_file in split_file[1]:
                    new_filelines.append(split_file[0]+","+ self.project_path + "\\" + file_name)
                else:
                    new_filelines.append(file)
            with open(self.cfg_file, 'w') as f:
                for file in new_filelines:
                    f.write(file)
            f.close()
            self.WriteToLog("File " + self.clicked_file + " has been successfully renamed to " + self.project_path + "\\" + file_name + ".")

    @QtCore.pyqtSlot(str, str, str, str)
    def NewSessionSignalReceived(self, session_name, type, app_path, model_path):
        print(session_name)
        print(type)
        print(app_path)
        print(model_path)
        #create session files and add the info
        session_file_path = self.project_path + "\\" + session_name + ".ssf"
        with open(session_file_path, 'w') as f:
            f.write(session_name + "," + type + "," + app_path + "," + model_path)
        f.close()
        self.current_session_path = session_file_path
        self.current_app_path = app_path
        self.current_session_type = type
        self.loaded_model_path = model_path
        if type == "testing":
            with open(self.cfg_file, 'a') as f:
                f.write("2," + session_file_path + "\n")
            f.close()
        elif type == "training":
            with open(self.cfg_file, 'a') as f:
                f.write("3," + session_file_path + "\n")
            f.close()
        t1_child = QTreeWidgetItem([session_name + ".ssf"])
        t1_child.setIcon(0, QIcon('imgs/session.png'))
        t1_child.setSelected(True)
        self.tree_sessions.addChild(t1_child)
        self.tree_widget.expandToDepth(2)

    @QtCore.pyqtSlot(str, str, str, str)
    def ConfigureRunSignalReceived(self, type, path_1, path_2, test_app_path):
        self.run_type = type
        self.WriteToLog("Run configured successfully.")
        print(test_app_path)
        if type == "crash":
            self.run_session_file = path_1
            self.run_steps_file = ""
            self.run_check_file = ""
            self.run_test_app_path = ""
        elif type == "test":
            self.run_session_file = ""
            self.run_steps_file = path_1
            self.run_check_file = path_2
            self.run_test_app_path = test_app_path

    def convert_to_text(self):
        r = sr.Recognizer()
        with sr.AudioFile('output.wav') as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(text)
        return text

    @QtCore.pyqtSlot()
    def RecordedTextReceived(self):
        print("Convertttt")
        text = self.convert_to_text()
        self.steps_text_editor.appendPlainText(text)
        '''if self.steps_text_editor.hasFocus():
        elif self.check_text_editor.hasFocus():
            self.check_text_editor.setPlainText(text)'''

