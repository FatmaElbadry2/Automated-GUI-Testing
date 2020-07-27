import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton

import pyaudio
import wave
import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

btn2pushed = False
stop_signal = pyqtSignal()

def window():
    app = QApplication(sys.argv)
    win = QDialog()
    b1 = QPushButton(win)
    b1.setText("Button1")
    b1.move(50,20)
    b1.clicked.connect(b1_clicked)

    b2 = QPushButton(win)
    b2.setText("Button2")
    b2.move(50,50)
    b2.clicked.connect(b2_clicked)

    win.setGeometry(100,100,200,100)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())

def b1_clicked():
   print ("Button 1 clicked")
   wf = wave.open('output.wav', 'wb')
   wf.setnchannels(CHANNELS)
   sample_width, frames = record()
   wf.setsampwidth(sample_width)
   wf.setframerate(RATE)
   wf.writeframes(b''.join(frames))
   wf.close()
   '''i = 0
   while ( btn2pushed != True ):
       # not doing anything
       if ( i % 100000 == 0 ):
           print ("Waiting for user to push button 2")
       QCoreApplication.processEvents()
       i += 1'''

   print ("Button 2 has been pushed")


def b2_clicked():
    global btn2pushed
    btn2pushed = True

def record():
    global btn2pushed
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start recording")
    frames = []
    while not btn2pushed:
        data = stream.read(CHUNK)
        frames.append(data)
        print("Waiting for user to push button 2")
        QCoreApplication.processEvents()
    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return sample_width, frames

def record_to_file():
    r = sr.Recognizer()
    with sr.AudioFile('output.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
    return text

if __name__ == '__main__':
   window()