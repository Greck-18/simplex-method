import sys
from typing import Counter
sys.path.append("D:\course\data")
from pulp import LpMaximize,LpProblem,LpStatus,LpVariable,GLPK,GLPK_CMD,value,lpSum
from pulp.constants import LpMinimize,LpMaximize
from beautifultable import BeautifulTable
from PyQt5 import QtWidgets, uic
from sample import Excel
import simple
import os
import pprint


class MainWindow(QtWidgets.QMainWindow,simple.Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.N=4
        self.M=3
        self.lp_sum=0
        self.all_stocks=0
        self.all_needs=0
        self.text=""
        self.indicator=3
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
        self.btnTamplate.clicked.connect(self.loadTemplate)
        self.model_min=LpProblem("Transportation_LP_Problem",LpMinimize)
        self.model_max=LpProblem("Transportation_LP_Problem",LpMaximize)
        self.table=""
        self.html_header="""<table class="result"><thead><tr><th>Поставщики</th><th>B1</th><th>B2</th><th>B3</th><th>B4</th></tr></thead><tbody>"""


    def getFileName(self):
        file=QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
        if file:
            self.file_name=file[0]


    @staticmethod
    def __checkTypeOfTask(stocks,needs):
        if stocks==needs: return True
        return False


    def loadTemplate(self):
        with open("template_table.txt",encoding="utf-8") as file:
            table_template=file.read()
        self.msgbox.setText(table_template)
        self.msgbox.exec()


    def createHtmlFile(self,text):
        with open("result_table.txt","w",encoding="utf-8") as file:
            template_file=open("css_template.txt","r",encoding="utf-8")
            template_html=template_file.read().strip("\n")
            text=template_html+text
            file.write(text)




    def analyze(self):
        self.info=Excel(self.file_name)
        self.xindex=[(range(1,self.M+1)[i],range(1,self.N+1)[j]) for j in range(self.N) for i in range(self.M)]
        self.x=LpVariable.dicts("x",self.xindex,0,None)
        self.mainMatrix=self.info.getMainMatrix()
        self.sum_stocks=self.info.getSumStocks()
        self.sum_needs=self.info.getSumNeeds()
        if not MainWindow.__checkTypeOfTask(self.sum_stocks,self.sum_needs):
            raise Exception("Please chose another value!")

        self.lp_sum=lpSum(self.mainMatrix[i-1][j-1]*self.x[i,j] for i in range(1,4) for j in range(1,5))
        self.model_min+=self.lp_sum
        self.model_max+=self.lp_sum
        for i in range(1,self.M+1):
            self.all_stocks=self.x[i,1]+self.x[i,2]+self.x[i,3]+self.x[i,4]<=self.info.getAllStocks(self.rowStocks)
            self.model_min+=self.all_stocks
            self.model_max+=self.all_stocks
            self.rowStocks+=1
        for i in range(1,self.N+1):
            self.all_needs=self.x[1,i]+self.x[2,i]+self.x[3,i]>=self.info.getAllNeeds(self.colNeeds)
            self.model_min+=self.all_needs
            self.model_max+=self.all_needs
            self.colNeeds+=1


        self.status_min=self.model_min.solve()
        self.status_min="Your transport problem has been solved!" if self.status_min==1 else "The problem was not solved!"
        for k,v in enumerate(self.model_min.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"

        self.createHtmlFile(self.text)


        self.text_for_solution=f"{self.status_min}\n{46*'-'}\nMinimum:\n{LpStatus[self.model_min.status]}: \nThe minimum costs will be={value(self.model_min.objective)}\n{10*'-'}\n"

        self.status_max=self.model_max.solve()

        self.text=""
        self.indicator=3
        for k,v in enumerate(self.model_max.variables()):
            if k==0:
                self.text+=self.html_header
                self.text+=f"<tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            elif k%4==0:
                self.text+=f"</tr><tr><td>{self.info.getNameSuppliers(self.indicator)}</td>"
                self.indicator+=1
            self.text+=f"<td>{v.varValue}</td>"
            if k==11:
                self.text+="</tr></tbody></table>"


        with open("result_table.txt","a",encoding="utf-8") as file:
            file.write(self.text)



        self.text_for_solution+=f"Maximum:\n{LpStatus[self.model_max.status]}: \nThe maximum costs will be={value(self.model_max.objective)}\n{46*'-'}\n"



        with open("result_table.txt",encoding="utf-8") as file:
            self.table=file.read()

        self.textBrowser.setText(self.table)

        self.textBrowser_2.setText(self.text_for_solution)


def main():
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
