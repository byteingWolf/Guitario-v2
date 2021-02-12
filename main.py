import sys
from PyQt5 import QtWidgets
from gui import MainWindow

"""
Guitario, simple chord recognizer
All created MP4 files are stored in saved_accords directory
"""

if __name__ == '__main__':
    print("Loading application!")
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Guitario")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
