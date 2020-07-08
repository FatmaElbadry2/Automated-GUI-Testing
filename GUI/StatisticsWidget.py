from GUI_Imports import *
from global_imports import *
from DialogBoxes import *
from PyQt5.QtChart import QChart, QChartView, QBarSet, QPercentBarSeries, QBarCategoryAxis, QBarSeries, QPieSeries, QPieSlice, QLineSeries, QScatterSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class StatisticsWidget(QScrollArea):
    def __init__(self, parent, geometry, bug_array):
        super().__init__()
        self.title = "Dexter Report Analytics"
        self.top = 0
        self.left = 0
        self.setWindowFlags(Qt.Window)
        self.setWindowFlags(self.windowFlags() & ~(QtCore.Qt.WindowMaximizeButtonHint))
        self.width = geometry.width()
        self.height = geometry.height()-20
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.bug_array = bug_array
        #--------------layout---------------
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        #self.setCentralWidget(self.main_widget)
        '''scroll = QScrollArea()
        scroll.setWidget(self)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(self.height)
        self.main_layout.addWidget(scroll)'''
        #self.setLayout(self.main_layout)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        self.horizontalScrollBar().setEnabled(False)

        self.InitializeMainWidget()

        self.showMaximized()

    def InitializeMainWidget(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.title_layout = QHBoxLayout(self.main_widget)
        self.title_widget = QWidget(self.main_widget)
        self.title_widget.setLayout(self.title_layout)
        self.title_widget.setFixedWidth(self.width-40)
        #self.title_widget.setStyleSheet("background-color:red")
        self.title_widget.setFixedHeight(80)
        self.main_layout.addWidget(self.title_widget)
        self.AddTitle()

        self.upper_layout = QHBoxLayout(self.main_widget)
        self.upper_widget = QWidget(self.main_widget)
        self.upper_widget.setLayout(self.upper_layout)
        self.upper_widget.setFixedWidth(self.width-10)
        #self.upper_widget.setStyleSheet("background-color: red")
        self.upper_widget.setFixedHeight(self.height*0.4375)
        self.main_layout.addWidget(self.upper_widget)
        self.CreatePointChart()
        hSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.upper_layout.addSpacerItem(hSpacer)
        self.CreatePieChart()
        hSpacer = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.upper_layout.addSpacerItem(hSpacer)

        self.lower_layout = QHBoxLayout(self.main_widget)
        self.lower_widget = QWidget(self.main_widget)
        self.lower_widget.setLayout(self.lower_layout)
        self.lower_widget.setFixedWidth(self.width-20)
        self.lower_widget.setFixedHeight(self.height*0.425)
        #self.lower_widget.setStyleSheet("background-color: red")
        self.main_layout.addWidget(self.lower_widget)
        self.CreateLeftWidgets()
        self.CreateLineChart()
        self.CreateBarChart()
        vSpacer = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.main_layout.addSpacerItem(vSpacer)
        hSpacer = QtWidgets.QSpacerItem(35, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lower_layout.addSpacerItem(hSpacer)

        self.table_layout = QVBoxLayout(self.main_widget)
        self.table_widget = QWidget(self.main_widget)
        self.table_widget.setLayout(self.table_layout)
        self.table_widget.setFixedWidth(self.width-40)
        #self.table_widget.setFixedHeight(self.height * 0.425)
        #self.table_widget.setStyleSheet("background-color: red")
        self.main_layout.addWidget(self.table_widget)
        self.CreateBugTable(self.bug_array)

    def AddTitle(self):
        layout = QHBoxLayout(self.title_widget)
        widget = QWidget(self.title_widget)
        widget.setLayout(layout)
        widget.setStyleSheet("QWidget{background-color: #cc1db9; border: 1px solid; border-radius: 20px; padding: 5px, 5px, 10px, 0px; border-color: #cc1db9;}")
        widget.setFixedWidth(self.width-48)
        widget.setFixedHeight(70)

        hSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addSpacerItem(hSpacer)

        label = QLabel(self)
        font = QFont()
        font.setPointSize(24)
        label.setFont(font)
        label.setText("Run Analytics")
        label.setAlignment(Qt.AlignLeft)
        #label.move(5, 5)
        label.setStyleSheet("QLabel{background-color: none; border: none; color: #ffffff; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif; font-weight: lighter; letter-spacing: 2px;}")
        layout.addWidget(label)
        self.title_layout.addWidget(widget)

    def CreatePointChart(self):
        label = QLabel(self.main_widget)
        font = QFont()
        font.setPointSize(21)
        label.setFont(font)
        label.setText("Unique states per action")
        label.setAlignment(Qt.AlignLeft)
        label.move(self.width-(self.width-52), self.height-(self.height-120))
        label.setFixedWidth(400)
        label.setMinimumHeight(40)
        label.setStyleSheet("QLabel{color: #4e5052; font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter; letter-spacing: 1.5px;}")

        layout = QHBoxLayout(self.upper_widget)
        widget = QWidget(self.upper_widget)
        widget.setLayout(layout)
        '''widget = QFrame(self.upper_widget)
        widget.setFrameShape(QFrame.StyledPanel)
        widget.showNormal()'''
        widget.setStyleSheet("QWidget{background-color: #ffffff; border: 5px solid #ffffff; border-radius: 20px; padding: 15px, 5px, 10px, 0px;}")
        widget.setFixedWidth(self.upper_widget.width()*0.774)
        widget.setFixedHeight(self.upper_widget.height()-7)

        chart = QChart()

        series = QScatterSeries(self)
        series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(12.0)
        series.append(1, 6)
        series.append(20, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(1, 5)
        series << QPointF(1, 1) << QPointF(13, 3) << QPointF(16, 6) << QPointF(1, 10) << QPointF(15, 2)
        series.setBrush(QColor(qRgb(194, 138, 221)))
        chart.addSeries(series)

        series = QScatterSeries(self)
        series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(12.0)
        series.append(15, 5)
        series.append(21, 5)
        series.append(13, 7)
        series.append(7, 3)
        series.append(10, 5)
        series.setBrush(QColor(qRgb(145, 130, 223)))
        chart.addSeries(series)

        series = QScatterSeries(self)
        series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(12.0)
        series.append(8, 5)
        series.append(24, 5)
        series.append(1, 7)
        series.append(15, 3)
        series.append(12, 5)
        series.setBrush(QColor(qRgb(147, 160, 238)))
        chart.addSeries(series)

        #chart.createDefaultAxes()
        x_axis = QValueAxis()
        x_axis.setRange(0,25)
        x_axis.setLabelFormat("%.0f")
        x_axis.setTickCount(25)
        y_axis = QValueAxis()
        y_axis.setRange(0, 20)
        y_axis.setLabelFormat("%.0f")
        chart.setAxisX(x_axis)
        chart.setAxisY(y_axis)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #chart.setTitle("Line Chart Example")

        chart.legend().setVisible(False)
        #chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.verticalScrollBar().setEnabled(False)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setFixedWidth((self.upper_widget.width()*0.774)-20)
        chartview.setFixedHeight(self.upper_widget.height()-45)
        chartview.chart().setBackgroundBrush(QtGui.QColor("transparent"))

        self.upper_layout.addWidget(widget)
        layout.addWidget(chartview)
        chartview.move(-10, 5)
        hSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addSpacerItem(hSpacer)
        #self.setCentralWidget(chartview)


    def CreatePieChart(self):
        label = QLabel(self.main_widget)
        font = QFont()
        font.setPointSize(20)
        label.setFont(font)
        label.setText("Coverage")
        label.setAlignment(Qt.AlignLeft)
        label.move(self.width-(self.width-1555), self.height-(self.height-120))
        label.setFixedWidth(400)
        label.setFixedHeight(70)
        label.setStyleSheet("QLabel{color: #4e5052; font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter; letter-spacing: 1.5px;}")

        layout = QHBoxLayout(self.upper_widget)
        widget = QWidget(self.upper_widget)
        widget.setLayout(layout)
        widget.setStyleSheet(
            "QWidget{background-color: #ffffff; border: 5px solid #ffffff; border-radius: 20px; padding: 0px, 0px, 0px, 30px;}")
        widget.setFixedWidth(self.upper_widget.width()*0.2)
        widget.setFixedHeight(self.upper_widget.height()-7)

        series = QPieSeries()
        series.append("70%", 70)
        series.append("", 30)

        # adding slice
        slice = QPieSlice()
        slice = series.slices()[0]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(QColor(qRgb(96,153,232)), 2))
        slice.setBrush(QColor(qRgb(96,153,232)))

        slice = QPieSlice()
        slice = series.slices()[1]
        slice.setPen(QPen(QColor(qRgb(145,197,255)), 2))
        slice.setBrush(QColor(qRgb(145,197,255)))

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #chart.setTitle("Pie Chart Example")

        chart.legend().setVisible(False)
        #chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.verticalScrollBar().setEnabled(False)
        chartview.setRenderHint(QPainter.Antialiasing)
        chartview.setFixedWidth((self.upper_widget.width()*0.2)-10)
        chartview.setFixedHeight(self.upper_widget.height()-50)
        chartview.chart().setBackgroundBrush(QtGui.QColor("transparent"))

        self.upper_layout.addWidget(widget)
        layout.addWidget(chartview)
        hSpacer = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addSpacerItem(hSpacer)

        #self.setCentralWidget(chartview)

    def CreateWidgetItem(self, widget, title, value, icon, type):
        layout_h = QHBoxLayout(widget)
        widget_h = QWidget(widget)
        widget_h.setLayout(layout_h)
        widget_h.setStyleSheet("QWidget{background-color: #ffffff; border: 5px solid #ffffff; border-radius: 20px; padding: 0px, 0px, 0px, 0px;}")
        widget_h.setFixedWidth((self.lower_widget.width()*0.16)-10)
        widget_h.setFixedHeight(self.lower_widget.height()*0.3)

        hSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout_h.addSpacerItem(hSpacer)

        icon_btn = QPushButton(widget_h)
        icon_btn.setStyleSheet("QPushButton{background: none; border: none;}")
        icon_btn.setMinimumHeight(50)
        icon_btn.setFixedWidth(50)
        icon_btn.setIconSize(QSize(50,50))
        icon_btn.setIcon(QIcon(icon))
        layout_h.addWidget(icon_btn)

        widget_v = QFrame(widget_h)
        widget_v.setFrameShape(QFrame.StyledPanel)
        widget_v.showNormal()
        widget_v.setFixedWidth(150)
        widget_v.setFixedHeight(95)
        label = QLabel(widget_v)
        font = QFont()
        font.setPointSize(16)
        label.setFont(font)
        label.setText(" "+title)
        label.setAlignment(Qt.AlignLeft)
        label.setAlignment(Qt.AlignTop)
        label.setFixedWidth(150)
        label.setStyleSheet("QLabel{background-color: none; border: none; color: #4e5052; font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter; letter-spacing: 1.5px; padding: 0px;}")
        label.move(0,7)

        label = QLabel(widget_v)
        font = QFont()
        font.setPointSize(34)
        label.setFont(font)
        label.setText(value)
        label.setAlignment(Qt.AlignLeft)
        label.setAlignment(Qt.AlignTop)
        label.setFixedWidth(150)
        label.setFixedHeight(50)
        label.setStyleSheet("QLabel{background-color: none; border: none; color: #4e5052; font-weight: lighter; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif; letter-spacing: 1.5px; padding: 0px;}")
        label.move(0,35)

        if type==0:
            label = QLabel(widget_v)
            font = QFont()
            font.setPointSize(14)
            label.setFont(font)
            label.setText("s")
            label.setAlignment(Qt.AlignLeft)
            label.setAlignment(Qt.AlignTop)
            label.setFixedWidth(150)
            label.setFixedHeight(45)
            label.setStyleSheet(
                "QLabel{background-color: none; border: none; color: #4e5052; font-weight: lighter; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif; letter-spacing: 1.5px; padding: 0px;}")
            label.move(115, 55)

        hSpacer = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout_h.addSpacerItem(hSpacer)
        layout_h.addWidget(widget_v)
        #layout.addWidget(widget_h)
        return widget_h


    def CreateLeftWidgets(self):
        widget = QFrame(self.lower_widget)
        widget.setFrameShape(QFrame.StyledPanel)
        widget.showNormal()
        widget.setStyleSheet("QWidget{background-color: none; border: none;}")
        widget.setFixedWidth(self.lower_widget.width()*0.1575)
        widget.setFixedHeight(self.lower_widget.height()-10)

        widget_1 = self.CreateWidgetItem(widget, "Runtime", "1520", 'imgs/timer.png', 0)
        widget_2 = self.CreateWidgetItem(widget, "Bugs", "5", 'imgs/bug.png', 1)
        widget_2.move(0, self.lower_widget.height()*0.33)
        widget_3 = self.CreateWidgetItem(widget, "Unique States", "200", 'imgs/state.png', 2)
        widget_3.move(0, self.lower_widget.height()*0.66)

        self.lower_layout.addWidget(widget)

    def CreateLineChart(self):
        label = QLabel(self.main_widget)
        font = QFont()
        font.setPointSize(18)
        label.setFont(font)
        label.setText("State Occurrences")
        label.setAlignment(Qt.AlignLeft)
        label.move(self.width -(self.width-360), self.height-(self.height-575))
        label.setFixedWidth(400)
        label.setStyleSheet(
            "QLabel{color: #4e5052; font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter; letter-spacing: 1.5px;}")

        layout = QVBoxLayout(self.lower_widget)
        widget = QWidget(self.lower_widget)
        widget.setLayout(layout)
        widget.setStyleSheet("QWidget{background-color: #ffffff; border: 5px solid #ffffff; border-radius: 20px; padding: 15px, 5px, 10px, 0px;}")
        widget.setFixedWidth(self.width*0.4)
        widget.setFixedHeight(self.lower_widget.height()-20)

        series = QLineSeries(self)
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)
        series.setBrush(QColor(qRgb(255, 160, 238)))

        chart = QChart()

        chart.addSeries(series)
        x_axis = QValueAxis()
        x_axis.setRange(0, 2000)
        x_axis.setLabelFormat("%.0f")
        x_axis.setTickCount(20)
        y_axis = QValueAxis()
        y_axis.setRange(0, 20)
        y_axis.setLabelFormat("%.0f")
        chart.setAxisX(x_axis)
        chart.setAxisY(y_axis)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().setVisible(False)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.verticalScrollBar().setEnabled(False)
        chartview.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(chartview)
        self.lower_layout.addWidget(widget)

    def CreateBarChart(self):
        label = QLabel(self.main_widget)
        font = QFont()
        font.setPointSize(18)
        label.setFont(font)
        label.setText("Action Statistics")
        label.setAlignment(Qt.AlignLeft)
        label.move(self.width -(self.width-1150), self.height-(self.height-575))
        label.setFixedWidth(400)
        label.setStyleSheet("QLabel{color: #4e5052; font-family: Century Gothic, CenturyGothic, AppleGothic, sans-serif; font-weight: lighter; letter-spacing: 1.5px;}")
        hSpacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.lower_layout.addSpacerItem(hSpacer)
        layout = QVBoxLayout(self.lower_widget)
        widget = QWidget(self.lower_widget)
        widget.setLayout(layout)
        widget.setStyleSheet(
            "QWidget{background-color: #ffffff; border: 5px solid #ffffff; border-radius: 20px; padding: 15px, 5px, 10px, 0px;}")
        widget.setFixedWidth(self.width*0.41)
        widget.setFixedHeight(self.lower_widget.height()-18)

        set0 = QBarSet("Parwiz")
        set0.setBrush(QColor(qRgb(210, 170, 245)))

        set0 << 1 << 2 << 3 << 4 << 5 << 6 << 10 << 8 << 6 << 7 << 8 << 3 << 6 << 7 <<6

        series = QBarSeries()
        series.append(set0)

        chart = QChart()
        chart.addSeries(series)
        #chart.setTitle("Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = ["button", "tab", "combobox", "submenu",  "icon button", "close", "save", "load", "redo", "undo", "export", "new", "info", "settings", "label"]
        #print(len(categories))
        '''axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)'''

        x_axis = QBarCategoryAxis()
        x_axis.append(categories)
        x_axis.setLabelsAngle(-85)
        y_axis = QValueAxis()
        y_axis.setRange(0, 20)
        y_axis.setLabelFormat("%.0f")
        chart.setAxisX(x_axis, series)
        chart.setAxisY(y_axis)

        chart.legend().setVisible(False)
        #chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        chartView.verticalScrollBar().setEnabled(False)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setFixedWidth(widget.width()-15)
        chartView.setFixedHeight(widget.height()-10)

        layout.addWidget(chartView)
        self.lower_layout.addWidget(widget)

    def AddBug(self, ID, type, time, action):
        if ID == "":
            ID = "-"
        if type == "":
            type = "-"
        if time == "":
            time = "-"
        if action == "":
            action = "-"

        layout = QHBoxLayout(self.table_widget)
        widget = QWidget(self.table_widget)
        widget.setLayout(layout)
        widget.setStyleSheet(
            "QWidget{background-color: #ffffff; border: 1px solid; border-radius: 20px; padding: 5px, 5px, 10px, 0px; border-color: #ffffff;}")
        widget.setFixedWidth(self.width - 48)
        widget.setFixedHeight(45)

        hSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setText(ID)
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #4e5052; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;  font-weight: lighter; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setText(type)
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #4e5052; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;  font-weight: lighter; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setText(time)
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #4e5052; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;  font-weight: lighter; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setText(action)
        label.setFixedWidth(280)
        label.setMinimumHeight(40)
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #4e5052; font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;  font-weight: lighter; letter-spacing: 2px;}")
        layout.addWidget(label)
        return widget

    def CreateBugTable(self, bug_array):
        dir_ = QtCore.QDir("Roboto")
        _id = QtGui.QFontDatabase.addApplicationFont("Fonts/Roboto-Regular.ttf")
        layout = QHBoxLayout(self.table_widget)
        widget = QWidget(self.table_widget)
        widget.setLayout(layout)
        widget.setStyleSheet(
            "QWidget{background-color: #cc1db9; border: 1px solid; border-radius: 20px; padding: 5px, 5px, 10px, 0px; border-color: #cc1db9;}")
        widget.setFixedWidth(self.width - 48)
        widget.setFixedHeight(50)

        hSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        label.setText("Bug ID")
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #ffffff; text-transform: uppercase; font-weight: 500; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        label.setText("Type")
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #ffffff; text-transform: uppercase; font-weight: 500; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        label.setText("Occured at")
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #ffffff; text-transform: uppercase; font-weight: 500; letter-spacing: 2px;}")
        layout.addWidget(label)

        hSpacer = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(hSpacer)

        label = QLabel(widget)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        label.setText("User action")
        label.setFixedWidth(280)
        label.setAlignment(Qt.AlignLeft)
        # label.move(5, 5)
        label.setStyleSheet(
            "QLabel{background-color: none; border: none; color: #ffffff; text-transform: uppercase; font-weight: 500; letter-spacing: 2px;}")
        layout.addWidget(label)

        self.table_layout.addWidget(widget)

        vSpacer = QtWidgets.QSpacerItem(0, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.table_layout.addSpacerItem(vSpacer)

        for i in range(len(bug_array)):
            #print(bug_array[i][0], bug_array[i][1], bug_array[i][2], bug_array[i][3])
            bug_widget = self.AddBug(bug_array[i][0], bug_array[i][1], bug_array[i][2], bug_array[i][3])
            self.table_layout.addWidget(bug_widget)


'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    geometry = app.desktop().availableGeometry()
    bug_array = []
    bug_array.append(["0", "Crash", "09:10", "Continue"])
    bug_array.append(["1", "Crash", "11:59", ""])
    bug_array.append(["2", "Error", "14:30", "Continue"])
    bug_array.append(["3", "Error", "16:50", "Continue"])
    bug_array.append(["4", "Crash", "20:40", "Halt"])

    main = StatisticsWidget(app, geometry, bug_array=bug_array)
    main.show()
    sys.exit(app.exec_())'''