from sys import exit, argv

from PyQt5.QtWidgets import QApplication

from windows import MainWindow


if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec())
