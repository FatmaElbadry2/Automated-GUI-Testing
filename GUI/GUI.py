from GUI_Imports import *
from MainWindow import *


if __name__ == "__main__":

    app = QApplication(sys.argv)
    geometry = app.desktop().availableGeometry()

    bug_array = []
    bug_array.append(["0", "Crash", "09:10", "Continue"])
    bug_array.append(["1", "Crash", "11:59", ""])
    bug_array.append(["2", "Error", "14:30", "Continue"])
    bug_array.append(["3", "Error", "16:50", "Continue"])
    bug_array.append(["4", "Crash", "20:40", "Halt"])

    pixmap = QPixmap("imgs/logo.png")
    splash = QSplashScreen(pixmap)
    splash.resize(470, 250)
    splash.show()

    start = time.time()

    while time.time() < start + 2:
        app.processEvents()

    window = Window(geometry, bug_array=bug_array)
    window.show()
    splash.finish(window)

    sys.exit(app.exec())

