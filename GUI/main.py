import sys
from PyQt5 import QtWidgets, uic
import simple
import os


class MainWindow(QtWidgets.QMainWindow,simple.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name=None
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.getFileName)

    def getFileName(self):

        self.listWidget.clear()
        file=QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
        if file:
            self.file_name=file[0]












def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
