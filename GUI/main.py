import sys
sys.path.append("D:\course\data")
from pulp import LpMaximize,LpProblem,LpStatus,LpVariable,GLPK,GLPK_CMD,value,lpSum
from pulp.constants import LpMinimize
from beautifultable import BeautifulTable
from PyQt5 import QtWidgets, uic
from sample import Excel
import simple
import os


class MainWindow(QtWidgets.QMainWindow,simple.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.N=4
        self.M=3
        self.xindex=None
        self.listForTable=[]
        self.model=None
        self.file_name=None
        self.rowStocks=3
        self.colNeeds=1
        self.stocks=None
        self.needs=None
        self.mainMatrix=None
        self.x=None
        self.setupUi(self)
        self.btnBrowse.clicked.connect(self.getFileName)
        self.btnStart.clicked.connect(self.analyze)
        self.model=LpProblem("Transportation_LP_Problem",LpMinimize)
        self.table=BeautifulTable()

    def getFileName(self):
        self.listWidget.clear()
        file=QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
        if file:
            self.file_name=file[0]


    @staticmethod
    def __checkTypeOfTask(stocks,needs):
        if stocks==needs: return True
        return False


    def createTable(self):
        self.table.columns.header=Excel(self.file_name).getAllConsumers()
        self.table.rows.header=Excel(self.file_name).getAllSuppliers()




    def analyze(self):

        self.xindex=[(range(1,self.M+1)[i],range(1,self.N+1)[j]) for j in range(self.N) for i in range(self.M)]
        self.x=LpVariable.dicts("x",self.xindex,0,None)
        self.mainMatrix=Excel(self.file_name).getMainMatrix()
        self.sum_stocks=Excel(self.file_name).getSumStocks()
        self.sum_needs=Excel(self.file_name).getSumNeeds()
        if not MainWindow.__checkTypeOfTask(self.sum_stocks,self.sum_needs):
            raise Exception("Please chose another value!")

        self.model+=lpSum(self.mainMatrix[i-1][j-1]*self.x[i,j] for i in range(1,4) for j in range(1,5))
        for i in range(1,self.M+1):
            self.model+=self.x[i,1]+self.x[i,2]+self.x[i,3]+self.x[i,4]<=Excel(self.file_name).getAllStocks(self.rowStocks)
            self.rowStocks+=1
        for i in range(1,self.N+1):
            self.model+=self.x[1,i]+self.x[2,i]+self.x[3,i]>=Excel(self.file_name).getAllNeeds(self.colNeeds)
            self.colNeeds+=1

        self.model.solve()
        self.createTable()
        for k,v in enumerate(self.model.variables()):
            # print(k,"-",v.varValue)
            self.listForTable.append(v.varValue)
            if k%4==0 and k!=0:
                # self.table.rows.append(self.listForTable)

                # print(self.listForTable)
                self.listForTable=[]
                break

        # self.createTable()

        print(self.table)
        # self.label.setText()
        # self.listWidget.addItem(f"{LpStatus[self.model.status]}")
        # self.listWidget.addItem(f"Objective Function:{value(self.model.objective)}")



















def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
