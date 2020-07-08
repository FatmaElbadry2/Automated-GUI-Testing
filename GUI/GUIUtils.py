from GUI_Imports import *
from DialogBoxes import *

#--------------------------------------------------------Menubar--------------------------------------------------------
def UnderlineFirstLetter(string):
    new_str = ""
    for i in range(len(string)):
        if i == 0:
            new_str = string[i] + "\u0332"
        else:
            new_str = new_str + string[i]
    #print(new_str)
    return(new_str)

def CreateFileMenu(window, menubar):
    # ------------1st part------------
    file_str = UnderlineFirstLetter('File')
    fileMenu = menubar.addMenu(file_str)
    fileMenu.setStyleSheet("QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    fileMenu.setMinimumWidth(250)
    newPro = QAction('New Project...', window)
    fileMenu.addAction(newPro)
    newSession = QAction('New Session...', window)
    fileMenu.addAction(newSession)
    open = QAction('Open...', window)
    open.setIcon(QtGui.QIcon("imgs/open.png"))
    fileMenu.addAction(open)
    save = QAction('Save All', window)
    save.setShortcut("Ctrl+S")
    save.setIcon(QtGui.QIcon("imgs/save.png"))
    fileMenu.addAction(save)
    '''openRecentMenu = QMenu('Open Recent', window)
    # supposed to have an array to parse from & max of 5 projects + for loop
    open_act_1 = QAction('...', window)
    openRecentMenu.addAction(open_act_1)
    fileMenu.addMenu(openRecentMenu)'''
    fileMenu.addSeparator()
    # ------------2nd part------------
    importAct = QAction('Import Testcase...', window)
    importAct.setIcon(QtGui.QIcon("imgs/import.png"))
    fileMenu.addAction(importAct)
    exportAct = QAction('Export Testcase...', window)
    exportAct.setIcon(QtGui.QIcon("imgs/export.png"))
    fileMenu.addAction(exportAct)
    fileMenu.addSeparator()
    # ------------3rd part------------
    closeAct = QAction('Close Project', window)
    closeAct.setStatusTip('Close Project')
    closeAct.setIcon(QtGui.QIcon("imgs/close.png"))
    fileMenu.addAction(closeAct)
    exitAct = QAction('Exit', window)
    exitAct.setShortcut('Ctrl+Q')
    exitAct.setStatusTip('Exit application')
    exitAct.setIcon(QtGui.QIcon("imgs/exit.png"))
    exitAct.triggered.connect(window.close)
    fileMenu.addAction(exitAct)

    return newPro, newSession, open, save, importAct, exportAct, closeAct, exitAct

def CreateEditMenu(window, menubar):
    edit_str = UnderlineFirstLetter('Edit')
    editMenu = menubar.addMenu(edit_str)
    editMenu.setStyleSheet(
        "QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    editMenu.setMinimumWidth(250)
    copy_path = QAction('Copy Path', window)
    copy_path.setIcon(QtGui.QIcon("imgs/copy.png"))
    editMenu.addAction(copy_path)

def CreateViewMenu(window, menubar):
    view_str = UnderlineFirstLetter('View')
    viewMenu = menubar.addMenu(view_str)
    viewMenu.setStyleSheet(
        "QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    viewMenu.setMinimumWidth(250)
    full_screen = QAction('Full Screen', window)
    full_screen.setIcon(QtGui.QIcon("imgs/full-screen.png"))
    viewMenu.addAction(full_screen)

def CreateRunMenu(window, menubar):
    run_str = UnderlineFirstLetter('Run')
    runMenu = menubar.addMenu(run_str)
    runMenu.setStyleSheet(
        "QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    runMenu.setMinimumWidth(250)
    run = QAction('Run...', window)
    run.setIcon(QtGui.QIcon("imgs/run2.png"))
    runMenu.addAction(run)

def CreateToolsMenu(window, menubar):
    tools_str = UnderlineFirstLetter('Tools')
    toolsMenu = menubar.addMenu(tools_str)
    toolsMenu.setStyleSheet(
        "QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    toolsMenu.setMinimumWidth(250)
    pref = QAction('Report Preferences', window)
    pref.setIcon(QtGui.QIcon("imgs/report.png"))
    toolsMenu.addAction(pref)
    record = QAction('Screen Recording...', window)
    record.setIcon(QtGui.QIcon("imgs/record.png"))
    toolsMenu.addAction(record)

def CreateHelpMenu(window, menubar):
    help_str = UnderlineFirstLetter('Help')
    helpMenu = menubar.addMenu(help_str)
    helpMenu.setStyleSheet(
        "QMenu{background-color: #efefef; font-size:9.5pt;} QMenu::item:selected{background:#cbcbcb; color: white;}")
    helpMenu.setMinimumWidth(250)
    user_guide = QAction('User Guide', window)
    user_guide.setIcon(QtGui.QIcon("imgs/help.png"))
    helpMenu.addAction(user_guide)

#--------------------------------------------------------Sidebar--------------------------------------------------------
def CreateSidebar(Widget):
    font = QFont()
    font.setPointSize(10)
    font.setBold(True)
    t1 = QTreeWidgetItem(["Project"])
    t1.setIcon(0, QIcon('imgs/project.png'))
    t1.setFont(0, font)
    font = QFont()
    font.setPointSize(10)
    t1_sub = QTreeWidgetItem(["Sessions"])
    t1_sub.setIcon(0, QIcon('imgs/sessions.png'))
    t1_sub.setFont(0, font)
    t1.addChild(t1_sub)

    t2_sub = QTreeWidgetItem(["Test cases"])
    t2_sub.setIcon(0, QIcon('imgs/test.png'))
    t2_sub.setFont(0, font)
    t1.addChild(t2_sub)

    t2_sub_1 = QTreeWidgetItem(["Test Steps"])
    t2_sub_1.setIcon(0, QIcon('imgs/steps.png'))
    t2_sub_1.setFont(0, font)
    t2_sub.addChild(t2_sub_1)

    t2_sub_2 = QTreeWidgetItem(["Check"])
    t2_sub_2.setIcon(0, QIcon('imgs/check.png'))
    t2_sub_2.setFont(0, font)
    t2_sub.addChild(t2_sub_2)

    # here we add the sessions and their paths
    '''for i in range(3):
        t1_child = QTreeWidgetItem(["Child A" + str(i), "Child B" + str(i), "Child C" + str(i)])
        t1_child.setIcon(0, QIcon('imgs/session.png'))
        t1_sub.addChild(t1_child)'''

    tw = QTreeWidget(Widget)
    qss = """
    QTreeWidget {
        background: white;
        border: 1px solid; 
        border-color: #cbcbcb #cbcbcb rgba(0,0,0,0) rgba(0,0,0,0);
    }
    QTreeWidget::item:hover {  
        background-color: '#d8d6d6';
        color: black;
        border: none;
    }
    QTreeWidget::item:selected {  
        background-color: '#d8d6d6';
        color: black;
        border: none;
    }
    QTreeWidget::item:pressed {
        background: '#d8d6d6';
        color: black;
        border: none;
    }"""

    tw.setStyleSheet(qss)
    tw.setColumnCount(1)
    # tw.setHeaderLabels(["Sessions"])
    tw.setHeaderHidden(True)
    tw.addTopLevelItem(t1)
    tw.setMaximumWidth(240)

    '''layout = QVBoxLayout(self.tab1)
    layout.setSpacing(0)
    widget = QWidget(self.tab1)
    layout.addWidget(tw)
    widget.setLayout(layout)'''

    return tw, t1, t1_sub, t2_sub_1, t2_sub_2

def CreateSidebarMenu(Widget):
    # Button bar
    proj_icon = QPushButton(Widget)
    proj_icon.setStyleSheet(
        "QPushButton {background-color: none; border:none;} QPushButton::selected{background-color: none; border:none;}")
    icon = QIcon("imgs/home.png")
    proj_icon.setIcon(icon)
    proj_icon.setIconSize(QSize(15, 15))

    '''label = QLineEdit(self.tab1)
    label.setText("Project")
    label.setDisabled(True)
    label.setMinimumWidth(45)'''
    qss = """
            QComboBox {
               background: rgba(0,0,0,0);
               border: none;
               color: black;
               font-size: 10pt;
            }
            QComboBox::drop-down 
            {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(imgs/down-arrow.png);
                width: 10px;
                height: 13px;
            }"""
    # label.setStyleSheet(qss)

    menu = QComboBox(Widget)
    menu.addItem("Project")
    menu.addItem("Open Files")
    menu.setIconSize(QSize(15, 15))
    menu.setStyleSheet(qss)
    menu.setFixedWidth(90)
    menu.setFixedHeight(30)
    menu.move(10, -5)
    # menu.setStyleSheet("QComboBox {background-color: rgba(0,0,0,0); border:none;}")

    newBtn = QPushButton(Widget)
    newBtn.setStyleSheet("QPushButton {background-color: none; border:none;}")
    icon = QIcon("imgs/new-file.png")
    newBtn.setIcon(icon)
    newBtn.setIconSize(QSize(12, 12))
    newBtn.setToolTip("New session")

    openBtn = QPushButton(Widget)
    openBtn.setStyleSheet("QPushButton {background-color: none; border:none;}")
    icon = QIcon("imgs/open2.png")
    openBtn.setIcon(icon)
    openBtn.setIconSize(QSize(14, 14))
    openBtn.setToolTip("Open session")

    btnLayout = QHBoxLayout(Widget)
    btnWidget = QWidget(Widget)
    btnLayout.addWidget(proj_icon)
    # btnLayout.addWidget(label)
    btnLayout.addWidget(menu)
    hSpacer = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    btnLayout.addSpacerItem(hSpacer)
    btnLayout.addWidget(newBtn)
    hSpacer = QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    btnLayout.addSpacerItem(hSpacer)
    btnLayout.addWidget(openBtn)
    btnWidget.setLayout(btnLayout)
    btnWidget.setFixedHeight(50)
    btnWidget.setFixedWidth(240)
    btnWidget.setStyleSheet(
        "QWidget{background: #efefef; border: 1px solid; border-color: rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0) rgba(0,0,0,0);}")

    return btnWidget, newBtn, openBtn

def CreateToolbar(widget):
    toolbar = QMenuBar(widget)
    qss = """
    QMenuBar{
        background-color:rgba(0,0,0,0);
        border: none
    }
    QMenuBar::item:selected {  
        background-color: '#e6e4e4';
        border: 1px solid;
        border-radius: 5px;
        border-color: '#e6e4e4';
    }
    QMenuBar::item:hover {
        background-color: '#e6e4e4';
        border: 1px solid;
        border-radius: 5px;
        border-color: '#e6e4e4';
    }"""

    toolbar.setStyleSheet(qss)

    new_action = QAction(QIcon('imgs/add-file.png'), ' &New File', widget)
    new_action.setStatusTip("New file")
    toolbar.addAction(new_action)

    open_action = QAction(QIcon('imgs/open-t.png'), 'Open', widget)
    open_action.setStatusTip("Open file")
    toolbar.addAction(open_action)

    save_action = QAction(QIcon('imgs/save-t.png'), 'Save', widget)
    save_action.setStatusTip("Save file")
    toolbar.addAction(save_action)

    copy_action = QAction(QIcon('imgs/copy-t.png'), 'Copy', widget)
    copy_action.setStatusTip("Copy")
    toolbar.addAction(copy_action)

    cut_action = QAction(QIcon('imgs/cut-t.png'), 'Cut', widget)
    cut_action.setStatusTip("Cut")
    toolbar.addAction(cut_action)

    paste_action = QAction(QIcon('imgs/paste-t.png'), 'Paste', widget)
    paste_action.setStatusTip("Paste")
    toolbar.addAction(paste_action)

    undo_action = QAction(QIcon('imgs/undo-t.png'), 'Undo', widget)
    undo_action.setStatusTip("Undo")
    toolbar.addAction(undo_action)

    redo_action = QAction(QIcon('imgs/redo-t.png'), 'Redo', widget)
    redo_action.setStatusTip("Redo")
    toolbar.addAction(redo_action)

    return toolbar

#--------------------------------------------Log bar---------------------------------------------
def CreateLogHBar(widget):
    label = QLineEdit(widget)
    label.setText("Run:")
    label.setDisabled(True)
    label.setMinimumWidth(30)
    qss = """
            QLineEdit {
               background: rgba(0,0,0,0);
               border: none;
               color: black;
               font-size: 9pt;
            }"""
    label.setStyleSheet(qss)

    session_name = QPushButton(widget)
    session_name.setText("  Session Name")
    session_name.setStyleSheet("QPushButton {background-color: none; color: #444444; border: 5px rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);}")
    #session_name.setStyleSheet("QPushButton {background-color: none; border: none;}")
    icon = QIcon("imgs/interfaces.png")
    session_name.setIcon(icon)
    session_name.setIconSize(QSize(13, 13))
    session_name.setMinimumWidth(100)

    # --------------------------------record button--------------------------------------
    qss = """
                QPushButton {
                    background-color:rgba(0,0,0,0);
                    border: none;
                }
                """

    record_btn = QPushButton(widget)
    record_btn.setStyleSheet(qss)
    icon = QIcon("imgs/record-r.png")
    record_btn.setIcon(icon)
    record_btn.setIconSize(QSize(37, 32))
    record_btn.setToolTip("Record session")
    # self.pause.clicked.connect(self.ToggleRunBtn)

    settings_btn = QPushButton(widget)
    settings_btn.setStyleSheet(qss)
    icon = QIcon("imgs/settings.png")
    settings_btn.setIcon(icon)
    settings_btn.setIconSize(QSize(16, 16))
    settings_btn.setToolTip("Run Configuration")

    layout = QHBoxLayout(widget)
    log_bar = QWidget(widget)
    layout.addWidget(label)
    hSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    layout.addSpacerItem(hSpacer)
    layout.addWidget(session_name)
    hSpacer = QtWidgets.QSpacerItem(2000, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    layout.addSpacerItem(hSpacer)
    layout.addWidget(record_btn)
    hSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    layout.addSpacerItem(hSpacer)
    layout.addWidget(settings_btn)
    hSpacer = QtWidgets.QSpacerItem(-9, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    layout.addSpacerItem(hSpacer)
    log_bar.setLayout(layout)
    log_bar.setStyleSheet("QWidget{background: #efefef; border: 1px solid; border-color: rgba(0,0,0,0);}")

    return log_bar, record_btn, settings_btn

def CreateLogVBar(widget):
    qss = """
    QPushButton {
        background-color:rgba(0,0,0,0);
        border: none;
    }"""
    run = QPushButton(widget)
    run.setStyleSheet(qss)
    icon = QIcon("imgs/run.png")
    run.setIcon(icon)
    run.setIconSize(QSize(12, 12))
    run.setToolTip("Run")

    stop = QPushButton(widget)
    stop.setStyleSheet(qss)
    stop.setToolTip("Stop")
    icon = QIcon("imgs/stop.png")
    stop.setIcon(icon)
    stop.setIconSize(QSize(12, 12))
    stop.setDisabled(True)

    clear = QPushButton(widget)
    clear.setStyleSheet(qss)
    icon = QIcon("imgs/delete.png")
    clear.setIcon(icon)
    clear.setIconSize(QSize(12, 12))
    clear.setToolTip("Clear")

    layout = QVBoxLayout(widget)
    log_bar = QWidget(widget)
    layout.addWidget(run)
    vSpacer = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    layout.addSpacerItem(vSpacer)
    layout.addWidget(stop)
    vSpacer = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    layout.addSpacerItem(vSpacer)
    layout.addWidget(clear)
    vSpacer = QtWidgets.QSpacerItem(0, 70, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
    layout.addSpacerItem(vSpacer)
    log_bar.setLayout(layout)
    log_bar.setStyleSheet("QWidget{background: #efefef; border: 1px solid; border-color: #cbcbcb rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);}")

    return log_bar, run, stop, clear

def CreateHLineVLogBar(widget):
    h_line = QFrame(widget)
    h_line.setFrameShape(QFrame.StyledPanel)
    h_line.setLineWidth(0.6)
    h_line.setFrameShape(QFrame.StyledPanel)
    h_line.setStyleSheet(
        "QFrame{background: rgba(0, 0, 0, 0); border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
    h_line.setFixedWidth(30)
    h_line.setFixedHeight(1)
    return h_line

def CreateLogArea(widget):
    text_area = QTextEdit(widget)
    font = QFont()
    font.setPointSize(9)
    text_area.setFont(font)
    text_area.setStyleSheet("QTextEdit {background-color: white; border: 1px solid; border-color: #cbcbcb; padding: 5px 0px 0px 7px; color: #cc1db9;}")
    text_area.setReadOnly(True)
    return text_area