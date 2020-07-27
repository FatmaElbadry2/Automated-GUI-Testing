from GUI_Imports import *
from global_imports import *
import pyaudio
import wave
import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class VoiceCommandsWidget(QWidget):
    recorded_text_signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.top = 0
        self.left = 0
        self.width = 350
        self.height = 55
        self.setFixedSize(350, 55)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        #self.setFocus()
        #QtWidgets.qApp.focusChanged.connect(self.OnFocusChanged)

        self.check = False
        self.qss_normal = """
                        QPushButton {
                            background-color: white;
                            border: 1px solid;
                            border-color: #cbcbcb rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
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
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon("imgs/windowlogo.png"))

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def AddItems(self):
        h_line = QFrame(self)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setLineWidth(0.6)
        h_line.setFrameShape(QFrame.StyledPanel)
        h_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb rgba(0, 0, 0, 0);}")
        h_line.move(0, -5)
        h_line.setMaximumHeight(5)
        h_line.setMinimumWidth(350)

        self.start_button = QPushButton("Start Recording", self)
        self.start_button.clicked.connect(self.ToggleStartBtn)
        self.start_button.move(0, 0)
        self.start_button.setMinimumWidth(350)
        qss = """
                QPushButton {
                    background-color: white;
                    border: 1px solid;
                    border-color: #cbcbcb rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                    color: black;
                    font-size: 11px;
                }"""
        self.start_button.setStyleSheet(qss)
        self.start_button.setMinimumHeight(30)

        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.clicked.connect(self.ToggleStopBtn)
        self.stop_button.move(0, 30)
        self.stop_button.setMinimumWidth(350)
        qss = """
                QPushButton {
                    background-color: white;
                    border: 1px solid;
                    border-color: rgba(0,0,0,0) rgba(0,0,0,0) #cbcbcb rgba(0,0,0,0);
                    color: black;
                    font-size: 11px;
                }"""
        self.stop_button.setStyleSheet(qss)
        self.stop_button.setMinimumHeight(25)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) rgba(0, 0, 0, 0) #cbcbcb;}")
        v_line.move(0, 0)
        v_line.setMinimumHeight(60)
        v_line.setMinimumWidth(5)

        v_line = QFrame(self)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setLineWidth(0.6)
        v_line.setFrameShape(QFrame.StyledPanel)
        v_line.setStyleSheet("QFrame{border: 1px solid; border-color: rgba(0, 0, 0, 0)  #cbcbcb rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);}")
        v_line.move(250, 0)
        v_line.setMinimumHeight(60)
        v_line.setMinimumWidth(5)

    def ToggleStartBtn(self):
        self.stop_button.setStyleSheet(self.qss_normal)
        self.start_button.setStyleSheet(self.qss_selected)
        print("Button start button clicked")
        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(CHANNELS)
        sample_width, frames = self.record()
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("Button 2 has been pushed")
        #text = self.convert_to_text()
        self.recorded_text_signal.emit()
        self.close()

    def ToggleStopBtn(self):
        self.start_button.setStyleSheet(self.qss_normal)
        self.stop_button.setStyleSheet(self.qss_selected)
        self.check = True
        #self.record_to_file()
        self.hide()

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("Start recording")
        frames = []
        while not self.check:
            data = stream.read(CHUNK)
            frames.append(data)
            print("Waiting for user to push button 2")
            QCoreApplication.processEvents()
        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()
        return sample_width, frames

    def convert_to_text(self):
        r = sr.Recognizer()
        with sr.AudioFile('output.wav') as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(text)
        return text

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = VoiceCommandsWidget()

    main.show()
    sys.exit(app.exec_())























