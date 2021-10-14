import openpyxl


class Excel:

    def __init__(self,file):
        self.book=openpyxl.open(file,read_only="true")
        self.sheet=self.book.active
        self.stocks=0
        self.needs=0
        self.mainMatrix=[]


    def getStocksInfo(self):
        for row in range(3,6):
            self.stocks+=self.sheet[row][5].value
        return self.stocks

    def getNeedsInfo(self):
        for col in range(1,5):
            self.needs+=self.sheet[6][col].value
        return self.needs

    def getMainMatrix(self):
        for row in range(3,6):
            self.help=[]
            for col in range(1,5):
                self.help.append(self.sheet[row][col].value)
            self.mainMatrix.append(self.help)
        return self.mainMatrix
