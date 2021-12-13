import openpyxl


class Excel:

    def __init__(self,file):
        self.book=openpyxl.open(file,read_only="true")
        self.sheet=self.book.active
        self.stocks=0
        self.needs=0
        self.name_suppliers=[]
        self.mainMatrix=[]
        self.listOfConsumers=[]
        self.listOfSuppliers=[]
        self.all_info=[]


    def getNameSuppliers(self,row):
        return self.sheet[row][0].value


    def getSumStocks(self):
        for row in range(3,6):
            self.stocks+=self.sheet[row][5].value
        return self.stocks

    def getSumNeeds(self):
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


    def getAllStocks(self,row):
        return self.sheet[row][5].value

    def getAllNeeds(self,col):
        return self.sheet[6][col].value


    def getAllConsumers(self):
        for col in range(1,5):
            self.listOfConsumers.append(self.sheet[2][col].value)
        return self.listOfConsumers

    def getAllSuppliers(self):
        for row in range(3,6):
            self.listOfSuppliers.append(self.sheet[row][0].value)
        return self.listOfSuppliers


    def getAllInfo(self):
        for row in range(3,7):
            for col in range(6):
                self.all_info.append(self.sheet[row][col].value)
        return self.all_info



