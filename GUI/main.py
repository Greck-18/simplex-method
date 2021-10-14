import sys
sys.path.append("D:\course\data")
from PyQt5 import QtWidgets, uic
from sample import Excel
import simple
import os


class MainWindow(QtWidgets.QMainWindow,simple.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name=None
        self.stocks=None
        self.needs=None
        self.mainMatrix=None
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.getFileName)
        self.btnStart.clicked.connect(self.analyze)

    def getFileName(self):

        self.listWidget.clear()
        file=QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
        if file:
            self.file_name=file[0]

    def analyze(self):

        self.mainMatrix=Excel(self.file_name).getMainMatrix()
        self.stocks=Excel(self.file_name).getStocksInfo()
        self.needs=Excel(self.file_name).getNeedsInfo()
        















def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
